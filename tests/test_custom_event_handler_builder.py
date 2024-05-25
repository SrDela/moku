import pytest
from moku.lambda_function import CustomEventActionBuilder
from moku.lambda_function.exceptions import InvalidCustomEventAction


class TestCustomEventHandlerBuilder:

    def test_should_build_handler_correctly(self):
        fake_handler_action = lambda x: x
        fake_handler_name = "test"
        custom_handler = CustomEventActionBuilder.execute(fake_handler_action).on(fake_handler_name)

        assert fake_handler_name == custom_handler.name
        assert fake_handler_action == custom_handler.action

    def test_should_build_handler_with_instance(self):
        fake_handler_action = lambda x: x
        fake_handler_name = "test"
        custom_handler = CustomEventActionBuilder(fake_handler_action).on(fake_handler_name)

        assert fake_handler_name == custom_handler.name
        assert fake_handler_action == custom_handler.action

    def test_should_build_two_handlers_correctly(self):
        fake_handler_action = lambda x: x
        fake_handler_name = "test"
        custom_handler = CustomEventActionBuilder.execute(fake_handler_action).on(fake_handler_name)
        s_fake_handler_action = lambda y: y
        s_fake_handler_name = "other_test"
        s_custom_handler = CustomEventActionBuilder.execute(s_fake_handler_action).on(s_fake_handler_name)

        assert fake_handler_name == custom_handler.name
        assert fake_handler_action == custom_handler.action
        assert s_fake_handler_name == s_custom_handler.name
        assert s_fake_handler_action == s_custom_handler.action

    def test_should_raise_error_if_event_action_is_not_a_function(self):
        with pytest.raises(InvalidCustomEventAction):
            fake_handler_action = "not a function"
            fake_handler_name = "test"
            CustomEventActionBuilder.execute(fake_handler_action).on(fake_handler_name)
