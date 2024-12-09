import aiogram
import aiogram.utils
import aiogram.utils.keyboard

from icecream import ic

#----------------------------------------------------MAIN MENU KEYBOARD----------------------------------------
main_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "📃🖌️Сгенерировать изображение", callback_data = "generate"),],
        [aiogram.types.InlineKeyboardButton(text = "👤Профиль", callback_data = "profile"),]
    ]
)

back_to_main_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "⬅️В главное меню", callback_data = "back_to_main_menu"),]
    ]
)
#___________________________________________________GENERATE_____________________________________________________

Generate = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard=[
    [
        [aiogram.types.InlineKeyboardButton(text = "Создать аватарку 📃🖌", callback_data="create_avatar"),],
        [aiogram.types.InlineKeyboardButton(text = "Настройка генерации ⚙️", callback_data="settings"), ],
        [aiogram.types.InlineKeyboardButton(text = "Назад ↩️", callback_data="back")  ,]
    ]
    ]
)


style_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        [aiogram.type.InlineKeyboardButton(text = "Фильмы", callback_data="style_movies"), ],
        [aiogram.type.InlineKeyboardButton(text = "Аниме", callback_data="style_anime"), ],
        [aiogram.type.InlineKeyboardButton(text = "Супергерои", callback_data="style_superheroes"),]
    ],

    [
        InlineKeyboardButton(text = "Назад ↩️", callback_data="back_to_main_menu")
    ]
])
#---------------------------------------------------GENERATE KEYBOARD--------------------------------------------
generate_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "📃🖌️Начать генерацию", callback_data = "generate_image"),],
        [
            aiogram.types.InlineKeyboardButton(text = "✍️Промт", callback_data = "prompt"),
            aiogram.types.InlineKeyboardButton(text = "🎨Cтиль", callback_data = "style"),
            aiogram.types.InlineKeyboardButton(text = "📐Формат", callback_data = "format"),
        ],
        [aiogram.types.InlineKeyboardButton(text = "⬅️В главное меню", callback_data = "back_to_main_menu"),]
    ]
)

generate_menu_format = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [
            aiogram.types.InlineKeyboardButton(text = "1:1", callback_data = "generate_menu_format_1:1"),
            aiogram.types.InlineKeyboardButton(text = "9:16", callback_data = "generate_menu_format_9:16"),
            aiogram.types.InlineKeyboardButton(text = "16:9", callback_data = "generate_menu_format_16:9"),
        ],
        [aiogram.types.InlineKeyboardButton(text = "⬅️Назад", callback_data = "back_to_generate_menu"),]
    ]
)

after_generate_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "🔄Сгенерировать еще раз", callback_data = "generate_another_one"),],
        [aiogram.types.InlineKeyboardButton(text = "⬅️В главное меню", callback_data = "back_to_main_menu"),]
    ]
)

#-----------------------------------------------------PROFILE MENU---------------------------------------------------
#profile menu
profile_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "💵Управление Балансом", callback_data = "balance")],
        [aiogram.types.InlineKeyboardButton(text = "⬅️В главное меню", callback_data = "back_to_main_menu")]
    ]
)

#balance
balance_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "📊Пополнить Баланс", callback_data = "top_up_balance")],
        [aiogram.types.InlineKeyboardButton(text = "⬅️Назад", callback_data = "profile")]
    ]
)

chose_balance_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [
            aiogram.types.InlineKeyboardButton(text = "1 (20 руб)", callback_data = "balance_1_generations"),
            aiogram.types.InlineKeyboardButton(text = "10 (180 руб)", callback_data = "balance_10_generations")
        ],
        [
            aiogram.types.InlineKeyboardButton(text = "25 (400 руб)", callback_data = "balance_25_generations"), 
            aiogram.types.InlineKeyboardButton(text = "50 (800 руб)", callback_data = "balance_50_generations")
        ],
        [
            aiogram.types.InlineKeyboardButton(text = "100 (1650 руб)", callback_data = "balance_100_generations"),
            aiogram.types.InlineKeyboardButton(text = "200 (3500 руб)", callback_data = "balance_200_generations")
        ],
        [
            aiogram.types.InlineKeyboardButton(text = "⬅️Назад", callback_data = "balance")
        ],
    ]
)

back_to_balance_menu = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "⬅️Назад", callback_data = "balance")]
    ]
)

cancel_payment_button = aiogram.types.InlineKeyboardMarkup(
    inline_keyboard = [
        [aiogram.types.InlineKeyboardButton(text = "⬅️Отменить", callback_data = "cancel_payment")]
    ]
)
