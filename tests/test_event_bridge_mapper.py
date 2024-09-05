import pytest
from collections.abc import Callable
from moku.event_bridge import EventBridgeRule, EventBridgeRuleDetail, EventBridgeMapper
from moku.event_bridge.exceptions import EventBridgeRuleException


class TestEventBridgeMapper:

    func: Callable[[any], any] = lambda x: x
    func2: Callable[[any], str] = lambda x: str(x)

    def test_should_add_rule_and_resolve_correctly(self):
        event_name: str = "fake.event"
        rule: EventBridgeRule = EventBridgeRule(
            detail=EventBridgeRuleDetail(action=event_name),
            action=self.func
        )
        mapper = EventBridgeMapper()
        mapper.add_rule(rule)
        action = mapper.resolve(event_name)

        assert self.func == action

    def test_should_overwrite_rule_and_resolve_correctly(self):
        event_name: str = "fake.event"
        rule: EventBridgeRule = EventBridgeRule(
            detail=EventBridgeRuleDetail(action=event_name),
            action=self.func
        )
        rule2: EventBridgeRule = EventBridgeRule(
            detail=EventBridgeRuleDetail(action=event_name),
            action=self.func2
        )
        mapper = EventBridgeMapper()
        mapper.add_rule(rule)
        mapper.add_rule(rule2)
        action = mapper.resolve(event_name)

        assert self.func2 == action

    def test_should_raise_error_if_rule_is_not_mapped(self):
        event_name: str = "fake.event"
        rule: EventBridgeRule =  EventBridgeRule(
            detail=EventBridgeRuleDetail(action=event_name),
            action=self.func
        )
        mapper = EventBridgeMapper()
        mapper.add_rule(rule)

        with pytest.raises(EventBridgeRuleException):
            mapper.resolve("other.event")
