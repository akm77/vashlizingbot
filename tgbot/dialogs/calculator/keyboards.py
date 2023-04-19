import operator

from aiogram import F
from aiogram_dialog.widgets.kbd import Row, Radio, Group, Button, SwitchTo, Cancel, Counter
from aiogram_dialog.widgets.text import Format, Const

from . import constants, events, states, onclick, whenable


def enter_price(**defaults):
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
            min_value=defaults.get("min_price"),
            max_value=defaults.get("max_price"),
            increment=defaults.get("price_step"),
            default=round((defaults.get("min_price") + defaults.get("max_price")) / 2),
            cycle=True,
            on_value_changed=events.on_car_price_changed
        ),
        Counter(
            id=constants.CalculatorForm.INTEREST_COUNTER,
            min_value=1,
            max_value=100,
            increment=1,
            default=20,
            cycle=True,
            on_value_changed=events.on_interest_changed,
            when=whenable.is_admin
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
        Cancel(Const("<<"),
               on_click=onclick.on_click_exit)
    )

