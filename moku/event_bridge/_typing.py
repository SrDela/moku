from dataclasses import dataclass
from typing import Any, Dict
from collections.abc import Callable


EventBridgeRuleAction = Callable[[Dict[str, Any]], Any]


@dataclass
class EventBridgeRuleDetail:
    action: str


@dataclass
class EventBridgeRule:
    detail: EventBridgeRuleDetail
    action: EventBridgeRuleAction
