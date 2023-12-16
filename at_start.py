from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from constants import CHOOSING


async def at_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [
        ["Анонимный чат", "Интересные факты"]
    ]
    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "Чем займемся?",
        reply_markup=markup,
    )

    return CHOOSING
