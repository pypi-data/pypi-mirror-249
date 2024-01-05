"""Module containing JSONSerializableStructure class."""

import json
from typing import Any, Dict, Type, TypeVar

T = TypeVar("T", bound="JSONSerializableStructure")
StrDict = Dict[str, Any]


class JSONSerializableStructure:
    """Class to be inherited by structures that can be serialized to JSON format."""

    def __init__(self) -> None:
        raise NotImplementedError(
            f"Class '{self.__class__.__name__}' should not be instantiated directly; it should only be derived from"
        )

    @classmethod
    def from_str_dict(cls: Type[T], str_dict: Dict, **kwargs: Any) -> T:
        """Returns instance of cls loaded from passed str_dict."""
        raise NotImplementedError("Method 'from_str_dict' should be implemented by the inheriting class.")

    def to_str_dict(self) -> StrDict:
        """Returns a dictionary representing the current instance."""
        raise NotImplementedError("Method 'to_str_dict' should be implemented by the inheriting class.")

    @classmethod
    def from_json(cls: Type[T], json_str: str, **kwargs: Any) -> T:
        """Returns an instance of cls loaded from passed JSON str."""
        str_dict = json.loads(json_str)
        instance = cls.from_str_dict(str_dict, **kwargs)
        return instance

    def to_json(self) -> str:
        """Returns a JSON string representing the current instance."""

        json_str = json.dumps(
            obj=self.to_str_dict(),
            ensure_ascii=False,
            indent=4,
            default=str,
        )

        return json_str
