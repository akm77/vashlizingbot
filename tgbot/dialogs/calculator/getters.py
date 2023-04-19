from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Counter

from tgbot.config import Settings
from tgbot.models.repo import get_periods, get_markets, get_period, get_market
from . import constants
from ...utils.decimals import format_decimal


async def calculator_form(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('db_session')
    config: Settings = middleware_data.get("config")
    ctx = dialog_manager.current_context()
    start_data = ctx.start_data
    dialog_data = ctx.dialog_data

    down_fee = config.down_fee
    dialog_data.update(down_fee=down_fee)

    lease_periods = get_periods()
    markets = get_markets()
    custom_interest = dialog_data.get("custom_interest", 0)
    car_price = dialog_data.get("car_price") or round((config.min_price + config.max_price) / 2)
    car_price = int(car_price)
    car_price_kbd = dialog_manager.find(constants.CalculatorForm.PRICE_COUNTER)
    await car_price_kbd.set_value(value=car_price)

    lease_period = dialog_data.get("lease_period") or "12"
    lease_period_kbd = dialog_manager.find(constants.CalculatorForm.SELECT_LEASE_PERIOD)
    await lease_period_kbd.set_checked(item_id=lease_period)

    market = dialog_data.get("market") or "local_market"
    market_kbd = dialog_manager.find(constants.CalculatorForm.SELECT_MARKET)
    await market_kbd.set_checked(item_id=market)

    started_by = start_data.get("started_by") or "UNKNOWN"

    match market:
        case "local_market":
            if lease_period == "12":
                actual_interest_rate = config.local_market_interest_rate_12
            elif lease_period == "24":
                actual_interest_rate = config.local_market_interest_rate_24
            else:
                actual_interest_rate = config.local_market_interest_rate_24
        case "foreign_market":
            if lease_period == "12":
                actual_interest_rate = config.foreign_market_interest_rate_12
            elif lease_period == "24":
                actual_interest_rate = config.foreign_market_interest_rate_24
            else:
                actual_interest_rate = config.foreign_market_interest_rate_24
        case _:
            actual_interest_rate = config.local_market_interest_rate_24

    admins = config.admins
    user = dialog_manager.middleware_data.get("event_from_user").id
    if user in admins and not custom_interest:
        interest_kbd = dialog_manager.find(constants.CalculatorForm.INTEREST_COUNTER)
        await interest_kbd.set_value(actual_interest_rate)

    actual_interest_rate = custom_interest or actual_interest_rate
    dialog_data.update(actual_interest_rate=actual_interest_rate)

    dialog_data.update(lease_period_in_year="один год" if lease_period == "12" else "два года")

    dialog_data.update(formated_car_price=format_decimal(round(car_price), delimiter=" ", pre=1))

    actual_down_fee = car_price * down_fee / 100
    dialog_data.update(actual_down_fee=format_decimal(round(actual_down_fee), delimiter=" ", pre=1))

    monthly_fee = round((car_price * (100 + actual_interest_rate) / 100 - actual_down_fee) / int(lease_period))
    dialog_data.update(monthly_fee=format_decimal(round(monthly_fee), delimiter=" ", pre=1))

    return {"started_by": started_by,
            "down_fee": down_fee,
            "car_price": format_decimal(car_price, delimiter=" ", pre=1),
            "actual_down_fee": format_decimal(round(actual_down_fee), delimiter=" ", pre=1),
            "monthly_fee": format_decimal(round(monthly_fee), delimiter=" ", pre=1),
            "lease_period_name": get_period(lease_period).name,
            "lease_periods": lease_periods,
            "actual_interest_rate": actual_interest_rate,
            "market_name": get_market(market).name,
            "markets": markets}
