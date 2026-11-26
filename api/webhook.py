import html
import os
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
    Update,
)

BASE_URL = os.getenv("WEBAPP_URL", "https://borevichh.github.io/borevichh-quiz/").strip().rstrip("/") + "/"

dp = Dispatcher()
app = FastAPI()


def build_main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎮 Играть • borevichh quiz #7",
                    web_app=WebAppInfo(url=BASE_URL),
                )
            ],
            [
                InlineKeyboardButton(
                    text="♟️ Шахматы vs ИИ",
                    web_app=WebAppInfo(url=f"{BASE_URL}?mode=chess"),
                ),
                InlineKeyboardButton(
                    text="⚡ Блиц 3:00",
                    web_app=WebAppInfo(url=f"{BASE_URL}?mode=blitz"),
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📲 Поделиться игрой с друзьями",
                    switch_inline_query="Сыграем в borevichh quiz #7? 13 игр, Блиц 3:00 и Шахматы vs ИИ ⚽♟️",
                )
            ],
        ]
    )


@dp.message(CommandStart())
async def cmd_start(message: Message) -> None:
    first_name = html.escape(message.from_user.first_name) if message.from_user else "Игрок"
    text = (
        f"👋 <b>Привет, {first_name}!</b>\n"
        f"Добро пожаловать в <b>borevichh quiz — 7 Edition</b> ⚽\n\n"
        f"Внутри тебя ждут <b>13 интеллектуальных режимов (20+)</b>:\n"
        f"• ♟️ <b>Шахматы vs ИИ</b> — 3 уровня сложности + разбор ходов\n"
        f"• ⚡ <b>Блиц 3:00</b> — спринт на скорость и реакцию\n"
        f"• 🔐 <b>Пароль, Судоку, Связи, Криптограмма</b> и ещё 7 игр\n"
        f"• 🏆 Уровни XP, серия побед, подсказки и достижения\n\n"
        f"<i>Выбирай режим кнопкой ниже или жми синюю кнопку «Играть» в меню:</i>"
    )
    await message.answer(
        text,
        reply_markup=build_main_keyboard(),
        parse_mode="HTML",
    )


@dp.message(Command("play"))
async def cmd_play(message: Message) -> None:
    await message.answer(
        "🚀 <b>Запускай матч!</b> Нажми кнопку ниже:",
        reply_markup=build_main_keyboard(),
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
    return {"status": "running"}
