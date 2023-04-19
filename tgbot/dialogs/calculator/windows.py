from aiogram.enums import ContentType
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Format

from . import states, getters, keyboards

CALC_FORM = """\
Расчет для: {started_by}\n
<pre>------------------------------</pre>\n
Основные критерии выбора авто
- авто должно быть не старше <b>3</b> лет (2020 -2023)
- стоимость покупки не более <b>200 000</b> АЕД (+-10% по согласованию сторон)\n

Откуда авто - <b>{market_name}</b>
Стоимость авто - <b>{car_price}</b> AED
Срок лизинга - <b>{lease_period_name}</b>
Первоначальный взнос - <b>{down_fee} %</b>
Процентная ставка - <b>{actual_interest_rate} %</b>
"""


def calculator_window(**defaults):
    return Window(Format(CALC_FORM),
                  keyboards.enter_price(**defaults),
                  state=states.CalculatorStates.enter_data,
                  getter=getters.calculator_form)


def calculator_input_window(text: str, handler=None, state=None, getter=None, **defaults):
    return Window(
        Format(text),
        MessageInput(handler,
                     content_types=[ContentType.TEXT]),
        state=state,
        getter=getter
    )
