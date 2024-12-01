import os
import asyncio
import aiogram
import aiogram.filters

from YooKassa import YooKassaPayment

from bot import user_handlers

from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from icecream import ic

from database.engine import create_db, drop_db, session_maker
from middlewares.db import DataBaseSession

#constants
bot = aiogram.Bot(os.getenv("BOT_TOKEN"))
dp = aiogram.Dispatcher() #Dispatcher - main Router

dp.include_router(user_handlers.user_router)

async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()
    await create_db()

async def on_shutdown(bot):
    ic("Bot was shutdown")

#start polling
async def main(): # main async fucntion
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool = session_maker))

    await bot.delete_webhook(drop_pending_updates = True) #delete webhook
    await bot.send_message(chat_id = os.getenv("scpro_developer_chat_id"), text = "started") #sending start debug info 
    await dp.start_polling(bot) # start the bot polling

    # Create the database
    try:
        await create_db()
        ic("Database created successfully")
    except DataBaseSession as e:
        raise DataBaseSession(f"Failed to create database: {e}")


    # Initialize the payment processor
    payment_processor = YooKassaPayment(account_id = os.getenv('YOOKASSA_SHOP_ID'),
                                         secret_key = os.getenv('YOOKASSA_SECRET_KEY'))

    # Example of creating a payment
    payment = payment_processor.create_payment(
        amount = 100.00,
        currency = 'RUB',
        description = 'Order No. 1',
        return_url = 'https://www.example.com/return_url'
    )

    print(f"Payment created: {payment}")


if __name__ == "__main__":
    asyncio.run(main())