import aiogram
import aiogram.utils
import aiogram.utils.keyboard

from icecream import ic

#main menu keyboard
main_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [
            aiogram.types.InlineKeyboardButton(text = "Создать аватарку", callback_data = "generate"),
            aiogram.types.InlineKeyboardButton(text = "Профиль", callback_data = "profile"),
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