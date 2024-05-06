from __future__ import annotations
from typing import Optional
from ._typing import EventAction
from .exceptions import S3EventException
from ._default_event import DefaultS3Event


class S3EventBuilder:

    def __init__(self, event_name: Optional[str] = None) -> None:
        self.__event_name: Optional[str] = event_name

    @staticmethod
    def on(event_name: str) -> S3EventBuilder:
        return S3EventBuilder(event_name)

    def do(self, action: EventAction) -> DefaultS3Event:
        if self.__event_name is None:
            raise S3EventException("Must define first the event name using the 'on' method.")
        return DefaultS3Event(name=self.__event_name, action=action)
