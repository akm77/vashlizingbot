import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button

from tgbot.config import Settings
from tgbot.utils.calculation import cost_calculation

logger = logging.getLogger(__name__)

PROPOSAL = """\
Условия лизинга:
-При условии лизинга на <b>{lease_period_in_year}</b> и процентной ставки <b>{actual_interest_rate} %</b>:
Стоимость авто –  <b>{formated_car_price}</b> AED
Первоначальный взнос <b>{down_fee} %</b> от стоимости авто <b>{car_price}</b> AED = <b>{actual_down_fee}</b> AED
С учетом первоначального взноса, ежемесячный платеж составляет - <b>{monthly_fee}</b> AED
"""


async def on_click_calculate(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.show_mode = ShowMode.SEND
    dialog_data = manager.current_context().dialog_data
    config: Settings = manager.middleware_data.get("config")
    session = manager.middleware_data.get('db_session')
    cost_calculation_text = await cost_calculation(config=config,
                                                   db_session=session,
                                                   data=dialog_data,
                                                   manager=manager)
    dialog_data.update(cost_calculation_text=cost_calculation_text)


async def on_click_exit(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.show_mode = ShowMode.EDIT
    dialog_data = manager.current_context().dialog_data

    #
    # actual_down_fee = car_price * down_fee / 100
    # dialog_data.update(actual_down_fee=format_decimal(round(actual_down_fee), delimiter=" ", pre=1))
    #
    # monthly_fee = round((car_price * (100 + actual_interest_rate) / 100 - actual_down_fee) / int(lease_period))
    # dialog_data.update(monthly_fee=format_decimal(round(monthly_fee), delimiter=" ", pre=1))
    await callback.message.answer(PROPOSAL.format_map(dialog_data))
