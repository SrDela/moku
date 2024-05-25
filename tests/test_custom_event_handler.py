import pytest
from moku.lambda_function import CustomEventActionBuilder, CustomEventHandler
from moku.lambda_function.exceptions import InvalidCustomEventError, DuplicatedEventHandlerError
from pydantic import BaseModel, Field, ValidationError
from unittest.mock import MagicMock


class ContentType(BaseModel):
    message: str
    data: list


class EventValidator(BaseModel):
    type: str = Field(min_length=3)
    content: ContentType


custom_event = {
    "type": "test",
    "content": {
        "message": "OK",
        "data": []
    }
}
other_custom_event = {
    "type": "other_test",
    "content": {
        "message": "OK"
    }
}


class TestCustomEventHandler:

    def test_should_map_custom_event_handler_correctly(self):
        event_name = "test"
        fake_function = MagicMock(lambda x: x)
        action = CustomEventActionBuilder.execute(fake_function).on(event_name)

        other_event_name = "other_test"
        other_fake_function = MagicMock(lambda y: y)
        other_action = CustomEventActionBuilder.execute(other_fake_function).on(other_event_name)

        handler = CustomEventHandler(action_selection_key="type")
        handler.add_action(action)
        handler.add_action(other_action)

        handler.resolve(custom_event)
        fake_function.assert_called_once()
        other_fake_function.assert_not_called()

    def test_should_map_two_custom_event_handlers_correctly(self):
        event_name = "test"
        fake_function = MagicMock(lambda x: x)
        action = CustomEventActionBuilder.execute(fake_function).on(event_name)

        other_event_name = "other_test"
        other_fake_function = MagicMock(lambda y: y)
        other_action = CustomEventActionBuilder.execute(other_fake_function).on(other_event_name)

        handler = CustomEventHandler(action_selection_key="type")
        handler.add_action(action)
        handler.add_action(other_action)

        handler.resolve(custom_event)
        handler.resolve(other_custom_event)

        fake_function.assert_called_once()
        other_fake_function.assert_called_once()

    def test_should_raise_an_error_if_handler_is_already_defined(self):
        with pytest.raises(DuplicatedEventHandlerError):
            event_name = "test"
            action = CustomEventActionBuilder.execute(lambda x: x).on(event_name)
            other_event_name = "test"
            other_action = CustomEventActionBuilder.execute(lambda y: y).on(other_event_name)

            handler = CustomEventHandler(action_selection_key="type")
            handler.add_action(action)
            handler.add_action(other_action)

    def test_should_raise_an_error_if_event_selection_key_could_not_be_found(self):
        with pytest.raises(InvalidCustomEventError):
            event_name = "test"
            action = CustomEventActionBuilder.execute(lambda x: x).on(event_name)
            other_event_name = "other_test"
            other_action = CustomEventActionBuilder.execute(lambda y: y).on(other_event_name)

            handler = CustomEventHandler(action_selection_key="notSelectionKey")
            handler.add_action(action)
            handler.add_action(other_action)

            handler.resolve(custom_event)

    def test_should_validate_event_if_validator_is_provided(self):

        event_name = "test"
        fake_function = lambda x: x.content.message == "OK"
        action = CustomEventActionBuilder.execute(fake_function).on(event_name)
        other_event_name = "other_test"
        other_action = CustomEventActionBuilder.execute(lambda x: x).on(other_event_name)

        handler = CustomEventHandler(
            action_selection_key="type",
            event_validator=EventValidator
        )
        handler.add_action(action)
        handler.add_action(other_action)

        resolved_handler = handler.resolve(custom_event)

        assert True == resolved_handler

        with pytest.raises(ValidationError):
            handler.resolve(other_custom_event)
