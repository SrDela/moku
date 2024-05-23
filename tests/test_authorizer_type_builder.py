import pytest
from moku.authorizer import AuthorizerTypeBuilder
from moku.authorizer._typing import AuthorizerType
from moku.authorizer.exceptions import InvalidAuthorizerProcedure, UnmappedAuthorizationTypeError

fake_req_procedure = lambda x: x
fake_token_procedure = lambda x: x


class TestAuthorizerTypeBuilder:

    def test_should_create_type_successfully(self):
        auth_type = AuthorizerTypeBuilder.for_auth_type('REQUEST').use(fake_req_procedure)
        man_auth_type = AuthorizerType(type='REQUEST', procedure=fake_req_procedure)

        assert man_auth_type.type == auth_type.type
        assert man_auth_type.procedure == auth_type.procedure

    def test_should_create_type_successfully_with_instance(self):
        auth_type = AuthorizerTypeBuilder('REQUEST').use(fake_req_procedure)
        man_auth_type = AuthorizerType(type='REQUEST', procedure=fake_req_procedure)

        assert man_auth_type.type == auth_type.type
        assert man_auth_type.procedure == auth_type.procedure

    def test_should_create_two_types_successfully(self):
        req_type = AuthorizerTypeBuilder.for_auth_type('REQUEST').use(fake_req_procedure)
        token_type = AuthorizerTypeBuilder.for_auth_type('TOKEN').use(fake_token_procedure)

        man_req_type = AuthorizerType(type='REQUEST', procedure=fake_req_procedure)
        man_token_type = AuthorizerType(type='TOKEN', procedure=fake_token_procedure)

        assert man_req_type.type == req_type.type
        assert man_req_type.procedure == req_type.procedure
        assert man_token_type.type == token_type.type
        assert man_token_type.procedure == token_type.procedure

    def test_should_raise_an_error_if_procedure_is_not_callable(self):
        with pytest.raises(InvalidAuthorizerProcedure, match=r'must be a function or method.'):
            AuthorizerTypeBuilder.for_auth_type('REQUEST').use(1)

    def test_should_raise_an_error_if_auth_type_is_not_defined(self):
        with pytest.raises(UnmappedAuthorizationTypeError, match=r'An auth type must be defined first'):
            AuthorizerTypeBuilder().use(fake_req_procedure)
