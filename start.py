from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from anonym_chat import previous_interlocutors
from constants import CHOOSING


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    user_data = context.user_data
    user_data["facts_iterator"] = 0
    previous_interlocutors[user_id] = set()
    reply_keyboard = [
        ["Анонимный чат", "Интересные факты"]
    ]
    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text(
        "Привет! Чем займемся сегодня?",
        reply_markup=markup,
    )

    return CHOOSING
