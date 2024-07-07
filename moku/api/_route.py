from __future__ import annotations
from typing import Optional

from .exceptions import InvalidRouteException
from . import _typing


class APIGatewayRoute:

    def __init__(self, prefix: str) -> None:
        self.__prefix: str = prefix
        self.__path: Optional[str] = None
        self.__method: Optional[str] = None
        self.__path_map: _typing.RouteMap = {}

    def route(self, path: str, method: str) -> APIGatewayRoute:
        self.__validate_http_method(method)
        self.__path = path[1:] if path.startswith("/") else path
        self.__method = method
        return self

    def to(self, action: _typing.RouteAction) -> None:
        if self.__path is None or self.__method is None:
            raise InvalidRouteException("Missing path or method.")

        key = self.build_key(self.__prefix, self.__method)
        if self.__path not in {"/", ""}:
            key = self.build_key(f"{self.__prefix}/{self.__path}", self.__method)
        self.__path_map[key] = action

        self.clean_attributes()

    def __validate_http_method(self, method: str) -> None:
        try:
            _typing.HTTPMethod(method)
        except ValueError:
            raise InvalidRouteException(
                "Invalid HTTP Method provided. Provide one of the following "
                + ", ".join(_typing.HTTPMethod.list_())
            )

    @staticmethod
    def build_key(resource: str, method: str) -> str:
        return f"{method}::{resource}"

    @property
    def prefix(self) -> str:
        return self.__prefix

    @property
    def map_(self) -> _typing.RouteMap:
        return self.__path_map

    def clean_attributes(self) -> None:
        self.__path = None
        self.__method = None
