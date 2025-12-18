from aiogram.fsm.state import State, StatesGroup

class SearchState(StatesGroup):
    city = State()
    district = State()
    property_type = State()
    price = State()
