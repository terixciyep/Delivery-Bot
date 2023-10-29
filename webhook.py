from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot
from id_bot import NGROK_TUNNEL_URL


WEBHOOK_SECRET = '123123123'

async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)

async def bot_weebhook(update: dict):
    telegram_update = types.Update(**update)

async def on_shutdown(bot: Bot) -> None:
    await bot.session.close()