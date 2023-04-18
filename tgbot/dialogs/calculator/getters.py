from aiogram_dialog import DialogManager

from ...config import Settings


async def calculator_form(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('db_session')
    config: Settings = middleware_data.get("config")
    ctx = dialog_manager.current_context()
    start_data = ctx.start_data
    dialog_data = ctx.dialog_data

    lease_periods = [("12 месяцев", 12), ("24 месяца", 24)]
    car_price = dialog_data.get("car_price") or 0
    lease_period = dialog_data.get("lease_period") or "12"
    started_by = start_data.get("started_by") or "UNKNOWN"

    return {"started_by": started_by,
            "car_price": car_price,
            "lease_period": lease_period,
            "lease_periods": lease_periods}
