from dataclasses import dataclass
from typing import Any, Iterable, Optional

from numerous.sdk.models.input import (
    InputSource,
    InputVariable,
    get_input_sources_from_scenario_document,
)
from numerous.sdk.models.optimization import OptimizationConfiguration

from .component import Component, extract_components
from .job import Job
from .parameter import Parameter, get_parameters_dict


@dataclass
class Scenario:
    id: str
    name: str
    components: dict[str, Component]
    parameters: dict[str, Parameter]
    jobs: dict[str, Job]
    input_sources: list[InputSource]
    input_variables: list[InputVariable]
    optimization: Optional[OptimizationConfiguration] = None

    @staticmethod
    def from_document(
        data: dict[str, Any], optimization: Optional[OptimizationConfiguration] = None
    ) -> "Scenario":
        input_sources_mapping = get_input_sources_from_scenario_document(data)
        components = extract_components(data, input_sources_mapping)

        return Scenario(
            id=data["id"],
            name=data.get("scenarioName", ""),
            components=components,
            jobs={
                job_id: Job.from_document(job_id, job_data)
                for job_id, job_data in data.get("jobs", {}).items()
            },
            input_sources=list(input_sources_mapping.values()),
            input_variables=_collect_input_variables(components.values()),
            optimization=optimization,
            parameters=get_parameters_dict(data.get("parameters", [])),
        )


def _collect_input_variables(components: Iterable[Component]) -> list[InputVariable]:
    input_variables: list[InputVariable] = []
    for component in list(components):
        input_variables += list(component.input_variables.values())
        input_variables += _collect_input_variables(
            [
                subcomponent
                for subcomponent_category in component.components.values()
                for subcomponent in subcomponent_category
            ]
        )
    return input_variables
