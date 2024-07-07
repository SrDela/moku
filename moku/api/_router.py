from moku._interfaces.event_handler import EventHandler

from . import _typing
from ._route import APIGatewayRoute
from .exceptions import InvalidRouteException


class APIGatewayRouter(EventHandler):

    def __init__(self) -> None:
        self.__routes: _typing.RouteMap = {}

    def add_route(self, route: APIGatewayRoute) -> None:
        self.__routes |= route.map_

    @property
    def routes(self):
        return self.__routes

    def resolve(self, resource: str, method: str) -> _typing.RouteAction:
        action = self.__routes.get(APIGatewayRoute.build_key(resource, method))
        if action is None:
            raise InvalidRouteException(f"The {method} method for resource '{resource}' is not mapped.")
        return action
