from aiogram import Dispatcher
from aiogram_dialog import DialogRegistry

from . import calculator


def setup_dialogs(dp: Dispatcher):
    registry = DialogRegistry()
    for dialog in [
        *calculator.calculator_dialogs(),
    ]:
        registry.register(dialog)  # register a dialog

    registry.setup_dp(dp)
