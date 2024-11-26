#imports
import aiogram

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from aiogram.filters import StateFilter, Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from icecream import ic

from ..keyboards import inline_keyboards
from ..states.user_states import UserStates
from ..filters import chat_type

#create new Router for handling user messages
user_router = aiogram.Router()
user_router.message.filter(chat_type.ChatTypeFilter(["private"]))

#handling /start command
async def start_handler(message_or_callback, state: FSMContext):
    await state.set_state(UserStates.main_menu)
    await message_or_callback.answer(text = "Здравствуйте, рады снова вас видеть!", reply_markup = inline_keyboards.main_menu)

@user_router.callback_query(F.data == "back_to_main_menu")
async def handle_back_to_main_menu(callback: CallbackQuery, state: FSMContext):
    await start_handler(callback.message, state)

@user_router.message(StateFilter("*"), CommandStart())
async def handle_start_message(message: Message, state: FSMContext):
    await start_handler(message, state)

#handling generate avatar
@user_router.callback_query(F.data == "generate")
async def start_generate(call: CallbackQuery, state: FSMContext):
    await call.message.answer(text = "Введите текстовый запрос", reply_markup = inline_keyboards.back_to_main_menu)

#handling profile
@user_router.callback_query(F.data == "profile")
async def start_generate(call: CallbackQuery):
    await call.message.answer(text = "profile")