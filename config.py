import os

from aiogram import Bot
from aiogram.enums import ParseMode
from id_bot import id

bot = Bot(id, parse_mode=ParseMode.HTML)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
