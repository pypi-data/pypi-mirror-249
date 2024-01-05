"""Module containing Connectives enum."""

from enum import Enum, auto
from typing import Dict


class Connectives(Enum):
    """Enumeration of language connectives."""

    AND = auto()
    BELIEF = auto()
    BOT = auto()
    BOX = auto()
    CONDITIONAL_BELIEF = auto()
    CONSERVATIVE_UPGRADE = auto()
    DIAMOND = auto()
    IMPLIES = auto()
    KNOWLEDGE = auto()
    NOT = auto()
    OR = auto()
    RADICAL_UPGRADE = auto()
    STRONG_BELIEF = auto()
    TOP = auto()
    UPDATE = auto()


CONNECTIVE_TO_ARITY: Dict[Connectives, int] = {
    Connectives.BOT: 0,
    Connectives.TOP: 0,
    Connectives.BELIEF: 1,
    Connectives.BOX: 1,
    Connectives.DIAMOND: 1,
    Connectives.KNOWLEDGE: 1,
    Connectives.NOT: 1,
    Connectives.STRONG_BELIEF: 1,
    Connectives.AND: 2,
    Connectives.CONDITIONAL_BELIEF: 2,
    Connectives.CONSERVATIVE_UPGRADE: 2,
    Connectives.IMPLIES: 2,
    Connectives.OR: 2,
    Connectives.RADICAL_UPGRADE: 2,
    Connectives.UPDATE: 2,
}
