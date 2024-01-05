"""Module containing DigraphRepresentableStructure class."""

from pathlib import Path
from typing import Dict

import graphviz

from smcplaus.models.state import State

StateToLabelMap = Dict[State, str]


class DigraphRepresentableStructure:
    """Class to be inherited by structures that can be represented by a digraph."""

    @property
    def state_to_label(self) -> StateToLabelMap:
        """Returns a map from state to digraph label."""
        raise NotImplementedError("Method 'state_to_label' should be implemented by the inheriting class.")

    def generate_digraph(self) -> graphviz.Digraph:
        """Returns a digraph of the passed instance."""
        raise NotImplementedError("Method 'generate_digraph' should be implemented by the inheriting class.")

    def dump_digraph(self, filepath: Path) -> None:
        """Dumps digraph of passed instance to passed filepath."""

        digraph = self.generate_digraph()

        filepath.write_text(digraph.source, encoding="utf8")

        return
