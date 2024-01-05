"""Module containing State class."""

from __future__ import annotations

import re

from smcplaus.exceptions import ConfigError, IllDefinedStructureError

_STATE_RE = re.compile(r"s(\d+)")


class State:
    """A state indexed by an integer."""

    def __init__(self, index: int) -> None:
        # Validating passed args
        if not isinstance(index, int) or index < 0:
            raise IllDefinedStructureError(f"Argument 'index' must be a positive integer; '{index}' not allowed")

        self.index = index

        return

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return False
        return self.index == other.index

    def __hash__(self) -> int:
        return hash((State, self.index))

    def __repr__(self) -> str:
        return f"State({self.index})"

    def __str__(self) -> str:
        return f"s{self.index}"

    @classmethod
    def from_str(cls, state_str: str) -> State:
        """Returns instance of State loaded from passed str."""

        fullmatch = _STATE_RE.fullmatch(state_str)

        if not fullmatch:
            raise ConfigError(f"Passed state '{state_str}' is not of form '{_STATE_RE.pattern}' (eg. s15)")

        index = int(fullmatch.group(1))
        instance = cls(index=index)

        return instance
