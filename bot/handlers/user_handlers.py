#imports
import io
import os
import asyncio
import aiogram

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile, FSInputFile
from aiogram.filters import StateFilter, Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())
from pyexpat.errors import messages
from datetime import datetime

import database

from icecream import ic
from sqlalchemy.ext.asyncio import AsyncSession

from ..keyboards import inline_keyboards
from ..states.user_states import UserStates
from ..filters import chat_type
from ai import AI_Requests

#create new Router for handling user messages
user_router = aiogram.Router()
user_router.message.filter(chat_type.ChatTypeFilter(["private"]))

AI_requests = AI_Requests(api_key = os.getenv("api_key"))

#------------------------------------------------MAIN MENU-------------------------------------------------------
@user_router.message(StateFilter("*"), CommandStart())
async def menu_handle_start_command(message: Message, state: FSMContext, session: AsyncSession):
    if not await database.orm_get_user(session, message.from_user.id):
        data = {
            "id": message.from_user.id,
            "name": message.from_user.username,
            "status_sub": None,
            "balance": 0,
            "image": None,
            "date": datetime.strptime(datetime.now().strftime("%d.%m.%y"), "%d.%m.%y")
        }
        await database.orm_add_user(session, data)

    await state.set_state(UserStates.main_menu)
    await message.answer_photo(photo = FSInputFile("assets\\empty_image.png"))
    await message.answer(text = "Здравствуйте, рады снова вас видеть!\nЧтобы начать, выберите один из вариантов работы с ботом", reply_markup = inline_keyboards.main_menu)

@user_router.callback_query(F.data == "back_to_main_menu")
async def menu_handle_callback(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await call.message.delete()
    await state.set_state(UserStates.main_menu)
    await call.message.answer(text = "Здравствуйте, рады снова вас видеть!\nЧтобы начать, выберите один из вариантов работы с ботом", reply_markup = inline_keyboards.main_menu)

#------------------------------------------------GENERATING-------------------------------------------------------
@user_router.callback_query(F.data == "generate")
async def set_propmt(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
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
#PROFILE MENU
@user_router.callback_query(F.data == "profile")
async def profile_menu(call: CallbackQuery, state: FSMContext , session: AsyncSession):
    """Profile menu"""
    await call.message.delete()
    await state.set_state(UserStates.profile_menu)
    user_data = await database.orm_get_user(session, call.from_user.id)
    await call.message.answer(text = f"Профиль пользователя {user_data.name}:\nID: {user_data.id}",
                              reply_markup = inline_keyboards.profile_menu)

#BALANCE
@user_router.callback_query(StateFilter(UserStates.profile_menu, UserStates.top_up_balance), F.data == "balance")
async def balance_menu(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Balance menu"""
    await state.set_state(UserStates.balance_menu)
    user_data = await database.orm_get_user(session, call.from_user.id)
    await call.message.edit_text(text = f"Текущий баланс: {user_data.balance}", reply_markup = inline_keyboards.balance_menu)

@user_router.callback_query(StateFilter(UserStates.balance_menu), F.data == "top_up_balance")
async def top_up_balance(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Top up the balance, yookassa api"""
    await call.message.delete()
    await state.set_state(UserStates.top_up_balance)
    await call.message.answer(text = "top_up_balance", 
                              reply_markup = inline_keyboards.back_to_balance_menu)

#photo
@user_router.callback_query(StateFilter(UserStates.profile_menu), F.data == "photo")
async def change_photo(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Changing user photo in profile"""
    await state.set_state(UserStates.send_photo)
