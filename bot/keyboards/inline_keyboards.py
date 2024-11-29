import aiogram
import aiogram.utils
import aiogram.utils.keyboard

from icecream import ic

#----------------------------------------------------MAIN MENU KEYBOARD----------------------------------------
main_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [
            aiogram.types.InlineKeyboardButton(text = "📃🖌️ Создать аватарку 📃🖌️", callback_data = "generate"),
        ],
        [
            aiogram.types.InlineKeyboardButton(text = "👤 Профиль 👤", callback_data = "profile"),
        ]
    ]
)

back_to_main_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [
            aiogram.types.InlineKeyboardButton(text = "В главное меню", callback_data = "back_to_main_menu"),
        ]
    ]
)

#---------------------------------------------------GENERATE KEYBOARD--------------------------------------------
generate_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [
            aiogram.types.InlineKeyboardButton(text = "Промт", callback_data = "generate"),
        ],
        [
            aiogram.types.InlineKeyboardButton(text = "Cтиль", callback_data = "style"),
        ]
    ]
)

after_generate_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [
            aiogram.types.InlineKeyboardButton(text = "Сгенерировать еще раз", callback_data = "generate_another_one"),
        ],
        [
            aiogram.types.InlineKeyboardButton(text = "В главное меню", callback_data = "back_to_main_menu"),
        ]
    ]
)

#-----------------------------------------------------PROFILE MENU---------------------------------------------------
profile_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [
            aiogram.types.InlineKeyboardButton(text = "Управление Балансом", callback_data = "subscribe")
        ],
        [
            aiogram.types.InlineKeyboardButton(text = "Установить Фото", callback_data = "photo")
        ]
    ]
)