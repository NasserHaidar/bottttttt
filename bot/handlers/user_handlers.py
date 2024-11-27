#imports
import io
import os
import asyncio
import aiogram

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, BufferedInputFile, FSInputFile
from aiogram.filters import StateFilter, Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from dotenv import find_dotenv , load_dotenv
from pyexpat.errors import messages

from database.orm_query import orm_add_user, orm_get_user

load_dotenv(find_dotenv())

from icecream import ic
from sqlalchemy.ext.asyncio import AsyncSession

from ..keyboards import inline_keyboards
from ..states.user_states import UserStates
from ..filters import chat_type
from ai import AI_Requests

from dotenv import api_key
from database.models.user import User

from database import session_maker


#create new Router for handling user messages
user_router = aiogram.Router()
user_router.message.filter(chat_type.ChatTypeFilter(["private"]))

AI_requests = AI_Requests(api_key = os.getenv("api_key"))



#------------------------------------------------MAIN MENU-------------------------------------------------------
async def start_handler(message: Message, state: FSMContext):
    await state.set_state(UserStates.main_menu)
    await message.answer_photo(photo = FSInputFile("assets\\empty_image.png"),
                               caption = "Здравствуйте, рады снова вас видеть!",
                               reply_markup = inline_keyboards.main_menu)

@user_router.callback_query(F.data == "back_to_main_menu")
async def menu_handle_callback(callback: CallbackQuery, state: FSMContext):
    await start_handler(callback.message, state)

@user_router.message(StateFilter("*"), CommandStart())
async def menu_handle_start_command(message: Message, state: FSMContext):
    await start_handler(message, state)

#------------------------------------------------GENERATING-------------------------------------------------------
@user_router.callback_query(F.data == "generate")
async def start_generate(call: CallbackQuery, state: FSMContext):
    await state.set_state(UserStates.prompt)
    await call.message.answer(text = "Введите текстовый запрос", reply_markup = inline_keyboards.back_to_main_menu)

async def generate(message: Message, state: FSMContext):
    waiting_message = await message.answer("Генерация изображения, это может занять некоторое время...")

    await state.update_data(prompt = message.text)
    data = await state.get_data()
    image_data = await asyncio.to_thread(AI_requests.imitation_generate_image, data["prompt"], AI_requests.dalle2)
    image = BufferedInputFile(image_data, f"generated_image_{message.from_user.id}")

    await waiting_message.delete()
    await message.answer_photo(photo = image, reply_markup = inline_keyboards.after_generate_menu)

@user_router.message(StateFilter(UserStates.prompt), F.text)
async def generate_handle_state(message: Message, state: FSMContext):
    await generate(message, state)

@user_router.callback_query(F.data == "generate_another_one")
async def generate_handle_callback(call: CallbackQuery, state: FSMContext):
    await generate(call.message, state)

#-------------------------------------------------PROFILE---------------------------------------------------------
@user_router.callback_query(F.data == "profile")
async def profile_menu(call: CallbackQuery, state: FSMContext , session: AsyncSession ):

    await state.update_data(image=messages.photo[-1].file_id)

    await call.message.answer(text = f"Профиль пользователя: {call.from_user.username}",
                              reply_markup = inline_keyboards.profile_menu)
    data = await state.get_data()

    await orm_add_user(session, data)

    await state.clear()