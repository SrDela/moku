class InvalidRouteKeyException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InvalidRouteActionException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
