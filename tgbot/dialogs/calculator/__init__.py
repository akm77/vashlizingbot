from aiogram_dialog import Dialog

from . import windows, events, states, getters


def calculator_dialogs(**defaults):
    return [
        Dialog(
            windows.calculator_window(**defaults),
            windows.calculator_input_window(text="👇 Введите цену 👇",
                                            handler=events.on_enter_price,
                                            state=states.CalculatorStates.enter_price,
                                            getter=getters.calculator_form),
            on_start=None,
            on_process_result=None
        )
    ]
