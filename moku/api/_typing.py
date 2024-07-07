from typing import Dict, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum


class HTTPMethod(Enum):
    GET: str = "GET"
    POST: str = "POST"
    PATCH: str = "PATCH"
    PUT: str = "PUT"
    DELETE: str = "DELETE"

    @classmethod
    def list_(cls):
        return [method.value for method in cls]


RouteAction = Callable[[dict], any]

RouteMap = Dict[str, RouteAction]
