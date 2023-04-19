from aiogram.types import Message
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.common import ManagedWidget
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Select, ManagedCounterAdapter

from . import states, constants
from ...config import Settings
from ...utils.decimals import check_digit_value


async def on_lease_period_changed(event: ChatEvent, widget: ManagedWidget[Select], manager: DialogManager, item_id):
    ctx = manager.current_context()
    ctx.dialog_data.update(lease_period=item_id)


async def on_market_changed(event: ChatEvent, widget: ManagedWidget[Select], manager: DialogManager, item_id):
    ctx = manager.current_context()
    ctx.dialog_data.update(market=item_id)


async def on_car_price_changed(event: ChatEvent, widget: ManagedCounterAdapter, manager: DialogManager):
    ctx = manager.current_context()
    car_price = widget.get_value()
    ctx.dialog_data.update(car_price=car_price)


async def on_interest_changed(event: ChatEvent, widget: ManagedCounterAdapter, manager: DialogManager):
    ctx = manager.current_context()
    custom_interest = widget.get_value()
    ctx.dialog_data.update(custom_interest=custom_interest)


async def on_enter_price(message: Message, message_input: MessageInput,
                         manager: DialogManager):
    ctx = manager.current_context()
    config: Settings = manager.middleware_data.get("config")
    try:
        car_price = check_digit_value(message.text, type_factory=int,
                                      min_value=config.min_price, max_value=config.max_price)
        ctx.dialog_data.update(car_price=car_price)
    except ValueError:
        await message.answer(f"Ошибка ввода {message.text}, необходимо целое число в диапазоне  \n")
        return
    await manager.switch_to(states.CalculatorStates.enter_data)
