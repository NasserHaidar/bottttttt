from aiogram.fsm.state import State, StatesGroup
from icecream import ic

class UserStates(StatesGroup):
    main_menu = State()
    prompt = State()
    model = State()
    style = State()