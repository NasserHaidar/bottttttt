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

balance_values = {"1": 20.0, "10": 180.0, "25": 400.0, "50": 800.0, "100": 1650.0, "200": 3500.0}

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
#@user_router.callback_query(F.data == "generate")
#async def set_propmt(call: CallbackQuery, state: FSMContext, session: AsyncSession):
#    await call.message.delete()
#    await state.set_state(UserStates.prompt)
#
#    await call.message.answer(text = "(1/2) Введите текстовый запрос", reply_markup = inline_keyboards.back_to_main_menu)

#@user_router.message(StateFilter(UserStates.prompt), F.text)
@user_router.callback_query(F.data == "generate")
async def set_image(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await call.message.delete()
    #await state.update_data(prompt = str(message.text))    
    await state.set_state(UserStates.generate_menu)

    await call.message.answer_photo(photo = FSInputFile("assets\\photo_for_avatar_example.jpg", "photo_for_avatar_example.jpg"), 
                               caption = "Отправьте свое изображение, на его основе будет сгенерировано новое", 
                               reply_markup = inline_keyboards.back_to_main_menu)

#GENERATION MENU
@user_router.message(StateFilter(UserStates.generate_menu), F.photo)
async def generate_menu(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()

    if message.photo:
        photo_file_id = message.photo[-1].file_id
        file = await message.bot.get_file(photo_file_id)
        image: io.BytesIO = await message.bot.download_file(file.file_path)
        image = image.getvalue()
        uploaded_image_id = AI_requests.upload_image(image)
        await state.update_data(generate_menu = {"user_image_id": uploaded_image_id, "reference_image_id": ""})

    if data.get("prompt"):
        prompt = data["prompt"]
    else:
        prompt = ""

    await message.answer(text = f"Теперь настроим вашу генерацию\nТекущий промпт - {prompt}", reply_markup = inline_keyboards.generate_menu)

@user_router.callback_query(StateFilter(UserStates.generate_menu), F.data == "back_to_generate_menu")
async def back_to_generate_menu(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await call.message.delete()
    await generate_menu(call.message, state, session)

@user_router.callback_query(StateFilter(UserStates.generate_menu), F.data == "format")
async def generate_menu_format(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await call.message.delete()

    await call.message.answer(text = "Выберите нужный формат иозображения", reply_markup = inline_keyboards.generate_menu_format)

# Сделать стили --------------------------------------------------TODO------------------------------------------------------------ 
@user_router.callback_query(StateFilter(UserStates.generate_menu), F.data == "style")
async def change_style(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await call.message.delete()

    # СПИСОК СТИЛЕЙ СЮДА, ЕСЛИ НУЖНО, СДЕЛАЙ ЕЩЕ ХЕНДЛЕРЫ


async def generate(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    user_data = await database.orm_get_user(session, call.from_user.id)
    current_user_balance = float(user_data.balance)
    try:
        if current_user_balance - 1 >= 0:
            current_user_balance -= 1
            await database.orm_update_user_balance(session = session, user_id = call.message.chat.id, balance = current_user_balance)
            waiting_message = await call.message.answer("Генерация изображения, это может занять некоторое время...")
            await state.update_data(prompt = call.message.text)
            data = await state.get_data()
            images_data = await asyncio.to_thread(AI_requests.generate_image, data["prompt"], data["generate_menu"]["user_image_id"])

            media = []
            for image in images_data:
                media.append(InputMediaPhoto(media = BufferedInputFile(image, f"generated_image_{call.message.chat.id}")))

            await waiting_message.delete()

            await call.message.answer_media_group(media = media)
            await call.message.answer(text = f"Результат генерации по запросу: {data['prompt']}", reply_markup = inline_keyboards.after_generate_menu)
        else:
            await call.message.answer(text = "Не хватает средств на балансе", reply_markup = inline_keyboards.back_to_main_menu)
    except Exception as e:
        await call.message.answer(text = f"Ошибка запроса, возможно, ваш запрос не удовлетворяет правилам площадки, пожалуйста, попробуйте еще раз")
        ic(e)

@user_router.callback_query(StateFilter(UserStates.generate_menu), F.data == "generate_image")
async def generate_handle_state(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await generate(call, state, session)

@user_router.callback_query(F.data == "generate_another_one")
async def generate_handle_callback(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    await generate(call, state, session)

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

    await call.message.edit_text(text = f"Текущий баланс: {user_data.balance} генераций", reply_markup = inline_keyboards.balance_menu)

@user_router.callback_query(StateFilter(UserStates.balance_menu), F.data == "top_up_balance")
async def send_top_up_balance(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Send needly balance to top up"""
    await call.message.delete()
    await state.set_state(UserStates.top_up_balance)

    await call.message.answer(text = "Выбирете нужное количество генераций (одна генерация +-20 рублей)",
                              reply_markup = inline_keyboards.chose_balance_menu)

@user_router.callback_query(StateFilter(UserStates.top_up_balance), F.data.startswith("balance_"))
async def top_up_balance(call: CallbackQuery, state: FSMContext, session: AsyncSession):
    """Top up the balance, yookassa api"""
    value = call.data.split("_")[1]
    user_data = await database.orm_get_user(session, call.from_user.id)
    await call.message.delete()
    try:
        payment = Yokassa.create_payment(
                            amount = balance_values[value],
                            currency = "RUB", 
                            description = f"Order_{call.message.from_user.id}_{datetime.now().strftime('%d.%m.%y')}", 
                            return_url = "https://t.me/Peek_ab0o0_bot"
                        )
        payment_id = payment.id
        await state.update_data(top_up_balance = payment_id)
        payment_url_message = await call.message.answer(text = f"Ссылка на оплату: {payment.confirmation.confirmation_url}", reply_markup = inline_keyboards.back_to_balance_menu)
        while True:
            await asyncio.sleep(1)
            if Yokassa.find_payment(payment_id).status == "succeeded":
                await payment_url_message.delete()
                await database.orm_update_user_balance(session, call.from_user.id, float(user_data.balance) + float(value))
                await call.message.answer(text = f"Баланс генераций успешно пополнен на: {value}", reply_markup = inline_keyboards.back_to_balance_menu)
                break

    except Exception as e:
        await call.message.answer(text = f"Ошибка: {e}")

"""@user_router.callback_query(StateFilter(UserStates.top_up_balance), F.data == "cancel_payment")
async def cancel_payment(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    payment_id = data["top_up_balance"]
    ic(payment_id)
    #Yokassa.cancel_payment(payment_id = payment_id)
    #await balance_menu(message, state, session)"""