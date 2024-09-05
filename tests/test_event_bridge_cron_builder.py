import pytest
from moku.event_bridge import EventBridgeRule, EventBridgeRuleDetail, CronBuilder
from moku.event_bridge.exceptions import EventBridgeRuleException


class TestEventBridgeCronBuilder:

    def test_should_build_rule_correctly(self):
        event_name = "some.event"
        action = lambda x: print(x)
        event = CronBuilder.link(action).to(event_name)
        assert EventBridgeRule(
            detail=EventBridgeRuleDetail(action=event_name),
            action=action
        ) == event

    def test_should_build_rule_directly_with_instance(self):
        event_name = "some.event"
        action = lambda x: print(x)
        event = CronBuilder(action).to(event_name)
        assert EventBridgeRule(
            detail=EventBridgeRuleDetail(action=event_name),
            action=action
        ) == event

    def test_should_raise_exception_when_action_is_not_defined(self):
        with pytest.raises(EventBridgeRuleException):
            CronBuilder().to(lambda x: print(x))
