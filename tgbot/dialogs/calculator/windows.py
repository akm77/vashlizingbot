from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Format

from . import states, getters, keyboards

CALC_FORM = """\
Расчет для: {started_by}\n
<pre>------------------------------</pre>\n
Откуда авто - <b>{market_name}</b>
Стоимость авто - <b>{car_price}</b> AED
Срок лизинга - <b>{lease_period_name}</b>
"""


def calculator_window():
    return Window(Format(CALC_FORM),
                  keyboards.enter_price(),
                  state=states.CalculatorStates.enter_data,
                  getter=getters.calculator_form)


def calculator_input_window(text: str, handler=None, state=None, getter=None):
    return Window(
        Format(text),
        MessageInput(handler,
                     content_types=[ContentType.TEXT]),
        state=state,
        getter=getter
    )
