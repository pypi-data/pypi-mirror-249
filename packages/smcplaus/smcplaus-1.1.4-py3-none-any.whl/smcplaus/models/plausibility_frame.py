"""Module containing PlausibilityFrame class."""

from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple

import graphviz

from smcplaus.constants import ConfigKeys
from smcplaus.exceptions import ConfigError, IllDefinedStructureError
from smcplaus.models.state import State
from smcplaus.protocols.digraph_representable_structure import DigraphRepresentableStructure, StateToLabelMap
from smcplaus.protocols.json_serializable_structure import JSONSerializableStructure, StrDict

StateToAppearanceMap = Dict[State, Set[State]]

_PLAUSIBILITY_FRAME_KEYS: Tuple[str, str] = (ConfigKeys.DOMAIN.value, ConfigKeys.STATE_TO_APPEARANCE.value)


class PlausibilityFrame(JSONSerializableStructure, DigraphRepresentableStructure):
    """A plausibility frame specified by a domain and a mapping from states to appearances."""

    def __init__(self, domain: Set[State], state_to_appearance: StateToAppearanceMap, force_s4: bool = False) -> None:
        self._check_valid_state_to_appearance(domain, state_to_appearance)

        # Adding undefined states to mapping
        undefined_states = domain - set(state_to_appearance.keys())
        for undefined_state in undefined_states:
            state_to_appearance[undefined_state] = set()

        try:
            self._check_reflexive(state_to_appearance)
        except IllDefinedStructureError as err:
            if force_s4:
                state_to_appearance = self._make_reflexive(state_to_appearance)
            else:
                err.add_note("If you would like to add S4-closure, pass kwarg 'force_s4=True'")
                raise err

        try:
            self._check_transitive(state_to_appearance)
        except IllDefinedStructureError as err:
            if force_s4:
                state_to_appearance = self._make_transitive(state_to_appearance)
            else:
                err.add_note("If you would like to add S4-closure, pass kwarg 'force_s4=True'")
                raise err

        try:
            self._check_total(state_to_appearance)
        except IllDefinedStructureError as err:
            if force_s4:
                err.add_note("Even taking the S4-closure did not resolve this; please add more edges")
            else:
                err.add_note("Try taking the S4-closure by passing kwarg 'force_s4=True'")
            raise err

        self.domain = domain
        self.state_to_appearance = state_to_appearance

        return

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlausibilityFrame):
            return False
        return (self.domain, self.state_to_appearance) == (other.domain, other.state_to_appearance)

    def leq(self, state0: State, state1: State) -> bool:
        """Returns whether state1 is at least as plausible as state0 (i.e. state1 in the appearance of state0)."""
        return state1 in self.state_to_appearance[state0]

    def less_than(self, state0: State, state1: State) -> bool:
        """
        Returns whether state1 is strictly more plausible than state0 (i.e. state1 in the appearance of state0
        but state0 not in the appearance of state1).
        """
        return self.leq(state0, state1) and not self.leq(state1, state0)  # pylint: disable=W1114

    def best_of(self, subset: Set[State]) -> Set[State]:
        """Returns a set of all the maximal states of passed subset."""

        maximal_states: Set[State] = set()
        for state in subset:
            if all(self.leq(arb_state, state) for arb_state in subset):
                maximal_states.add(state)

        return maximal_states

    @staticmethod
    def _check_valid_state_to_appearance(domain: Set[State], state_to_appearance: StateToAppearanceMap) -> None:
        """
        Raises IllDefinedStructureError if passed state_to_appearance contains
        states that are not present in the passed domain.
        """

        domain_of_mapping: Set[State] = set()
        for state, appearance in state_to_appearance.items():
            domain_of_mapping.add(state)
            domain_of_mapping.update(appearance)

        invalid_states = domain_of_mapping - domain
        if len(invalid_states) != 0:
            raise IllDefinedStructureError(
                f"The following states are in the passed mapping 'state_to_appearance', "
                f"but not in the passed 'domain': {invalid_states}"
            )

        return

    @staticmethod
    def _check_reflexive(state_to_appearance: StateToAppearanceMap) -> None:
        """Raises IllDefinedStructureError if passed mapping is not reflexive."""

        non_reflexive_states_str = {
            str(state) for state in state_to_appearance.keys() if state not in state_to_appearance[state]
        }

        if non_reflexive_states_str:
            raise IllDefinedStructureError(
                f"The following states do not have reflexive edges: {non_reflexive_states_str}"
            )

        return

    @staticmethod
    def _check_transitive(state_to_appearance: StateToAppearanceMap) -> None:
        """Raises IllDefinedStructureError if passed mapping is not reflexive."""

        two_step_paths = PlausibilityFrame._get_two_step_paths(state_to_appearance)

        non_transitive_paths_str = {
            (str(s0), str(s1), str(s2)) for (s0, s1, s2) in two_step_paths if s2 not in state_to_appearance[s0]
        }

        if non_transitive_paths_str:
            raise IllDefinedStructureError(f"The following paths are not transitive: {non_transitive_paths_str}")

        return

    @staticmethod
    def _check_total(state_to_appearance: StateToAppearanceMap) -> None:
        """Raises IllDefinedStructureError if passed mapping is not reflexive."""

        # Splitting up states
        states = list(state_to_appearance.keys())
        half_num_states = len(states) // 2
        chunk0 = states[:half_num_states]
        chunk1 = states[half_num_states:]

        non_related_pairs_str: Set[Tuple[str, str]] = set()
        for state0 in chunk0:
            for state1 in chunk1:
                if state0 not in state_to_appearance[state1] and state1 not in state_to_appearance[state0]:
                    non_related_pairs_str.add((str(state0), str(state1)))

        if non_related_pairs_str:
            raise IllDefinedStructureError(f"The following pairs are not related: {non_related_pairs_str}")

        return

    @staticmethod
    def _make_reflexive(state_to_appearance: StateToAppearanceMap) -> StateToAppearanceMap:
        """Returns a reflexive version of the passed mapping."""
        return {state: appearance | {state} for state, appearance in state_to_appearance.items()}

    @staticmethod
    def _make_transitive(state_to_appearance: StateToAppearanceMap) -> StateToAppearanceMap:
        """Returns a transitive version of the passed mapping."""

        two_step_paths = PlausibilityFrame._get_two_step_paths(state_to_appearance)

        one_step_transitive_closure: StateToAppearanceMap = {
            state: appearance.copy() for state, appearance in state_to_appearance.items()
        }
        for s0, _, s2 in two_step_paths:
            one_step_transitive_closure[s0].add(s2)

        if state_to_appearance == one_step_transitive_closure:
            return one_step_transitive_closure
        else:
            return PlausibilityFrame._make_transitive(one_step_transitive_closure)

    @staticmethod
    def _get_two_step_paths(state_to_appearance: StateToAppearanceMap) -> Set[Tuple[State, State, State]]:
        """Returns a set of two-step paths in the passed mapping."""

        two_step_paths: Set[Tuple[State, State, State]] = set()
        for state0, appearance in state_to_appearance.items():
            for state1 in appearance:
                state1_appearance = state_to_appearance[state1]
                for state2 in state1_appearance:
                    two_step_paths.add((state0, state1, state2))

        return two_step_paths

    @classmethod
    def from_str_dict(cls, str_dict: Dict, force_s4: bool = False) -> PlausibilityFrame:
        """Returns instance of PlausibilityFrame loaded from passed str_dict."""

        correct_keys = set(_PLAUSIBILITY_FRAME_KEYS)
        if set(str_dict.keys()) != correct_keys:
            raise ConfigError(f"Passed config should have the following keys: {correct_keys!s}")

        domain = {State.from_str(state_str) for state_str in str_dict[ConfigKeys.DOMAIN.value]}
        state_to_appearance: StateToAppearanceMap = {}
        for state_str, appearance_list_str in str_dict[ConfigKeys.STATE_TO_APPEARANCE.value].items():
            state = State.from_str(state_str)
            appearance = {State.from_str(seen_state_str) for seen_state_str in appearance_list_str}
            state_to_appearance[state] = appearance
        instance = cls(domain=domain, state_to_appearance=state_to_appearance, force_s4=force_s4)

        return instance

    def to_str_dict(self) -> StrDict:
        """Returns a dictionary representing the current instance."""

        str_dict = {
            "domain": sorted([str(state) for state in self.domain]),
            "state_to_appearance": {
                str(state): sorted([str(seen_state) for seen_state in appearance])
                for state, appearance in self.state_to_appearance.items()
            },
        }

        return str_dict

    def get_clusters(self) -> List[Set[State]]:
        """Returns a list of clusters (i.e. subsets S of the domain where a <= b and b <= a for all a,b in S)."""

        clusters: List[Set[State]] = []
        for state in self.domain:
            # Searching for the cluster to which the state belongs
            for cluster in clusters:
                arbitrary_state_in_cluster = list(cluster)[0]
                if self.leq(state, arbitrary_state_in_cluster) and self.leq(arbitrary_state_in_cluster, state):
                    cluster.add(state)
                    break
            # The state belongs in a new cluster
            else:
                highest_cluster_that_is_leq_state: Optional[int] = None
                for i in range(len(clusters) - 1, -1, -1):
                    cluster = clusters[i]
                    arbitrary_state_in_cluster = list(cluster)[0]
                    if self.leq(arbitrary_state_in_cluster, state):
                        highest_cluster_that_is_leq_state = i
                        break

                new_cluster = {state}
                if highest_cluster_that_is_leq_state is None:
                    clusters.insert(0, new_cluster)
                else:
                    clusters.insert(highest_cluster_that_is_leq_state + 1, new_cluster)

        return clusters

    @property
    def state_to_label(self) -> StateToLabelMap:
        """Returns a map from state to digraph label."""
        return {state: str(state) for state in self.domain}

    def generate_digraph(self) -> graphviz.Digraph:
        """Returns a digraph of the passed instance."""
        return self.generate_labelled_digraph(state_to_label=self.state_to_label)

    def generate_labelled_digraph(self, state_to_label: StateToLabelMap) -> graphviz.Digraph:
        """Returns a digraph of the passed instance with passed labels."""

        # Initializing digraph
        digraph = graphviz.Digraph()

        # Adding nodes
        for state in sorted(self.domain, key=str):
            digraph.node(name=str(state), label=state_to_label[state])

        # Adding edges
        clusters = self.get_clusters()

        # Adding inter-cluster edges
        for cluster in clusters:
            for s0 in sorted(cluster, key=str):
                for s1 in sorted(cluster, key=str):
                    if s0 != s1:
                        digraph.edge(tail_name=str(s0), head_name=str(s1))

        # Adding edges to next cluster
        for i, cluster in enumerate(clusters[:-1]):
            cluster = clusters[i]
            next_cluster = clusters[i + 1]
            for s0 in sorted(cluster, key=str):
                for s2 in sorted(next_cluster, key=str):
                    digraph.edge(tail_name=str(s0), head_name=str(s2))

        return digraph
