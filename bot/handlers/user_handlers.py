#imports
import io
import os
import asyncio
import aiogram

from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile, FSInputFile, InputMediaPhoto, InputFile
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
from YooKassa import YooKassaPayment

#create new Router for handling user messages
user_router = aiogram.Router()
user_router.message.filter(chat_type.ChatTypeFilter(["private"]))

AI_requests = AI_Requests(api_key = os.getenv("api_key"))
Yokassa = YooKassaPayment(account_id = os.getenv("test_shop_id"), secret_key = os.getenv("test_secret_key"))

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

    await message.answer(text = "Здравствуйте, рады снова вас видеть!\nЧтобы начать, выберите один из вариантов работы с ботом",
                         reply_markup = inline_keyboards.main_menu)

@user_router.callback_query(F.data == "back_to_main_menu")
async def menu_handle_callback(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await call.message.delete()
    await state.set_state(UserStates.main_menu)

    await call.message.answer(text = "Здравствуйте, рады снова вас видеть!\nЧтобы начать, выберите один из вариантов работы с ботом",
                              reply_markup = inline_keyboards.main_menu)

#------------------------------------------------GENERATING-------------------------------------------------------
@user_router.callback_query(F.data == "generate")
async def set_propmt(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await call.message.delete()
    await state.set_state(UserStates.prompt)

    await call.message.answer(text = "Введите текстовый запрос", reply_markup = inline_keyboards.back_to_main_menu)

async def generate(message: Message, state: FSMContext, session: AsyncSession):
    user_data = await database.orm_get_user(session, message.from_user.id)
    current_user_balance = float(user_data.balance)
    try:
        if current_user_balance - 50.0 > 0:
            current_user_balance -= 50.0
            await database.orm_update_user_balance(balance = current_user_balance)
            waiting_message = await message.answer("Генерация изображения, это может занять некоторое время...")
            await state.update_data(prompt = message.text)
            data = await state.get_data()
            images_data = await asyncio.to_thread(AI_requests.generate_image, data["prompt"], user_data.image)

            media = []
            for image in images_data:
                media.append(InputMediaPhoto(media = BufferedInputFile(image, f"generated_image_{message.from_user.id}")))

            await waiting_message.delete()

            await message.answer_media_group(media = media)
            await message.answer(text = f"Результат генерации по запросу: {data['prompt']}", reply_markup = inline_keyboards.after_generate_menu)
        else:
            await message.answer(text = "Не хватает средств на балансе", reply_markup = inline_keyboards.back_to_main_menu)
    except:
        await message.answer(text = f"Ошибка запроса, возможно, ваш запрос не удовлетворяет правилам площадки, пожалуйста, попробуйте еще раз")
@user_router.message(StateFilter(UserStates.prompt), F.text)
async def generate_handle_state(message: Message, state: FSMContext, session: AsyncSession):
    await generate(message, state, session)

@user_router.callback_query(F.data == "generate_another_one")
async def generate_handle_callback(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await generate(call.message, state, session)

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

    await call.message.edit_text(text = f"Текущий баланс: {user_data.balance} руб.", reply_markup = inline_keyboards.balance_menu)

@user_router.callback_query(StateFilter(UserStates.balance_menu), F.data == "top_up_balance")
async def send_top_up_balance(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Send needly balance to top up"""
    await call.message.delete()
    await state.set_state(UserStates.top_up_balance)

    await call.message.answer(text = "Введите сумму пополнения (Минимальная сумма пополнения 10 рублей, максимальная 100 000 рублей)", 
                              reply_markup = inline_keyboards.back_to_balance_menu)

@user_router.message(StateFilter(UserStates.top_up_balance), F.text)
async def top_up_balance(message: Message, state: FSMContext, session: AsyncSession):
    """Top up the balance, yookassa api"""
    user_data = await database.orm_get_user(session, message.from_user.id)

    await message.delete()
    try:
        if float(message.text) <= 100000.0 and float(message.text) >= 10.0:
            payment = Yokassa.create_payment(amount = float(message.text), 
                                currency = "RUB", 
                                description = f"Order_{message.from_user.id}_{datetime.now().strftime('%d.%m.%y')}", 
                                return_url = "https://t.me/Peek_ab0o0_bot")
            payment_id = payment.id
            await state.update_data(top_up_balance = payment_id)
            payment_url_message = await message.answer(text = f"Ссылка на оплату: {payment.confirmation.confirmation_url}", reply_markup = inline_keyboards.back_to_balance_menu)
            while True:
                await asyncio.sleep(1)
                if Yokassa.find_payment(payment_id).status == "succeeded":
                    await payment_url_message.delete()
                    await database.orm_update_user_balance(session, message.from_user.id, float(user_data.balance) + float(message.text))
                    await message.answer(text = f"Баланс успешно пополнен на: {message.text} руб.", reply_markup = inline_keyboards.back_to_balance_menu)
                    break
        else:
            await message.answer(text = "Минимальная сумма пополнения 10 рублей, максимальная 100 000 рублей")
    except ValueError:
        await message.answer(text = "Вы ввели не число, попробуйте еще раз")

"""@user_router.callback_query(StateFilter(UserStates.top_up_balance), F.data == "cancel_payment")
async def cancel_payment(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    payment_id = data["top_up_balance"]
    ic(payment_id)
    #Yokassa.cancel_payment(payment_id = payment_id)
    #await balance_menu(message, state, session)"""

#PHOTO
@user_router.callback_query(StateFilter(UserStates.profile_menu, UserStates.send_photo), F.data == "photo")
async def change_photo(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Changing user photo in profile"""
    await call.message.delete()
    await state.set_state(UserStates.photo_menu)

    await call.message.answer(text = "Выберите действие", reply_markup = inline_keyboards.photo_menu)

@user_router.callback_query(StateFilter(UserStates.photo_menu), F.data == "show_photo")
async def show_photo(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Show user photo"""
    
    await call.message.delete()
    await state.set_state(UserStates.send_photo)
    user_data = await database.orm_get_user(session, call.from_user.id)

    image_bytes = AI_requests.get_image(image_id = user_data.image)

    if user_data.image:
        await call.message.answer_photo(photo = BufferedInputFile(image_bytes, f"user_image_{user_data.id}"), 
                                        caption = "Вот ваше фото", 
                                        reply_markup = inline_keyboards.back_to_photo_menu)
    else:
        await call.message.answer(text = "Вы еще не поставили фото", reply_markup = inline_keyboards.back_to_photo_menu)

@user_router.callback_query(StateFilter(UserStates.photo_menu), F.data == "new_photo")
async def send_photo(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Send photo to change"""
    await call.message.delete()
    await state.set_state(UserStates.send_photo)

    await call.message.answer(text = "Отправьте фото, которое хотите установить, как по умолчанию", reply_markup = inline_keyboards.back_to_photo_menu)

@user_router.message(StateFilter(UserStates.send_photo), F.photo)
async def handling_send_photo(message: Message, state: FSMContext, session: AsyncSession):
    """Processing a photo sent by a user"""
    photo_file_id = message.photo[-1].file_id

    try:
        file = await message.bot.get_file(photo_file_id)
        image: io.BytesIO = await message.bot.download_file(file.file_path)
        image = image.getvalue()

        status, image_id = AI_requests.upload_image(image)
        ic(status)
        await database.orm_update_user_image(session, message.from_user.id, image_id)
        await message.answer(text = "Фото успешно установлено", reply_markup = inline_keyboards.back_to_photo_menu)

    except Exception as e:
        ic(f"An error occurred: {e}")
        await message.answer("Произошла ошибка при обработке вашей фотографии.")
