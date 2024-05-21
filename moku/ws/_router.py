from __future__ import annotations
from inspect import isfunction

from . import _typing
from .exceptions import InvalidRouteActionException, InvalidRouteKeyException


class WebSocketAPIRouter:

    def __init__(self) -> None:
        self.__route_actions: _typing.RouteActionList = {}
        self.__route_key: str = ""

    def on(self, route_key: str) -> WebSocketAPIRouter:
        if len(route_key) == 0:
            raise InvalidRouteKeyException("Route cannot be empty.")

        if self.__route_actions.get(route_key) is not None:
            raise InvalidRouteKeyException("Route has already been mapped.")

        self.__route_key = route_key
        return self

    def perform(self, action: _typing.RouteAction) -> None:
        if not isfunction(action):
            raise InvalidRouteActionException("Action must be a function.")
        self.__route_actions[self.__route_key] = action

    @property
    def route_actions(self) -> _typing.RouteActionList:
        return self.__route_actions

    def resolve(self, route_key: str) -> _typing.RouteAction:
        action = self.__route_actions.get(route_key)
        if action is None:
            raise InvalidRouteKeyException("Unmapped route key.")
        return action
