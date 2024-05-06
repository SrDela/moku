from typing import Dict

from moku._interfaces.event_handler import EventHandler

from . import _typing
from ._route import APIGatewayRoute
from .exceptions import InvalidRouteException


class APIGatewayRouter(EventHandler):

    def __init__(self) -> None:
        self.__routes: Dict[str, _typing.RouteProps] = {}

    def add_route(self, route: APIGatewayRoute) -> None:
        for path, values in route.map_.items():
            path = path.removesuffix('/')
            self.__routes[path] = values

    @property
    def routes(self):
        return self.__routes

    def resolve(self, resource: str, method: str) -> _typing.RouteAction:
        route = self.__routes.get(resource)
        if route is None:
            raise InvalidRouteException(f"Resource '{resource}' is not mapped")
        action = route.methods.get(method)
        if action is None:
            raise InvalidRouteException("Invalid method.")
        return action
