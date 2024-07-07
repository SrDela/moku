import pytest
from moku.api import APIGatewayRoute
from moku.api.exceptions import InvalidRouteException


class TestAPIRoute:

    def test_should_route_one_action_correctly(self):
        route = APIGatewayRoute("/myroute")
        func = lambda x: print(x)
        route.route(path="/", method="GET").to(func)

        assert func == route.map_.get(route.build_key("/myroute", "GET"))

    def test_should_route_two_actions_correctly(self):
        route = APIGatewayRoute("/myroute")
        func = lambda x: print(x)
        func2 = lambda x: print(x, 1)
        route.route(path="/", method="GET").to(func)
        route.route(path="/extrapath", method="POST").to(func2)

        assert func == route.map_.get(route.build_key("/myroute", "GET"))
        assert func2 == route.map_.get(route.build_key("/myroute/extrapath", "POST"))

    def test_should_raise_exception_if_route_is_not_defined(self):
        route = APIGatewayRoute("/myroute")

        with pytest.raises(InvalidRouteException, match="Missing path or method."):
            route.to(lambda x: print(x))

    def test_should_raise_exception_if_http_method_is_invalid_or_not_allowed(self):
        route = APIGatewayRoute("/myroute")

        with pytest.raises(InvalidRouteException, match="Invalid HTTP Method provided."):
            route.route(path="/", method="SOME").to(lambda x: print(x))
