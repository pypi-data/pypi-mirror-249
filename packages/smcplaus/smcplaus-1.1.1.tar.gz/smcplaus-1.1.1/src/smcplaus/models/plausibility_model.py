"""Module containing (Pointed)PlausibilityModel class."""

from __future__ import annotations

from typing import Any, Dict, Set, Tuple

import graphviz

from smcplaus.constants import ConfigKeys
from smcplaus.exceptions import ConfigError, IllDefinedStructureError, SupposedlyUnreachableCaseError
from smcplaus.language.connectives import CONNECTIVE_TO_ARITY, Connectives
from smcplaus.language.formula import Formula
from smcplaus.language.propositional_variable import PropositionalVariable
from smcplaus.models.plausibility_frame import PlausibilityFrame, StateToAppearanceMap, StateToLabelMap
from smcplaus.models.state import State
from smcplaus.protocols.digraph_representable_structure import DigraphRepresentableStructure
from smcplaus.protocols.json_serializable_structure import JSONSerializableStructure, StrDict

StateToFactsMap = Dict[State, Set[PropositionalVariable]]

_PLAUSIBILITY_MODEL_KEYS: Tuple[str, str] = (ConfigKeys.FRAME.value, ConfigKeys.STATE_TO_FACTS.value)
_POINTED_PLAUSIBILITY_MODEL_KEYS: Tuple[str, str] = (ConfigKeys.MODEL.value, ConfigKeys.POINT.value)


class PlausibilityModel(JSONSerializableStructure, DigraphRepresentableStructure):
    """A plausibility frame with a valuation mapping from states to facts."""

    def __init__(self, frame: PlausibilityFrame, state_to_facts: StateToFactsMap) -> None:
        self._check_valid_state_to_facts(frame, state_to_facts)

        # Adding undefined states to mapping
        undefined_states = frame.domain - set(state_to_facts.keys())
        for undefined_state in undefined_states:
            state_to_facts[undefined_state] = set()

        self.frame = frame
        self.state_to_facts = state_to_facts

        return

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlausibilityModel):
            return False
        return (self.frame, self.state_to_facts) == (other.frame, other.state_to_facts)

    @staticmethod
    def _check_valid_state_to_facts(frame: PlausibilityFrame, state_to_facts: StateToFactsMap) -> None:
        """
        Raises IllDefinedStructureError if passed state_to_facts contains
        states that are not present in the domain of the passed frame.
        """

        invalid_states = set(state_to_facts.keys()) - frame.domain
        if len(invalid_states) != 0:
            raise IllDefinedStructureError(
                f"The following states are in the passed mapping 'state_to_facts', "
                f"but not in the domain of the passed 'frame': {invalid_states}"
            )

        return

    def truthset(self, formula: Formula) -> Set[State]:
        """Returns the set of states satisfying the passed formula."""
        return {state for state in self.frame.domain if PointedPlausibilityModel(self, state).satisfies(formula)}

    def update(self, formula: Formula) -> PlausibilityModel:
        """
        Returns a new instance of PlausibilityModel with all of the worlds not satisfying the passed formula removed.
        """

        # Constructing updated frame
        updated_domain = {
            state for state in self.frame.domain if PointedPlausibilityModel(model=self, point=state).satisfies(formula)
        }
        updated_state_to_appearance: StateToAppearanceMap = {}
        for state in updated_domain:
            updated_appearance = self.frame.state_to_appearance[state] & updated_domain
            updated_state_to_appearance[state] = updated_appearance
        updated_frame = PlausibilityFrame(domain=updated_domain, state_to_appearance=updated_state_to_appearance)

        # Updating fact map and constructing updated model
        updated_state_to_facts = {state: self.state_to_facts[state] for state in updated_domain}
        updated_model = PlausibilityModel(frame=updated_frame, state_to_facts=updated_state_to_facts)

        return updated_model

    def radical_upgrade(self, formula: Formula) -> PlausibilityModel:
        """
        Returns a new instance of PlausibilityModel with all of the worlds satisfying the passed formula strictly more
        plausible than the worlds that do not.
        """

        truthset = self.truthset(formula)
        falseset = self.frame.domain - truthset

        upgraded_state_to_appearance: StateToAppearanceMap = {}
        for state, appearance in self.frame.state_to_appearance.items():
            if state in truthset:
                upgraded_appearance = appearance - falseset
            else:
                upgraded_appearance = appearance | truthset
            upgraded_state_to_appearance[state] = upgraded_appearance

        upgraded_frame = PlausibilityFrame(domain=self.frame.domain, state_to_appearance=upgraded_state_to_appearance)
        upgraded_model = PlausibilityModel(frame=upgraded_frame, state_to_facts=self.state_to_facts)

        return upgraded_model

    def conservative_upgrade(self, formula: Formula) -> PlausibilityModel:
        """
        Returns a new instance of PlausibilityModel with the best worlds satisfying the passed formula strictly more
        plausible than the worlds that do not.
        """

        truthset = self.truthset(formula)
        best_of_truthset = self.frame.best_of(truthset)

        upgraded_state_to_appearance: StateToAppearanceMap = {}
        for state, appearance in self.frame.state_to_appearance.items():
            if state in best_of_truthset:
                upgraded_appearance = appearance & best_of_truthset
            else:
                upgraded_appearance = appearance | best_of_truthset
            upgraded_state_to_appearance[state] = upgraded_appearance

        upgraded_frame = PlausibilityFrame(domain=self.frame.domain, state_to_appearance=upgraded_state_to_appearance)
        upgraded_model = PlausibilityModel(frame=upgraded_frame, state_to_facts=self.state_to_facts)

        return upgraded_model

    @classmethod
    def from_str_dict(cls, str_dict: Dict, **kwargs: Any) -> PlausibilityModel:
        """Returns instance of PlausibilityModel loaded from passed str_dict."""

        correct_keys = set(_PLAUSIBILITY_MODEL_KEYS)
        if set(str_dict.keys()) != correct_keys:
            raise ConfigError(f"Passed config should have the following keys: {correct_keys!s}")

        frame = PlausibilityFrame.from_str_dict(
            str_dict[ConfigKeys.FRAME.value], force_s4=kwargs.get("force_s4", False)
        )
        state_to_facts: StateToFactsMap = {}
        for state_str, facts_list_str in str_dict[ConfigKeys.STATE_TO_FACTS.value].items():
            state = State.from_str(state_str)
            facts = {PropositionalVariable.from_str(fact_str) for fact_str in facts_list_str}
            state_to_facts[state] = facts
        instance = cls(frame=frame, state_to_facts=state_to_facts)

        return instance

    def to_str_dict(self) -> StrDict:
        """Returns a dictionary representing the current instance."""

        str_dict = {
            "frame": self.frame.to_str_dict(),
            "state_to_facts": {
                str(state): sorted([str(fact) for fact in facts]) for state, facts in self.state_to_facts.items()
            },
        }

        return str_dict

    @property
    def state_to_label(self) -> StateToLabelMap:
        """Returns a map from state to digraph label."""

        state_to_label: StateToLabelMap = {}
        for state in self.frame.domain:
            facts_str = {str(var) for var in self.state_to_facts[state]}
            if facts_str != set():
                var_str = str.join(", ", sorted(facts_str))
                label = f"{state!s} || {var_str}"
            else:
                label = str(state)
            state_to_label[state] = label

        return state_to_label

    def generate_digraph(self) -> graphviz.Digraph:
        """Returns a digraph of the passed instance."""
        return self.frame.generate_labelled_digraph(state_to_label=self.state_to_label)


class PointedPlausibilityModel(JSONSerializableStructure, DigraphRepresentableStructure):
    """A plausibility model with a specified point."""

    def __init__(self, model: PlausibilityModel, point: State) -> None:
        self.model = model

        if point not in model.frame.domain:
            raise IllDefinedStructureError(
                f"The point '{point}' does not exist in the passed model: {model.frame.domain} "
            )
        self.point = point

        return

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PointedPlausibilityModel):
            return False
        return (self.model, self.point) == (other.model, other.point)

    def satisfies(self, formula: Formula) -> bool:  # pylint: disable=R0911,R0912,R0914
        """Returns whether the passed formula is satisfied by the current PointedPlausibilityModel."""

        # Propositional variables
        if isinstance(formula.node, PropositionalVariable):
            return formula.node in self.model.state_to_facts[self.point]

        # Complex formulas
        if CONNECTIVE_TO_ARITY[formula.node] == 0:
            if formula.node is Connectives.BOT:
                return False
            elif formula.node is Connectives.TOP:
                return True
            else:
                raise SupposedlyUnreachableCaseError(local_namespace=locals())
        elif CONNECTIVE_TO_ARITY[formula.node] == 1:
            subf = formula.subformulas[0]  # type: ignore
            if formula.node is Connectives.BELIEF:
                best_states = self.model.frame.best_of(self.model.frame.domain)
                return best_states <= self.model.truthset(subf)
            elif formula.node is Connectives.BOX:
                appearance = self.model.frame.state_to_appearance[self.point]
                return appearance <= self.model.truthset(subf)
            elif formula.node is Connectives.DIAMOND:
                appearance = self.model.frame.state_to_appearance[self.point]
                return (appearance & self.model.truthset(subf)) != set()
            elif formula.node is Connectives.KNOWLEDGE:
                return self.model.frame.domain <= self.model.truthset(subf)
            elif formula.node is Connectives.NOT:
                return not self.satisfies(subf)
            elif formula.node is Connectives.STRONG_BELIEF:
                truthset = self.model.truthset(subf)
                falseset = self.model.frame.domain - self.model.truthset(subf)
                truthset_nonempty = len(truthset) != 0
                truthset_preferred = True
                for true_state in truthset:
                    for false_state in falseset:
                        if not self.model.frame.less_than(false_state, true_state):
                            truthset_preferred = False
                            break
                    if truthset_preferred is False:
                        break
                return truthset_nonempty and truthset_preferred
            else:
                raise SupposedlyUnreachableCaseError(local_namespace=locals())
        elif CONNECTIVE_TO_ARITY[formula.node] == 2:
            subf0, subf1 = formula.subformulas[0], formula.subformulas[1]  # type: ignore
            if formula.node is Connectives.AND:
                return self.satisfies(subf0) and self.satisfies(subf1)
            elif formula.node is Connectives.CONDITIONAL_BELIEF:
                best_of_truthset = self.model.frame.best_of(self.model.truthset(subf0))
                return best_of_truthset <= self.model.truthset(subf0)
            elif formula.node is Connectives.CONSERVATIVE_UPGRADE:
                upgraded_model = self.model.conservative_upgrade(subf0)
                return PointedPlausibilityModel(model=upgraded_model, point=self.point).satisfies(subf1)
            elif formula.node is Connectives.IMPLIES:
                return (not self.satisfies(subf0)) or self.satisfies(subf1)
            elif formula.node is Connectives.OR:
                return self.satisfies(subf0) or self.satisfies(subf1)
            elif formula.node is Connectives.RADICAL_UPGRADE:
                upgraded_model = self.model.radical_upgrade(subf0)
                return PointedPlausibilityModel(model=upgraded_model, point=self.point).satisfies(subf1)
            elif formula.node is Connectives.UPDATE:
                subf0, subf1 = formula.subformulas[0], formula.subformulas[1]  # type: ignore
                if not self.satisfies(subf0):
                    return True
                updated_model = self.model.update(subf0)
                return PointedPlausibilityModel(model=updated_model, point=self.point).satisfies(subf1)
            else:
                raise SupposedlyUnreachableCaseError(local_namespace=locals())
        else:
            raise SupposedlyUnreachableCaseError(local_namespace=locals())

    @classmethod
    def from_str_dict(cls, str_dict: Dict, **kwargs: Any) -> PointedPlausibilityModel:
        """Returns instance of PointedPlausibilityModel loaded from passed str_dict."""

        correct_keys = set(_POINTED_PLAUSIBILITY_MODEL_KEYS)
        if set(str_dict.keys()) != correct_keys:
            raise ConfigError(f"Passed config should have the following keys: {correct_keys!s}")

        model = PlausibilityModel.from_str_dict(
            str_dict[ConfigKeys.MODEL.value], force_s4=kwargs.get("force_s4", False)
        )
        point = State.from_str(str_dict[ConfigKeys.POINT.value])
        instance = cls(model=model, point=point)

        return instance

    def to_str_dict(self) -> StrDict:
        """Returns a dictionary representing the current instance."""

        str_dict = {
            "model": self.model.to_str_dict(),
            "point": str(self.point),
        }

        return str_dict

    @property
    def state_to_label(self) -> StateToLabelMap:
        """Returns a map from state to digraph label."""

        state_to_label = self.model.state_to_label.copy()
        point_label = state_to_label[self.point]
        state_to_label[self.point] = f"*{point_label}"

        return state_to_label

    def generate_digraph(self) -> graphviz.Digraph:
        """Returns a digraph of the passed instance."""
        return self.model.frame.generate_labelled_digraph(state_to_label=self.state_to_label)
