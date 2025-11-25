from aiogram import Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8586920536:AAHmc9iFU073Zvj-Ebt9G9OtSut9FsWxB0c"
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

async def send_user_message(chat_id: int):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть мини-приложение",
                    request_main_web_view={
                        "url": "https://t.me/more_stars_bot?startapp&mode=compact"
                    }
                )
            ]
        ]
    )

    await bot.send_message(
        chat_id,
        "Нажми кнопку для открытия мини-приложения:",
        reply_markup=keyboard
    )