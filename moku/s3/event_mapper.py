from typing import Dict

from moku._interfaces.event_handler import EventHandler

from ._typing import EventAction
from ._default_event import DefaultS3Event
from .exceptions import S3EventException


class S3EventMapper(EventHandler):

    def __init__(self) -> None:
        self.__event_map: Dict[str, EventAction] = {}

    def add_event(self, event: DefaultS3Event) -> None:
        self.__event_map[event.name] = event.action

    def resolve(self, event_name: str) -> EventAction:
        action = self.__event_map.get(event_name)
        if action is None:
            raise S3EventException("Unmapped event.")
        return action
