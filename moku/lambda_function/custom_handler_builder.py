from __future__ import annotations
from inspect import ismethod, isfunction

from . import _typing
from .exceptions import InvalidCustomEventAction


class CustomEventActionBuilder:

    def __init__(self, action: _typing.DefaultLambdaHandler) -> None:
        self.__action: _typing.DefaultLambdaHandler = action

    @staticmethod
    def execute(action: _typing.DefaultLambdaHandler) -> CustomEventActionBuilder:
        if not isfunction(action) and not ismethod(action):
            raise InvalidCustomEventAction("Action must be a function.")
        return CustomEventActionBuilder(action)

    def on(self, name: str) -> _typing.DefaultCustomEventAction:
        return _typing.DefaultCustomEventAction(
            name=name,
            action=self.__action
        )
