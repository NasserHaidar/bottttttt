#imports
import aiogram

from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter, Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from icecream import ic

from keyboards import inline_keyboards

from filters import chat_type

#create new Router for handling user messages
user_router = aiogram.Router()
user_router.message.filter()

#handling /start command
@user_router.message(StateFilter("*"), CommandStart())
async def start(message: Message):
    await message.answer(text = "Здравствуйте, рады снова вас видеть!", reply_markup = inline_keyboards.start_keyboard)

