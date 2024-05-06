import pytest
from moku.api import APIGatewayRoute
from moku.api.exceptions import InvalidRouteException


class TestAPIRoute:

    def test_should_route_one_action_correctly(self):
        route = APIGatewayRoute("/myroute")
        func = lambda x: print(x)
        route.when(path="/", method="GET").then(func)

        assert func == route.map_.get("/myroute").methods["GET"]

    def test_should_route_two_actions_correctly(self):
        route = APIGatewayRoute("/myroute")
        func = lambda x: print(x)
        func2 = lambda x: print(x, 1)
        route.when(path="/", method="GET").then(func)
        route.when(path="/extrapath", method="POST").then(func2)

        assert func == route.map_.get("/myroute").methods["GET"]
        assert func2 == route.map_.get("/myroute/extrapath").methods["POST"]

    def test_should_raise_exception_if_when_is_not_defined(self):
        route = APIGatewayRoute("/myroute")

        with pytest.raises(InvalidRouteException):
            route.then(lambda x: print(x))

    def test_should_raise_exception_if_http_method_is_invalid_or_not_allowed(self):
        route = APIGatewayRoute("/myroute")

        with pytest.raises(InvalidRouteException):
            route.when(path="/", method="SOME").then(lambda x: print(x))

    def test_should_split_and_store_props_correctly(self):
        route = APIGatewayRoute("/myroute")

        assert "/myroute" == route.prefix

        func = lambda x: print(x)
        route.when(path="/action/{id}", method="GET").then(func)
        route.when(path="/action/{id}", method="POST").then(func)

        route_props = route.map_.get("/myroute/action/{id}")
        assert "action" == route_props.action
        assert "{id}" == route_props.id_
        assert 2 == len(route_props.methods)
