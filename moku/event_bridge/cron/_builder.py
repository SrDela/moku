from __future__ import annotations
from typing import Optional

from .. import _typing
from ..exceptions import EventBridgeRuleException


class CronBuilder:

    def __init__(self, action: Optional[_typing.EventBridgeRuleAction] = None) -> None:
        self.__action: Optional[_typing.EventBridgeRuleAction] = action

    @staticmethod
    def link(action: _typing.EventBridgeRuleAction) -> CronBuilder:
        return CronBuilder(action)

    def to(self, event_name: str) -> _typing.EventBridgeRule:
        if self.__action is None:
            raise EventBridgeRuleException("Cron action is not defined.")

        return _typing.EventBridgeRule(
            detail=_typing.EventBridgeRuleDetail(action=event_name),
            action=self.__action
        )
