from typing import Dict

from moku._interfaces.event_handler import EventHandler

from . import _typing
from .exceptions import EventBridgeRuleException


class EventBridgeMapper(EventHandler):

    def __init__(self) -> None:
        self.__event_map: Dict[str, _typing.EventBridgeRuleAction] = {}

    def add_rule(self, rule: _typing.EventBridgeRule) -> None:
        self.__event_map[rule.detail.action] = rule.action

    def resolve(self, event_name: str) -> _typing.EventBridgeRuleAction:
        action = self.__event_map.get(event_name)
        if action is None:
            raise EventBridgeRuleException("Unmapped rule.")
        return action
