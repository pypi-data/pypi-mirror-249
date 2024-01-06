class InvalidExiprationDate(Exception):
    def __init__(self, expiration: str):
        self.expiration = expiration
        super().__init__(
            f"ExpirationDate {expiration} is not valid. Valid values is: YYYY-MM-DD"
        )


class InvalidStrikeType(Exception):
    def __init__(self, strike: any):
        self.strike = strike
        super().__init__(
            f"Strike type {type(strike)} is not valid. Valid values are: float, int"
        )


class MissingRequiredParameter(Exception):
    def __init__(self, msg: str):
        super().__init__(msg)


class InvalidOptionType(Exception):
    def __init__(self, option_type: str) -> None:
        super().__init__(
            f"Option type {option_type} is not valid. Valid values are: CALL, PUT"
        )


class InvalidParameter(Exception):
    def __init__(self, msg: str) -> None:
        super().__init__(f"Parameter is not valid. {msg}")


class BadRequestException(Exception):
    def __init__(self, code: int, msg: str) -> None:
        super().__init__(f"Request failed: {code}, msg: {msg}")
