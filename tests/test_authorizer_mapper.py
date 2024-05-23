import pytest
from moku.authorizer.exceptions import DuplicatedAuthorizerError, UnmappedAuthorizationTypeError
from moku.authorizer import AuthorizerTypeBuilder, AuthorizerMapper

fake_req_procedure = lambda x: x
fake_token_procedure = lambda x: x


class TestAuthorizerMapper:

    def test_should_map_authorizer_correctly(self):
        req_auth_type = AuthorizerTypeBuilder.for_auth_type('REQUEST').use(fake_req_procedure)
        mapper = AuthorizerMapper()
        mapper.add_authorizer(req_auth_type)

        assert fake_req_procedure == mapper.resolve('REQUEST')

    def test_should_map_two_authorizers_correctly(self):
        req_auth_type = AuthorizerTypeBuilder.for_auth_type('REQUEST').use(fake_req_procedure)
        token_auth_type = AuthorizerTypeBuilder.for_auth_type('TOKEN').use(fake_token_procedure)

        mapper = AuthorizerMapper()
        mapper.add_authorizer(req_auth_type)
        mapper.add_authorizer(token_auth_type)

        assert fake_req_procedure == mapper.resolve('REQUEST')
        assert fake_token_procedure == mapper.resolve('TOKEN')

    def test_should_raise_an_error_if_type_is_already_mapped(self):
        with pytest.raises(DuplicatedAuthorizerError):
            req_auth_type = AuthorizerTypeBuilder.for_auth_type('REQUEST').use(fake_req_procedure)
            other_auth_type = AuthorizerTypeBuilder.for_auth_type('REQUEST').use(fake_req_procedure)
            mapper = AuthorizerMapper()
            mapper.add_authorizer(req_auth_type)
            mapper.add_authorizer(other_auth_type)

    def test_should_raise_an_error_if_type_is_not_mapped(self):
        with pytest.raises(UnmappedAuthorizationTypeError, match="is not mapped"):
            req_auth_type = AuthorizerTypeBuilder.for_auth_type('REQUEST').use(fake_req_procedure)
            mapper = AuthorizerMapper()
            mapper.add_authorizer(req_auth_type)
            mapper.resolve('TOKEN')
