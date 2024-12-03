import aiogram
import aiogram.utils
import aiogram.utils.keyboard

from icecream import ic

#----------------------------------------------------MAIN MENU KEYBOARD----------------------------------------
main_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "📃🖌️ Создать аватарку 📃🖌️", callback_data = "generate"),],
        [aiogram.types.InlineKeyboardButton(text = "👤 Профиль 👤", callback_data = "profile"),]
    ]
)

back_to_main_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "В главное меню", callback_data = "back_to_main_menu"),]
    ]
)

#---------------------------------------------------GENERATE KEYBOARD--------------------------------------------
generate_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "Промт", callback_data = "generate"),],
        [aiogram.types.InlineKeyboardButton(text = "Cтиль", callback_data = "style"),]
    ]
)

after_generate_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "Сгенерировать еще раз", callback_data = "generate_another_one"),],
        [aiogram.types.InlineKeyboardButton(text = "В главное меню", callback_data = "back_to_main_menu"),]
    ]
)

#-----------------------------------------------------PROFILE MENU---------------------------------------------------
#profile menu
profile_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "Управление Балансом", callback_data = "balance")],
        [aiogram.types.InlineKeyboardButton(text = "Фото", callback_data = "photo")],
        [aiogram.types.InlineKeyboardButton(text = "В главное меню", callback_data = "back_to_main_menu")]
    ]
)

#balance
balance_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "Пополнить Баланс", callback_data = "top_up_balance")],
        [aiogram.types.InlineKeyboardButton(text = "Назад", callback_data = "profile")]
    ]
)

back_to_balance_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "Назад", callback_data = "balance")]
    ]
)

cancel_payment_button = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "Отменить", callback_data = "cancel_payment")]
    ]
)

#photo
photo_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "Посмотреть текущее Фото", callback_data = "show_photo")],
        [aiogram.types.InlineKeyboardButton(text = "Установить новое Фото", callback_data = "new_photo")],
        [aiogram.types.InlineKeyboardButton(text = "Назад", callback_data = "profile")]
    ]
)

back_to_photo_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "Назад", callback_data = "photo")]
    ]
)