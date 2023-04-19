import operator

from aiogram_dialog.widgets.kbd import Row, Radio, Group, Button, SwitchTo, Cancel, Counter
from aiogram_dialog.widgets.text import Format, Const

from . import constants, events, states, onclick, whenable


def enter_price():
    return Group(
        Row(
            Radio(
                Format("✅ {item.name}"),
                Format("  {item.name}"),
                id=constants.CalculatorForm.SELECT_MARKET,
                item_id_getter=operator.attrgetter("code"),
                on_state_changed=events.on_market_changed,
                items="markets",

            )
        ),
        SwitchTo(Const("✍️ Цена"),
                 id=constants.CalculatorForm.ENTER_PRICE,
                 state=states.CalculatorStates.enter_price),
        Counter(
            id=constants.CalculatorForm.PRICE_COUNTER,
            min_value=100_000,
            max_value=999_999,
            increment=20_000,
            default=400_000,
            cycle=True,
            on_value_changed=events.on_car_price_changed
        ),
        Row(
            Radio(
                Format("✅ {item.name}"),
                Format("  {item.name}"),
                id=constants.CalculatorForm.SELECT_LEASE_PERIOD,
                item_id_getter=operator.attrgetter("code"),
                on_state_changed=events.on_lease_period_changed,
                items="lease_periods",

            )
        ),
        Cancel(Const("<<"))
    )

