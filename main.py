from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from anonym_chat import anonym_chat_searching, anonym_chat, next_interlocutor, anonym_chat_exit
from at_start import at_start
from constants import CHOOSING, FACTS, FACTS_END, ANONYM_CHAT, ANONYM_CHAT_SEARCHING, TYPING_CHOICE
from facts import facts
from start import start
from token import TOKEN


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_data = context.user_data
    if "choice" in user_data:
        del user_data["choice"]

    await update.message.reply_text(
        f"I learned these facts about you: Until next time!",
        reply_markup=ReplyKeyboardRemove(),
    )

    user_data.clear()
    return ConversationHandler.END


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(filters.Regex("^Анонимный чат$"), anonym_chat_searching),
                MessageHandler(filters.Regex("^Интересные факты$"), facts)
            ],
            ANONYM_CHAT_SEARCHING: [
                MessageHandler(filters.Regex("^Выйти из анонимного чата$"), anonym_chat_exit),
                MessageHandler(filters.Regex("^Следующий собеседник$"), next_interlocutor),
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), anonym_chat
                )
            ],
            ANONYM_CHAT: [
                MessageHandler(filters.Regex("^Выйти из анонимного чата$"), anonym_chat_exit),
                MessageHandler(filters.Regex("^Следующий собеседник$"), next_interlocutor),
                MessageHandler(
                    filters.TEXT & ~filters.COMMAND, anonym_chat
                )
            ],
            FACTS: [
                MessageHandler(filters.Regex("^Назад$"), at_start),
                MessageHandler(filters.Regex("^Следующий факт$"), facts)
            ],
            FACTS_END: [
                MessageHandler(filters.Regex("^Назад$"), at_start)
            ],
            TYPING_CHOICE: [
                MessageHandler(
                    filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), anonym_chat
                )
            ]
        },
        fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
