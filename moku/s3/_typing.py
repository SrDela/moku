from typing_extensions import Protocol


class EventAction(Protocol):
    def __call__(event: dict) -> dict: ...
