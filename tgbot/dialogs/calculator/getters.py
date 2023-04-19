from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Radio, Counter

from tgbot.config import Settings
from . import constants
from tgbot.models.repo import get_periods, get_markets, get_period, get_market


async def calculator_form(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('db_session')
    config: Settings = middleware_data.get("config")
    ctx = dialog_manager.current_context()
    start_data = ctx.start_data
    dialog_data = ctx.dialog_data

    lease_periods = get_periods()
    markets = get_markets()

    car_price = dialog_data.get("car_price") or 400_000
    car_price_kbd: Counter = dialog_manager.find(constants.CalculatorForm.PRICE_COUNTER)
    await car_price_kbd.set_value(value=int(car_price))

    lease_period = dialog_data.get("lease_period") or "12"
    lease_period_kbd: Radio = dialog_manager.find(constants.CalculatorForm.SELECT_LEASE_PERIOD)
    await lease_period_kbd.set_checked(item_id=lease_period)

    market = dialog_data.get("market") or "local_market"
    market_kbd: Radio = dialog_manager.find(constants.CalculatorForm.SELECT_MARKET)
    await market_kbd.set_checked(item_id=market)

    started_by = start_data.get("started_by") or "UNKNOWN"

    return {"started_by": started_by,
            "car_price": car_price,
            "lease_period_name": get_period(lease_period).name,
            "lease_periods": lease_periods,
            "market_name": get_market(market).name,
            "markets": markets}
