"""Module containing Formula class."""

from __future__ import annotations

from typing import Optional, Tuple

from smcplaus.exceptions import IllDefinedFormulaError, SupposedlyUnreachableCaseError
from smcplaus.language.connectives import CONNECTIVE_TO_ARITY, Connectives
from smcplaus.language.propositional_variable import PropositionalVariable


class Formula:
    """
    A formula in our language represented as a tree-like structure with either PropositionalVariable's or Connectives
    for nodes and either None or List[Formula] for subformulas (i.e. branches).
    """

    def __init__(self, node: (PropositionalVariable | Connectives), subformulas: Optional[Tuple[Formula, ...]]) -> None:
        if isinstance(node, PropositionalVariable):
            if subformulas is not None:
                raise IllDefinedFormulaError(
                    f"Propositional variables do not have subformulas but {len(subformulas)} passed: {subformulas}"
                )
            self.node = node
            self.subformulas = None
        elif isinstance(node, Connectives):
            correct_num_subformulas = CONNECTIVE_TO_ARITY[node]
            if subformulas is None:
                raise IllDefinedFormulaError(
                    f"Connective '{node}' takes {correct_num_subformulas} formulas but '{None}' was passed; "
                    f"if '{node}' is 0-ary, pass the empty list '{[]}'"
                )
            if len(subformulas) != correct_num_subformulas:
                raise IllDefinedFormulaError(
                    f"Connective '{node.name}' takes {correct_num_subformulas} subformulas "
                    f"but {len(subformulas)} were passed"
                )
            self.node = node  # type: ignore
            self.subformulas = subformulas  # type: ignore
        else:
            raise TypeError(
                f"Argument 'node' must be of type '{PropositionalVariable}' or '{Connectives}' not '{type(node)}'"
            )

        return

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Formula):
            return False
        return (self.node, self.subformulas) == (other.node, other.subformulas)

    def __str__(self) -> str:  # pylint: disable=R0911,R0912  # pragma: no cover
        if isinstance(self.node, PropositionalVariable):
            return str(self.node)
        elif CONNECTIVE_TO_ARITY[self.node] == 0:
            if self.node is Connectives.TOP:
                return "T"
            elif self.node is Connectives.BOT:
                return "F"
            else:
                raise SupposedlyUnreachableCaseError(local_namespace=locals())
        elif CONNECTIVE_TO_ARITY[self.node] == 1:
            subf = self.subformulas[0]  # type: ignore
            if self.node is Connectives.BELIEF:
                return f"(B{subf!s})"
            elif self.node is Connectives.BOX:
                return f"([]{subf!s})"
            elif self.node is Connectives.DIAMOND:
                return f"(<>{subf!s})"
            elif self.node is Connectives.KNOWLEDGE:
                return f"(K{subf!s})"
            elif self.node is Connectives.NOT:
                return f"(~{subf!s})"
            elif self.node is Connectives.STRONG_BELIEF:
                return f"(S{subf!s})"
            else:
                raise SupposedlyUnreachableCaseError(local_namespace=locals())
        elif CONNECTIVE_TO_ARITY[self.node] == 2:
            subf0, subf1 = self.subformulas  # type: ignore
            if self.node is Connectives.AND:
                return f"({subf0!s} && {subf1!s})"
            elif self.node is Connectives.CONDITIONAL_BELIEF:
                return f"(C{subf0!s}{subf1!s})"
            elif self.node is Connectives.CONSERVATIVE_UPGRADE:
                return f"([^{subf0!s}]{subf1!s})"
            elif self.node is Connectives.IMPLIES:
                return f"({subf0!s} -> {subf1!s})"
            elif self.node is Connectives.OR:
                return f"({subf0!s} || {subf1!s})"
            elif self.node is Connectives.RADICAL_UPGRADE:
                return f"([${subf0!s}]{subf1!s})"
            elif self.node is Connectives.UPDATE:
                return f"([!{subf0!s}]{subf1!s})"
            else:
                raise SupposedlyUnreachableCaseError(local_namespace=locals())
        else:
            raise SupposedlyUnreachableCaseError(local_namespace=locals())
