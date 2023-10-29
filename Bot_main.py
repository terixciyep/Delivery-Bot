import asyncio
import datetime
import json
import logging

import uvicorn as uvicorn
from aiogram import Bot, Dispatcher, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from core import texts
from core.texts import get_waves_text
from db.cursor import cur
from id_bot import id, NGROK_TUNNEL_URL
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from fastapi import FastAPI
from routers_bot.main_router import main_router
from routers_bot.order_router import order_router
from webhook import WEBHOOK_SECRET
from config import bot

WEBHOOK_PATH = f"/bot/{id}"
WEBHOOK_URL = f"{NGROK_TUNNEL_URL}{WEBHOOK_PATH}"


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(WEBHOOK_URL, secret_token=WEBHOOK_SECRET)

def main() -> None:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage, bot=bot)
    dp.include_routers(main_router, order_router)
    dp.startup.register(on_startup) 
    app = web.Application()
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=WEBHOOK_SECRET,
    )
    webhook_requests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    main()