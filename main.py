import asyncio
import aiogram
import aiogram.filters
from config import *

from dotenv import find_dotenv , load_dotenv

from middlewares.db import DataBaseSession

load_dotenv(find_dotenv())
from bot import user_handlers
from database.engine import create_db, drop_db, session_maker

from icecream import ic

from database.engine import create_db, drop_db

#constants
bot = aiogram.Bot(BOT_TOKEN)
dp = aiogram.Dispatcher() #Dispatcher - main Router

dp.include_router(user_handlers.user_router)

async def on_startup(bot):
    run_param= False
    if run_param:
        await drop_db()

    await create_db()

async def on_shutdown(bot):
    print('Бот лег')


#start polling
async def main(): # main async fucntion
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))


    await bot.delete_webhook(drop_pending_updates = True) #delete webhook
    await bot.send_message(chat_id = scpro_developer_chat_id, text = "started") #sending start debug info 
    await dp.start_polling(bot) # start the bot polling

    # Create the database
    await create_db()
    print("Database created successfully!")

if __name__ == "__main__":
    asyncio.run(main())