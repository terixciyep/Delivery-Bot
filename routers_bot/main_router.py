import datetime
import os

from aiogram import types
from aiogram import Router
from aiogram.methods import SendPhoto
from aiogram.types import InputFile

from config import bot
from core import texts
from core.texts import get_waves_text
from db.cursor import cur
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

main_router = Router()


@main_router.message(lambda message: message.text.lower() == 'на старт' or message.text.lower()=='/start')
async def start_command(message: types.Message):
    await message.delete()
    await message.answer(texts.START_COMMAND, parse_mode='HTML')

@main_router.message(lambda message: message.text.lower() == 'доступные волны' or message.text.lower()=='/time')
async def shops_command(message: types.Message):
    await message.delete()
    return SendPhoto(photo='https://github.com/terixciyep/photos/blob/main/time.jpg?raw=true', caption=texts.time_delivery, chat_id=message.from_user.id)


@main_router.message(lambda message: message.text.lower() == 'узнать цены' or message.text.lower()=='/price')
async def shops_command(message: types.Message):
    await message.delete()
    return SendPhoto(photo='https://github.com/terixciyep/photos/blob/main/price.jpg?raw=true', caption=texts.PRICE, chat_id=message.from_user.id)

@main_router.message(lambda message: message.text.lower() == 'магазины для доставки' or message.text.lower()=='/location')
async def shops_command(message: types.Message):
    await message.delete()
    return SendPhoto(photo='https://github.com/terixciyep/photos/blob/main/location.jpg?raw=true', caption=texts.STORES, chat_id=message.from_user.id)



@main_router.message(lambda message: message.text.lower() == 'помощь' or message.text.lower()=='/help')
async def start_command(message: types.Message):
    await message.delete()
    return SendPhoto(photo='https://github.com/terixciyep/photos/blob/main/help.jpg?raw=true', caption=texts.help_command, chat_id=message.from_user.id)

