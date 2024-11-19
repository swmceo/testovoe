from aiogram.utils import executor
from create_bot import dp
from create_bot import bot
from handlers import client
import logging


async def on_startup(_):
    print('work')

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)