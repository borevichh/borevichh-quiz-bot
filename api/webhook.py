import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    Update,
)

WEBAPP_URL = os.getenv("WEBAPP_URL", "https://borevichh.github.io/borevichh-quiz/").strip()

dp = Dispatcher()
app = FastAPI()


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎮 Открыть borevichh quiz",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ]
    )
    await message.answer(
        "⚽ <b>borevichh quiz — 7 Edition</b>\n\n"
        "13 интеллектуальных игр (20+), бесконечный режим, Блиц 3:00 и Шахматы vs ИИ.\n"
        "Нажмите кнопку ниже, чтобы запустить игру прямо в Telegram:",
        reply_markup=kb,
        parse_mode="HTML",
    )


@app.post("/api/webhook")
async def telegram_webhook(request: Request):
    token = os.getenv("BOT_TOKEN", "").strip()
    bot = Bot(token=token)
    try:
        data = await request.json()
        update = Update.model_validate(data, context={"bot": bot})
        await dp.feed_update(bot, update)
    finally:
        await bot.session.close()
    return {"ok": True}


@app.get("/")
async def healthcheck():
    token = os.getenv("BOT_TOKEN", "").strip()
    return {
        "status": "running",
        "has_token": bool(token),
        "token_valid_format": ":" in token,
    }
