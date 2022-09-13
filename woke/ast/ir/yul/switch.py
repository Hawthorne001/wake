from __future__ import annotations

from typing import TYPE_CHECKING, Iterator, List, Tuple, Union

from woke.ast.ir.utils import IrInitTuple
from woke.ast.ir.yul.abc import YulAbc
from woke.ast.ir.yul.case_statement import Case
from woke.ast.ir.yul.function_call import FunctionCall
from woke.ast.ir.yul.identifier import Identifier
from woke.ast.ir.yul.literal import Literal
from woke.ast.nodes import YulFunctionCall, YulIdentifier, YulLiteral, YulSwitch

if TYPE_CHECKING:
    from .block import Block


class Switch(YulAbc):
    """
    TBD
    """
    _parent: Block
    __cases: List[Case]
    __expression: Union[FunctionCall, Identifier, Literal]

    def __init__(self, init: IrInitTuple, switch: YulSwitch, parent: YulAbc):
        super().__init__(init, switch, parent)
        if isinstance(switch.expression, YulFunctionCall):
            self.__expression = FunctionCall(init, switch.expression, self)
        elif isinstance(switch.expression, YulIdentifier):
            self.__expression = Identifier(init, switch.expression, self)
        elif isinstance(switch.expression, YulLiteral):
            self.__expression = Literal(init, switch.expression, self)
        else:
            assert False, f"Unexpected type: {type(switch.expression)}"
        self.__cases = [Case(init, case, self) for case in switch.cases]

    def __iter__(self) -> Iterator[YulAbc]:
        yield self
        yield from self.__expression
        for case_ in self.__cases:
            yield from case_

    @property
    def parent(self) -> Block:
        return self._parent

    @property
    def cases(self) -> Tuple[Case]:
        return tuple(self.__cases)

    @property
    def expression(self) -> Union[FunctionCall, Identifier, Literal]:
        return self.__expression
