"""Custom exceptions accessed by entire package."""

from typing import Dict


class IllDefinedFormulaError(Exception):
    """Raise when a formula is not well-defined."""


class IllDefinedStructureError(Exception):
    """Raise when a structure is not well-defined."""


class SupposedlyUnreachableCaseError(Exception):
    """Raise when a structure is not well-defined."""

    def __init__(self, local_namespace: Dict) -> None:
        super().__init__(f"It should be impossible to reach this case: {local_namespace}")


class ConfigError(Exception):
    """Raise when a passed config does not meet specifications."""
