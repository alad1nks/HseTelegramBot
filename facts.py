from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from constants import FACTS, FACTS_END

fact_file = open("facts.txt", "r", encoding="UTF-8")
fact_list = [s.replace("\n", "") for s in fact_file.readlines()]


async def facts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    facts_iterator = context.user_data["facts_iterator"]
    context.user_data["facts_iterator"] += 1
    if facts_iterator < len(fact_list):
        reply_keyboard = [
            ["Назад", "Следующий факт"]
        ]
        markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            fact_list[facts_iterator],
            reply_markup=markup,
        )
        return FACTS
    else:
        reply_keyboard = [
            ["Назад"]
        ]
        markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            "Факты закончились(",
            reply_markup=markup,
        )
        return FACTS_END
