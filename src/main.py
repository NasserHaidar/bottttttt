import asyncio
import aiogram
import aiogram.filters
from config import *

from icecream import ic

#constants
bot = aiogram.Bot(BOT_TOKEN)
dp = aiogram.Dispatcher() #Dispatcher - main Router

#start polling
async def main(): # main async fucntion
    await bot.delete_webhook(drop_pending_updates = True) #delete webhook
    await bot.send_message(chat_id = scpro_developer_chat_id, text = "started") #sending start debug info 
    await dp.start_polling(bot) # start the bot polling

asyncio.run(main())