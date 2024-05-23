class InvalidAuthorizerProcedure(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DuplicatedAuthorizerError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class UnmappedAuthorizationTypeError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
