import enum
import json
from dataclasses import dataclass
from typing import Any, Union


@dataclass
class Parameter:  # will be used as a base-class later for implementing specific functionality
    id: str
    uuid: str
    display_name: str
    type: str
    value: Any

    @staticmethod
    def from_document(data: dict[str, Any]) -> "Parameter":
        return Parameter(
            id=data["id"],
            uuid=data["uuid"],
            display_name=data["displayName"],
            type=data["type"],
            value=parse_value(data["value"], data["type"]),
        )


@dataclass
class FileReference:
    id: str
    path: str
    name: str

    @staticmethod
    def from_document(data: dict[str, Any]) -> "FileReference":
        return FileReference(data["id"], data["path"], data["name"])


class SimTimeUnit(enum.Enum):
    years = "years"
    months = "months"
    days = "days"
    hours = "hours"
    minutes = "minutes"
    seconds = "seconds"

    @classmethod
    def from_string(cls, value_str) -> "SimTimeUnit":
        for member in cls:
            if member.value == value_str:
                return member
        raise ValueError(f"No matching enum member for value: {value_str}")


@dataclass
class Currency:
    name: str
    code: str

    @staticmethod
    def from_document(data: dict[str, Any]) -> "Currency":
        return Currency(data["name"], data["code"])


@dataclass
class Month:
    value: int

    @staticmethod
    def from_document(data: dict[str, Any]) -> "Month":
        return Month(data["value"])


@dataclass
class MapLocation:
    id: str
    name: str
    center: tuple[float, float]

    @staticmethod
    def from_document(data: dict[str, Any]) -> "MapLocation":
        return MapLocation(data["id"], data["name"], data["center"])


@dataclass
class TimeValue:
    value: float
    unit: SimTimeUnit

    @staticmethod
    def from_document(data: dict[str, Any]) -> "TimeValue":
        return TimeValue(float(data["value"]), SimTimeUnit.from_string(data["unit"]))


@dataclass
class Config:
    value: str

    @staticmethod
    def from_document(data: dict[str, Any]) -> "Config":
        return Config(data["value"])


@dataclass
class Selector:
    value: Union[str, float, int]

    @staticmethod
    def from_document(data: dict[str, Any]) -> "Selector":
        return Selector(data["value"])


def parse_value(value: Any, type_: Any) -> Any:
    if type_ == "string":
        return value
    elif type_ == "number":
        return float(value)
    elif type_ == "boolean":
        return value
    elif type_ == "file":
        return FileReference.from_document(value)
    elif type_ == "json":
        return json.loads(value)
    elif type_ == "time_value":
        return TimeValue.from_document(value)
    elif type_ == "currency":
        return Currency.from_document(value)
    elif type_ == "month":
        return Month.from_document(value)
    elif type_ == "map":
        return MapLocation.from_document(value)
    elif type_ == "config":
        return Config.from_document(value)
    elif type_ == "selecter":
        return Selector.from_document(value)
    raise ValueError(f"Unkwnown parameter type: {type_}")


def get_parameters_dict(data: list[dict[str, Any]]) -> dict[str, Parameter]:
    return {param.id: param for param in get_parameters_list(data)}


def get_parameters_list(data: list[dict[str, Any]]) -> list[Parameter]:
    return [Parameter.from_document(param) for param in data]
