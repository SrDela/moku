from typing import Dict

from . import _typing
from .exceptions import DuplicatedAuthorizerError, UnmappedAuthorizationTypeError


class AuthorizerMapper:

    def __init__(self) -> None:
        self.__auth_map: Dict[str, _typing.AuthorizationProcedure] = {}

    def add_authorizer(self, authorizer: _typing.AuthorizerType) -> None:
        if self.__auth_map.get(authorizer.type) is not None:
            raise DuplicatedAuthorizerError(f"An authorizer of type '{authorizer.type}' is already mapped.")
        self.__auth_map[authorizer.type] = authorizer.procedure

    def resolve(self, auth_type: str) -> _typing.AuthorizationProcedure:
        procedure = self.__auth_map.get(auth_type)
        if not procedure:
            raise UnmappedAuthorizationTypeError(f"Authorization type '{auth_type}' is not mapped.")
        return procedure
