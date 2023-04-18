from enum import Enum


class CalculatorForm(str, Enum):
    SELECT_LEASE_PERIOD = "cf00"
    PRICE_COUNTER = "cf01"
    ENTER_PRICE = "cf02"

    def __str__(self) -> str:
        return str.__str__(self)
