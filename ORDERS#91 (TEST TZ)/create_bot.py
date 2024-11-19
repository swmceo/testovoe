import os
from data import config
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(token=config.TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())