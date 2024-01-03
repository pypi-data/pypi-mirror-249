import signal
from typing import Any, Callable, Optional

from numerous.sdk.connect.job_state import JobState


class HibernationHandler:
    def __init__(
        self, state_getter: Callable[[], JobState], last_read_key_setter: Callable
    ) -> None:
        self.hibernating = False
        self._state_getter = state_getter
        self._last_read_key_setter = last_read_key_setter
        self.callback: Optional[Callable[[], Any]] = None

    def hibernate(self) -> None:
        self.hibernating = True
        if self.callback is not None:
            self.callback()
        self._state_getter().commit()
        self._last_read_key_setter()
        signal.raise_signal(signal.SIGTERM)
