"""Constants accessed by entire package."""

from enum import StrEnum


class ConfigKeys(StrEnum):
    """Enumeration of keys used in configs to be loaded by structures."""

    DOMAIN = "domain"
    FRAME = "frame"
    MODEL = "model"
    POINT = "point"
    STATE_TO_APPEARANCE = "state_to_appearance"
    STATE_TO_FACTS = "state_to_facts"
