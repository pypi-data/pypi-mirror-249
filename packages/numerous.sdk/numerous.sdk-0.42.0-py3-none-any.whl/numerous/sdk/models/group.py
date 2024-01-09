from dataclasses import dataclass
from typing import Any

from .parameter import Parameter, get_parameters_dict


@dataclass
class Group:
    id: str
    name: str
    parameters: dict[str, Parameter]

    @staticmethod
    def from_document(data: dict[str, Any]) -> "Group":
        return Group(
            id=data["id"],
            name=data.get("groupName", ""),
            parameters=get_parameters_dict(data.get("parameters", [])),
        )
