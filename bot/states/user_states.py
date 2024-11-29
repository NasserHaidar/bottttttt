from aiogram.fsm.state import State, StatesGroup
from icecream import ic

class UserStates(StatesGroup):
    #main menu
    main_menu = State()

    #profile_menu
    profile_menu = State()

    #balance
    balance_menu = State()
    top_up_balance = State()

    #set photo
    send_photo = State()

    #generating
    prompt = State()
    model = State()
    style = State()