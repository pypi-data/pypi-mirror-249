"""Jobs represent the things that run on the numerous platform,
including the context in which code using the SDK is running.

This module contains the definition of :class:`Job` and the implementation
of its instances' creation.
"""

from dataclasses import dataclass
from typing import Any

from numerous.sdk.models.job_time import JobTime
from numerous.sdk.models.parameter import Parameter, get_parameters_dict


@dataclass
class Job:
    """A job in a :class:`numerous.sdk.models.scenario.Scenario`"""

    id: str
    name: str
    is_main: bool
    parameters: dict[str, Parameter]
    time: JobTime

    @staticmethod
    def from_document(job_id: str, data: dict[str, Any]) -> "Job":
        return Job(
            id=job_id,
            name=data.get("name", ""),
            is_main=data.get("isMain", False),
            parameters=get_parameters_dict(data.get("image", {}).get("parameters", [])),
            time=JobTime.from_document(data),
        )
