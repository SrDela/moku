from moku._interfaces.event_handler import EventHandler
from . import _typing


class LambdaFunction:

    def __init__(self) -> None:
        self.__trigger_map: _typing.TriggerMap = {}

    def add_trigger(self, trigger: EventHandler) -> None:
        self.__trigger_map[trigger.event_source] = trigger

    def resolve(self, *args: any, **kwargs: any) -> None:
        return
