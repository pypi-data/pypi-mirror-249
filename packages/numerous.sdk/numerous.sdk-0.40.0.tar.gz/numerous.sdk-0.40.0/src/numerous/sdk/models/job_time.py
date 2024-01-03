from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Generator, Optional, Union


class RunMode(Enum):
    CONTINUOUS = "continuous"
    DURATION = "duration"


@dataclass
class JobTime:
    """Contains information about the job runtime."""

    run_mode: RunMode
    start: datetime
    end: Optional[datetime]
    duration: Optional[timedelta]

    @staticmethod
    def from_document(job_data: dict[str, Any]) -> "JobTime":
        run_settings: dict[str, Any] = job_data["runSettings"]
        run_mode = RunMode(run_settings["runMode"])
        start = datetime.fromisoformat(run_settings["startDate"])
        end = (
            datetime.fromisoformat(run_settings["endDate"])
            if run_settings.get("endDate") is not None
            else None
        )
        return JobTime(
            run_mode=run_mode,
            start=start,
            end=end,
            duration=None if end is None else end - start,
        )

    def range(
        self, step: Union[timedelta, float] = 1.0, start: Optional[datetime] = None
    ) -> Generator[datetime, None, None]:
        """Range over the runtime of the job, from :attr:`start` to :attr:`end`,
        inclusive. If :attr:`end` is not defined, range forever.

        :param step: The step in time between yielded time value. If it is a `float` it
            is interpreted as seconds.
        :param start: If specified, it is used instead of the job start time.
        """
        step_ = step if isinstance(step, timedelta) else timedelta(seconds=step)
        t = start if start is not None else self.start
        while self.end is None or t < self.end:
            yield t
            t += step_
