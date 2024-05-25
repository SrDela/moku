from moku._interfaces.event_handler import EventHandler
from moku.utils import PYDANTIC_AVAILABLE

from typing import Optional

from . import _typing
from .exceptions import InvalidCustomEventError, DuplicatedEventHandlerError


class CustomEventHandler(EventHandler):

    def __init__(self, action_selection_key: str, event_validator: Optional[object] = None) -> None:
        """Custom event mapper generator

        Args:
            action_selection_key (str): The key that will be searched in the events to pick a handler
            event_validator (Optional[object], optional): A pydantic model. If pydantic is detected,
            then model_validate is executed on the validator for the event when resolving.
            Defaults to None.
        """
        self.__action_selection_key: str = action_selection_key
        self.__custom_handler_map: _typing.CustomEventMap = {}
        self.__event_validator: Optional[object] = event_validator

    def add_action(self, action: _typing.DefaultCustomEventAction) -> None:
        if self.__custom_handler_map.get(action.name) is not None:
            raise DuplicatedEventHandlerError(f"An action named '{action.name}' is already mapped.")
        self.__custom_handler_map[action.name] = action.action

    def resolve(self, event: dict) -> any:
        event_name = event.get(self.__action_selection_key)

        if PYDANTIC_AVAILABLE and self.__event_validator is not None:
            event = self.__event_validator.model_validate(event)

        if event_name is None:
            raise InvalidCustomEventError("The provided event does not satisfies the expected format.")
        return self.__custom_handler_map[event_name](event)
