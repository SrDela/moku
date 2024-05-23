from __future__ import annotations
from typing import Optional, Callable
from inspect import isfunction, ismethod

from .exceptions import InvalidAuthorizerProcedure, UnmappedAuthorizationTypeError
from . import _typing


class AuthorizerTypeBuilder:

    def __init__(self, auth_type: Optional[str] = None) -> None:
        self.__auth_type: Optional[str] = auth_type

    @staticmethod
    def for_auth_type(auth_type: str) -> AuthorizerTypeBuilder:
        return AuthorizerTypeBuilder(auth_type)

    def use(self, procedure: _typing.AuthorizationProcedure) -> _typing.AuthorizerType:
        if self.__auth_type is None:
            raise UnmappedAuthorizationTypeError("An auth type must be defined first by using the 'for_auth_type' method.")
        if not isfunction(procedure) and not ismethod(procedure):
            raise InvalidAuthorizerProcedure("Procedure must be a function or method.")
        return _typing.AuthorizerType(
            type=self.__auth_type,
            procedure=procedure
        )
