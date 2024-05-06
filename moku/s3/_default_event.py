from ._typing import EventAction
from dataclasses import dataclass


@dataclass
class DefaultS3Event:
    name: str
    action: EventAction

    def __eq__(self, __o: object) -> bool:

        if isinstance(__o, DefaultS3Event):
            if self.name == __o.name and self.action == __o.action:
                return True

        return False
