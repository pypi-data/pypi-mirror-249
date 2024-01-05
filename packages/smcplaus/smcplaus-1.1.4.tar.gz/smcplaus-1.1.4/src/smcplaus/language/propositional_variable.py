"""Module containing PropositionalVariable class."""

from __future__ import annotations

import re
import string
from typing import Optional

from smcplaus.exceptions import ConfigError, IllDefinedFormulaError

_LETTERS = tuple(string.ascii_lowercase)
_PROPOSITIONAL_VARIABLE_RE = re.compile(r"([a-z])(\d)*")


class PropositionalVariable:
    """A propositional variable indexed by an integer."""

    def __init__(self, letter: str, index: Optional[int] = None) -> None:
        # Validating passed args
        if letter not in _LETTERS:
            raise IllDefinedFormulaError(
                f"Argument 'letter' must be a lowercase ASCII character; '{letter}' not allowed"
            )
        if index is not None and (not isinstance(index, int) or index < 0):
            raise IllDefinedFormulaError(f"Argument 'index' must be a positive integer; '{index}' not allowed")

        self.letter = letter
        self.index = index

        return

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PropositionalVariable):
            return False
        return (self.letter, self.index) == (other.letter, other.index)

    def __hash__(self) -> int:
        return hash((PropositionalVariable, self.letter, self.index))

    def __repr__(self) -> str:
        return f"PropositionalVariable({self!s})"

    def __str__(self) -> str:
        return f"{self.letter}{self.index}" if self.index is not None else self.letter

    @classmethod
    def from_str(cls, var_str: str) -> PropositionalVariable:
        """Returns instance of PropositionalVariable loaded from passed str."""

        fullmatch = _PROPOSITIONAL_VARIABLE_RE.fullmatch(var_str)

        if not fullmatch:
            raise ConfigError(
                f"Passed propositional variable '{var_str}' is not "
                f"of form '{_PROPOSITIONAL_VARIABLE_RE.pattern}' (eg. 'm15')"
            )

        letter = fullmatch.group(1)
        if letter == "s":
            raise ConfigError(
                f"The letter 's' (in passed string '{var_str}') cannot be used because it is reserved for State's."
            )
        if fullmatch.group(2) is None:
            index = None
        else:
            index = int(fullmatch.group(2))
        instance = cls(letter=letter, index=index)

        return instance
