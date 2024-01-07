import itertools
import re
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Union

import pydantic
from pydantic import BaseModel

from classiq.interface.generator.arith.arithmetic import Arithmetic
from classiq.interface.generator.control_state import ControlState
from classiq.interface.generator.expressions.expression import Expression
from classiq.interface.generator.function_params import NAME_REGEX
from classiq.interface.generator.functions import FunctionDeclaration
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)
from classiq.interface.generator.quantum_function_call import (
    BAD_CALL_NAME_ERROR_MSG,
    SUFFIX_MARKER,
    randomize_suffix,
)
from classiq.interface.helpers.custom_pydantic_types import PydanticNonEmptyString
from classiq.interface.model.handle_binding import (
    HandleBinding,
    SlicedHandleBinding,
    SubscriptHandleBinding,
)
from classiq.interface.model.quantum_function_declaration import (
    QuantumFunctionDeclaration,
    QuantumOperandDeclaration,
)
from classiq.interface.model.quantum_statement import QuantumOperation
from classiq.interface.model.validation_handle import get_unique_handle_names

from classiq.exceptions import ClassiqError, ClassiqValueError


def _validate_no_duplicated_ports(
    inputs: Mapping[str, HandleBinding],
    outputs: Mapping[str, HandleBinding],
    inouts: Mapping[str, HandleBinding],
) -> None:
    inputs_and_inouts = inputs.keys() & inouts.keys()
    if inputs_and_inouts:
        raise ClassiqValueError(
            f"{inputs_and_inouts} are used as ports in both inputs and inouts"
        )

    outputs_and_inouts = outputs.keys() & inouts.keys()
    if outputs_and_inouts:
        raise ClassiqValueError(
            f"{outputs_and_inouts} are used as ports in both outputs and inouts"
        )


def _validate_no_duplicated_handles(
    inputs: Mapping[str, HandleBinding],
    outputs: Mapping[str, HandleBinding],
    inouts: Mapping[str, HandleBinding],
) -> None:
    inputs_and_inouts = get_unique_handle_names(inputs) & get_unique_handle_names(
        inouts
    )
    if inputs_and_inouts:
        raise ClassiqValueError(
            f"{inputs_and_inouts} are used as handles in both inputs and inouts"
        )

    outputs_and_inouts = get_unique_handle_names(outputs) & get_unique_handle_names(
        inouts
    )
    if outputs_and_inouts:
        raise ClassiqValueError(
            f"{outputs_and_inouts} are used as handles in both outputs and inouts"
        )


def _validate_no_mixing_sliced_and_whole_handles(
    inouts: Mapping[str, HandleBinding],
) -> None:
    inout_handle_names_to_types = {
        handle_name: {type(handle) for handle in handles}
        for handle_name, handles in itertools.groupby(
            inouts.values(), lambda handle: handle.name
        )
    }
    invalid_handles = [
        handle
        for handle, types in inout_handle_names_to_types.items()
        if len(types) > 1
    ]
    if invalid_handles:
        raise ClassiqValueError(
            f"Inout handles {', '.join(invalid_handles)} mix sliced and whole handles"
        )


ArgValue = Union[Expression, "QuantumOperand", SlicedHandleBinding, HandleBinding]


class OperandIdentifier(BaseModel):
    name: str
    index: Expression


class QuantumFunctionCall(QuantumOperation):
    function: Union[str, OperandIdentifier] = pydantic.Field(
        description="The function that is called"
    )
    params: Dict[str, Expression] = pydantic.Field(default_factory=dict)
    strict_zero_ios: bool = pydantic.Field(
        default=True,
        description="Enables automated qubit allocation for pre-determined zero inputs "
        "and allows automated qubit release when performing inversion.\n"
        "Setting this flag to False exposes zero inputs and outputs as regular "
        "functional registers, and shifts the responsibility to the user to manually "
        "manage qubit allocation and release.",
    )
    release_by_inverse: bool = pydantic.Field(
        default=False, description="Release zero inputs in inverse call."
    )
    control_states: List[ControlState] = pydantic.Field(
        default_factory=list,
        description="Call the controlled function with the given controlled states.",
    )
    should_control: bool = pydantic.Field(
        default=True,
        description="False value indicates this call shouldn't be controlled even if the flow is controlled.",
    )
    inputs: Dict[str, HandleBinding] = pydantic.Field(
        default_factory=dict,
        description="A mapping from the input name to the wire it connects to",
    )
    inouts: Dict[
        str, Union[SlicedHandleBinding, SubscriptHandleBinding, HandleBinding]
    ] = pydantic.Field(
        default_factory=dict,
        description="A mapping from in/out name to the wires that connect to it",
    )
    outputs: Dict[str, HandleBinding] = pydantic.Field(
        default_factory=dict,
        description="A mapping from the output name to the wire it connects to",
    )
    name: PydanticNonEmptyString = pydantic.Field(
        default=None,
        description="The name of the function instance. "
        "If not set, determined automatically.",
    )
    operands: Dict[str, "QuantumOperand"] = pydantic.Field(
        description="Function calls passed to the operator",
        default_factory=dict,
    )
    positional_args: List[ArgValue] = pydantic.Field(default_factory=list)

    _func_decl: Optional[QuantumFunctionDeclaration] = pydantic.PrivateAttr(
        default=None
    )

    @property
    def func_decl(self) -> QuantumFunctionDeclaration:
        if self._func_decl is None:
            raise ClassiqError("Accessing an unresolved quantum function call")

        return self._func_decl

    def set_func_decl(self, fd: Optional[FunctionDeclaration]) -> None:
        if fd is not None and not isinstance(fd, QuantumFunctionDeclaration):
            raise ClassiqValueError(
                "the declaration of a quantum function call cannot be set to a non-quantum function declaration."
            )
        self._func_decl = fd

    @property
    def func_name(self) -> str:
        if isinstance(self.function, OperandIdentifier):
            return self.function.name
        return self.function

    @property
    def wiring_inputs(self) -> Mapping[str, HandleBinding]:
        return self.inputs

    @property
    def wiring_inouts(
        self,
    ) -> Mapping[
        str, Union[SlicedHandleBinding, SubscriptHandleBinding, HandleBinding]
    ]:
        return self.inouts

    @property
    def wiring_outputs(self) -> Mapping[str, HandleBinding]:
        return self.outputs

    def get_positional_args(self) -> List[ArgValue]:
        result: List[ArgValue] = self.positional_args
        if not result:
            result = list(self.params.values())
            result.extend(self.operands.values())
            result.extend(self.inputs.values())
            result.extend(self.inouts.values())
            result.extend(self.outputs.values())
        return result

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, QuantumFunctionCall) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    @pydantic.validator("name", pre=True, always=True)
    def _create_name(cls, name: Optional[str], values: Dict[str, Any]) -> str:
        """
        generates a name to a user defined-functions as follows:
        <function_name>_<SUFFIX_MARKER>_<random_suffix>
        """
        if name is not None:
            match = re.fullmatch(pattern=NAME_REGEX, string=name)
            if match is None:
                raise ValueError(BAD_CALL_NAME_ERROR_MSG)
            return name

        function = values.get("function")
        if isinstance(function, OperandIdentifier):
            function = function.name

        suffix = f"{SUFFIX_MARKER}_{randomize_suffix()}"
        if not function:
            return name if name else suffix
        return f"{function}_{suffix}"

    @property
    def pos_param_args(self) -> Dict[str, Expression]:
        return dict(
            zip(
                self.func_decl.param_decls.keys(),
                (
                    param
                    for param in self.positional_args
                    if isinstance(param, Expression)
                ),
            )
        )

    @property
    def pos_operand_args(self) -> Dict[str, "QuantumOperand"]:
        return dict(
            zip(
                self.func_decl.operand_declarations.keys(),
                (
                    param
                    for param in self.positional_args
                    if not isinstance(param, (Expression, HandleBinding))
                ),
            )
        )

    @property
    def pos_port_args(self) -> Dict[str, HandleBinding]:
        return dict(
            zip(
                self.func_decl.port_declarations.keys(),
                (
                    param
                    for param in self.positional_args
                    if isinstance(param, HandleBinding)
                ),
            )
        )

    def _update_pos_port_params(self) -> None:
        for name, port_decl in self.func_decl.port_declarations.items():
            if port_decl.direction == PortDeclarationDirection.Input:
                self.inputs[name] = self.pos_port_args[name]
            elif port_decl.direction == PortDeclarationDirection.Output:
                self.outputs[name] = self.pos_port_args[name]
            else:
                self.inouts[name] = self.pos_port_args[name]

    def _reduce_positional_args_to_keywords(self) -> None:
        self.params.update(self.pos_param_args)
        self.operands.update(self.pos_operand_args)
        self._update_pos_port_params()

    def resolve_function_decl(
        self,
        function_dict: Mapping[str, FunctionDeclaration],
    ) -> None:
        if self._func_decl is None:
            func_decl = function_dict.get(self.func_name)
            if func_decl is None:
                raise ClassiqValueError(
                    f"Error resolving function {self.func_name}, the function is not found in included library."
                )
            self.set_func_decl(func_decl)

        if self.positional_args:
            self._reduce_positional_args_to_keywords()

        _check_params_against_declaration(
            set(self.params.keys()),
            set(self.func_decl.param_decls.keys()),
            self.func_decl.name,
        )
        _check_ports_against_declaration(self, self.func_decl)
        _check_params_against_declaration(
            set(self.operands.keys()),
            set(self.func_decl.operand_declarations.keys()),
            self.func_name,
        )

        for name, op in self.operands.items():
            op_decl = self.func_decl.operand_declarations[name]
            for qlambda in get_lambda_defs(op):
                if isinstance(qlambda, QuantumLambdaFunction):
                    qlambda.set_op_decl(op_decl)

    @pydantic.validator("strict_zero_ios")
    def _validate_arithmetic_cannot_strict_zero_ios(
        cls, strict_zero_ios: bool, values: Dict[str, Any]
    ) -> bool:
        assert not (
            values.get("function") == Arithmetic.discriminator() and not strict_zero_ios
        ), "when using the Arithmetic function, assign to the expression result register via the target parameter instead of the strict_zero_ios flag"
        return strict_zero_ios

    @staticmethod
    def _has_repetitions(name_list: Sequence[str]) -> bool:
        return len(set(name_list)) < len(name_list)

    @pydantic.root_validator()
    def validate_handles(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        inputs = values.get("inputs", dict())
        outputs = values.get("outputs", dict())
        inouts = values.get("inouts", dict())

        _validate_no_duplicated_ports(inputs, outputs, inouts)
        _validate_no_duplicated_handles(inputs, outputs, inouts)
        _validate_no_mixing_sliced_and_whole_handles(inouts)

        return values


class QuantumLambdaFunction(BaseModel):
    """
    The definition of an anonymous function passed as operand to higher-level functions
    """

    rename_params: Dict[str, str] = pydantic.Field(
        default_factory=dict,
        description="Mapping of the declared param to the actual variable name used ",
    )

    body: List["QuantumFunctionCall"] = pydantic.Field(
        description="A list of function calls passed to the operator"
    )

    _func_decl: Optional[QuantumOperandDeclaration] = pydantic.PrivateAttr(default=None)

    @property
    def func_decl(self) -> Optional[QuantumOperandDeclaration]:
        return self._func_decl

    def set_op_decl(self, fd: QuantumOperandDeclaration) -> None:
        self._func_decl = fd


class LambdaListComprehension(BaseModel):
    """
    Specification of a list of lambda functions iteratively
    """

    count: Expression = pydantic.Field(
        description="The number of lambda functions in the list"
    )

    index_var: str = pydantic.Field(
        description="The name of the integer variable holding the iteration index"
    )

    func: QuantumLambdaFunction = pydantic.Field(
        description="A lambda function definition replicated for index values 0 to count-1"
    )


QuantumCallable = Union[str, QuantumLambdaFunction]
QuantumOperand = Union[QuantumCallable, List[QuantumCallable], LambdaListComprehension]

QuantumFunctionCall.update_forward_refs()


def get_lambda_defs(operand: QuantumOperand) -> List[QuantumCallable]:
    if isinstance(operand, list):
        return operand
    elif isinstance(operand, LambdaListComprehension):
        return [operand.func]
    else:
        return [operand]


def _check_ports_against_declaration(
    call: QuantumFunctionCall, decl: QuantumFunctionDeclaration
) -> None:
    call_input_names = set(call.inputs.keys()) | set(call.inouts.keys())

    _check_params_against_declaration(
        call_input_names,
        decl.input_set,
        call.func_name,
        should_validate_missing_params=False,
    )

    call_output_names = set(call.outputs.keys()) | set(call.inouts.keys())

    _check_params_against_declaration(
        call_output_names,
        decl.output_set,
        call.func_name,
        should_validate_missing_params=False,
    )

    inout_names = {
        port.name
        for port in decl.port_declarations.values()
        if port.direction == PortDeclarationDirection.Inout
    }
    inout_params = set(call.inouts.keys())

    _check_params_against_declaration(
        inout_params, inout_names, call.func_name, should_validate_missing_params=False
    )


def _check_params_against_declaration(
    call_params: Set[str],
    param_decls: Set[str],
    callee_name: str,
    should_validate_missing_params: bool = True,
) -> None:
    unknown_params = call_params - param_decls
    if unknown_params:
        raise ClassiqValueError(
            f"Unknown parameters {unknown_params} in call to {callee_name!r}."
        )

    missing_params = param_decls - call_params
    if should_validate_missing_params and missing_params:
        raise ClassiqValueError(
            f"Missing parameters {missing_params} in call to {callee_name!r}."
        )
