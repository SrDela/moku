from __future__ import annotations
from typing import Optional
from collections import defaultdict
from enum import Enum

from .exceptions import InvalidRouteException
from . import _typing


class HTTPMethod(Enum):
    GET: str = "GET"
    POST: str = "POST"
    PATCH: str = "PATCH"
    PUT: str = "PUT"
    DELETE: str = "DELETE"

    @classmethod
    def list_(cls):
        return [method.value for method in cls]


class APIGatewayRoute:

    def __init__(self, prefix: str) -> None:
        self.__prefix: str = prefix
        self.__path: Optional[str] = None
        self.__root: Optional[str] = None
        self.__action: Optional[str] = None
        self.__id: Optional[str] = None
        self.__method: Optional[str] = None
        self.__path_map: _typing.RouteMap = defaultdict(_typing.RouteProps)

    def when(self, path: str, method: str) -> APIGatewayRoute:
        self.__validate_http_method(method)
        self.__path = path if path.startswith("/") else f'/{path}'
        parts = self.__path.split('/', maxsplit=3)
        self.__root = parts[0]
        if len(parts) > 1:
            self.__action = parts[1]
        if len(parts) > 2:
            self.__id = parts[2]
        self.__method = method
        return self

    def then(self, action: _typing.RouteAction) -> None:
        if self.__path is None or self.__method is None:
            raise InvalidRouteException("Missing path or method.")
        key = self.__prefix
        if self.__root:
            key += f"/{self.__root}"
        if self.__action:
            key += f"/{self.__action}"
        if self.__id:
            key += f"/{self.__id}"
        self.__path_map[key].methods[self.__method] = action
        self.__path_map[key].action = self.__action
        self.__path_map[key].id_ = self.__id

    def __validate_http_method(self, method: str) -> None:
        try:
            HTTPMethod(method)
        except ValueError:
            raise InvalidRouteException(
                "Invalid HTTP Method provided. Provide one of the following "
                + ", ".join(HTTPMethod.list_())
            )

    @property
    def prefix(self) -> str:
        return self.__prefix

    @property
    def map_(self) -> _typing.RouteMap:
        return self.__path_map
