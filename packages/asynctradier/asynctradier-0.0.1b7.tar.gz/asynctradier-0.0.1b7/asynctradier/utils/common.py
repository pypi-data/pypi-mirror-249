import re

from asynctradier.exceptions import InvalidExiprationDate, InvalidOptionType


def build_option_symbol(
    symbol: str, expiration_date: str, strike: float, option_type: str
) -> str:
    if not is_valid_expiration_date(expiration_date):
        raise InvalidExiprationDate(expiration_date)

    if not is_valid_option_type(option_type):
        raise InvalidOptionType(option_type)
    return f"{symbol.upper()}{expiration_date.replace('-', '')[2:]}{option_type.upper()[0]}{str(int(strike * 1000)).zfill(8)}"


def is_valid_expiration_date(expiration: str) -> bool:
    # valid exp date is YYYY-MM-DD
    return bool(re.match(r"\d{4}-\d{2}-\d{2}", expiration))


def is_valid_option_type(option_type: str) -> bool:
    return option_type.upper() in ("CALL", "PUT")
