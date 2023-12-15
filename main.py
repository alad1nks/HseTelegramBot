import logging
from typing import Dict

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

CHOOSING, FACTS, FACTS_END, TYPING_REPLY, TYPING_CHOICE = range(5)

file = open("facts.txt", "r", encoding="UTF-8")
fact_list = [s.replace("\n", "") for s in file.readlines()]
print(fact_list)


def facts_to_str(user_data: Dict[str, str]) -> str:
    facts = [f"{key} - {value}" for key, value in user_data.items()]
    return "\n".join(facts).join(["\n", "\n"])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    user_data["facts_iterator"] = 0
    reply_keyboard = [
        ["Анонимный чат", "Интересные факты"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Привет! Чем займемся сегодня?",
        reply_markup=markup,
    )

    return CHOOSING


async def anonym_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"Your {text.lower()}? Yes, I would love to hear about that!")

    return TYPING_REPLY


async def facts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    facts_iterator = context.user_data["facts_iterator"]
    context.user_data["facts_iterator"] += 1
    if facts_iterator < len(fact_list):
        reply_keyboard = [
            ["Назад", "Следующий факт"]
        ]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            fact_list[facts_iterator],
            reply_markup=markup,
        )
        return FACTS
    else:
        reply_keyboard = [
            ["Назад"]
        ]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        await update.message.reply_text(
            "Факты закончились(",
            reply_markup=markup,
        )
        return FACTS_END


async def facts_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    reply_keyboard = [
        ["Анонимный чат", "Интересные факты"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    await update.message.reply_text(
        "Чем займемся?",
        reply_markup=markup,
    )

    return CHOOSING


async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Store info provided by user and ask for the next category."""
    user_data = context.user_data
    text = update.message.text
    category = user_data["choice"]
    user_data[category] = text
    del user_data["choice"]
    reply_keyboard = [
        ["Анонимный чат", "Интересные факты"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    await update.message.reply_text(
        "Neat! Just so you know, this is what you already told me:"
        f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
        " on something.",
        reply_markup=markup,
    )

    return CHOOSING


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token("6765009066:AAGE2xWB8_M5HojuaAC4dNMd_z2mMzwcmMo").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(filters.Regex("^Анонимный чат$"), anonym_chat),
                MessageHandler(filters.Regex("^Интересные факты$"), facts)
            ],
            FACTS: [
                MessageHandler(filters.Regex("^Назад$"), facts_end),
                MessageHandler(filters.Regex("^Следующий факт$"), facts)
            ],
            FACTS_END: [
                MessageHandler(filters.Regex("^Назад$"), facts_end)
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), anonym_chat
                )
            ],
            TYPING_REPLY: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
                    received_information,
                )
            ],
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
