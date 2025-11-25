from aiogram import Bot, types
from aiogram.client.default import DefaultBotProperties
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "8586920536:AAHmc9iFU073Zvj-Ebt9G9OtSut9FsWxB0c"
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))

async def send_user_message(chat_id: int, product_name: str, start_parameter: str):

    # Сырая кнопка Mini App
    raw_keyboard = {
        "inline_keyboard": [
            [
                {
                    "text": "Открыть приложение",
                    "request_main_web_view": {
                        "bot_username": "more_stars_bot",
                        "start_parameter": start_parameter,
                        "mode": "fullscreen"
                    }
                }
            ]
        ]
    }

    # Создаём клавиатуру БЕЗ валидации aiogram
    keyboard = InlineKeyboardMarkup.model_construct(**raw_keyboard)

    await bot.send_message(
        chat_id=chat_id,
        text=f"🎉 Оплата за <b>{product_name}</b> прошла успешно!",
        reply_markup=keyboard
    )