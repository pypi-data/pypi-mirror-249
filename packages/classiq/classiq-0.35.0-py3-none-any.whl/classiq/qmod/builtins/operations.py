from classiq.interface.model.bind_operation import BindOperation

from classiq.qmod.qmod_variable import Input, Output, QVar
from classiq.qmod.quantum_callable import QCallable


def bind(source: Input[QVar], destination: Output[QVar]) -> None:
    assert QCallable.CURRENT_EXPANDABLE is not None
    QCallable.CURRENT_EXPANDABLE.append_statement_to_body(
        BindOperation(
            in_handle=source.get_handle_binding(),
            out_handle=destination.get_handle_binding(),
        )
    )


__all__ = [
    "bind",
]
