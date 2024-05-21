import pytest
from moku.ws import WebSocketAPIRouter
from moku.ws.exceptions import InvalidRouteKeyException, InvalidRouteActionException


class TestWSRouter:

    def test_should_route_correctly_one_action(self):
        fake_action = lambda x: x
        router = WebSocketAPIRouter()
        route_key = "$connect"
        router.on(route_key).perform(fake_action)

        assert len(router.route_actions) == 1
        assert router.resolve(route_key) == fake_action

    def test_should_route_correctly_two_actions(self):
        fake_action = lambda x: x
        other_fake_action = lambda y: y

        router = WebSocketAPIRouter()
        route_key = "$connect"
        other_route_key = "$disconnect"
        router.on(route_key).perform(fake_action)
        router.on(other_route_key).perform(other_fake_action)

        assert len(router.route_actions) == 2
        assert router.resolve(route_key) == fake_action
        assert router.resolve(other_route_key) == other_fake_action

    def test_should_raise_exception_if_route_is_unmapped(self):
        with pytest.raises(InvalidRouteKeyException, match="Unmapped route key."):
            router = WebSocketAPIRouter()
            route_key = "$connect"
            router.resolve(route_key)

    def test_should_raise_exception_if_route_key_is_empty(self):
        with pytest.raises(InvalidRouteKeyException, match="cannot be empty"):
            router = WebSocketAPIRouter()
            route_key = ""
            router.on(route_key).perform(lambda x: x)

    def test_should_raise_exception_if_route_is_already_mapped(self):
        with pytest.raises(InvalidRouteKeyException, match="has already been mapped"):
            router = WebSocketAPIRouter()
            route_key = "$connect"
            router.on(route_key).perform(lambda x: x)
            router.on(route_key).perform(lambda y: y)

    def test_should_raise_exception_if_action_is_not_a_function(self):
        with pytest.raises(InvalidRouteActionException, match="must be a function."):
            router = WebSocketAPIRouter()
            route_key = "$connect"
            router.on(route_key).perform(3)
