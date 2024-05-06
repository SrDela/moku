import pytest
from typing import Callable
from moku.api import APIGatewayRouter, APIGatewayRoute
from moku.api.exceptions import InvalidRouteException


class TestAPIRouter:

    func: Callable[[any], None] = lambda x: print(x)
    func2: Callable[[any], None] = lambda x: print(x, 1)

    def test_should_add_route_and_return_its_action(self):
        route = self.__build_test_route()
        router = APIGatewayRouter()
        router.add_route(route)

        assert 3 == len(router.routes.keys())

        action = router.resolve(resource="/myroute", method="GET")
        action2 = router.resolve(resource="/myroute/{some_id}", method="GET")
        action3 = router.resolve(resource="/myroute/extrapath", method="POST")

        assert self.func == action
        assert self.func == action2
        assert self.func2 == action3

    def test_should_raise_exception_if_resource_was_not_mapped(self):
        route = self.__build_test_route()
        router = APIGatewayRouter()
        router.add_route(route)

        with pytest.raises(InvalidRouteException):
            router.resolve(resource="/otherroute/path", method="PATCH")

    def test_should_raise_exception_if_method_was_not_mapped(self):
        route = self.__build_test_route()
        router = APIGatewayRouter()
        router.add_route(route)

        with pytest.raises(InvalidRouteException):
            router.resolve(resource="/myroute", method="PUT")

    def __build_test_route(self) -> APIGatewayRoute:
        route = APIGatewayRoute("/myroute")
        route.when(path="/", method="GET").then(self.func)
        route.when(path="/", method="POST").then(self.func)
        route.when(path="/{some_id}", method="GET").then(self.func)
        route.when(path="/extrapath", method="POST").then(self.func2)
        return route
