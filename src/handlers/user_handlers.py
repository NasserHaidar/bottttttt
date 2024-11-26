import aiogram

from aiogram import F
from aiogram.types import Message
from aiogram.filters import StateFilter, Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from icecream import ic

from filters import chat_type

#create new Router for handling user messages
user_router = aiogram.Router()
user_router.message.filter()