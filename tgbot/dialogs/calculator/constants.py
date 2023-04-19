from enum import Enum


class CalculatorForm(str, Enum):
    SELECT_LEASE_PERIOD = "cf00"
    SELECT_MARKET = "cf01"
    PRICE_COUNTER = "cf02"
    ENTER_PRICE = "cf03"
    INTEREST_COUNTER = "cf04"

    def __str__(self) -> str:
        return str.__str__(self)
