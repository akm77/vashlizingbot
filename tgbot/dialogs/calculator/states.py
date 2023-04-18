from aiogram.fsm.state import StatesGroup, State


class CalculatorStates(StatesGroup):
    enter_data = State()
    enter_price = State()




