from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from at_start import at_start
from constants import ANONYM_CHAT_SEARCHING, ANONYM_CHAT

chat_queue = set()

dialogue = dict()
previous_interlocutors = dict()


async def anonym_chat_searching(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id

    chat_queue.add(user_id)
    dialogue[user_id] = ''

    reply_keyboard = [
        ["Выйти из анонимного чата"]
    ]
    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True, one_time_keyboard=True)

    await update.message.reply_text(text="Поиск собеседника...", reply_markup=markup)
    for user in chat_queue:
        if user not in previous_interlocutors[user_id] and user != user_id:
            chat_queue.remove(user)
            chat_queue.remove(user_id)
            reply_keyboard = [
                ["Выйти из анонимного чата", "Следующий собеседник"]
            ]
            markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
            dialogue[user_id] = user
            dialogue[user] = user_id
            await context.bot.send_message(chat_id=user, text="Собеседник найден!", reply_markup=markup)
            await update.message.reply_text(text="Собеседник найден!", reply_markup=markup)
            break
    return ANONYM_CHAT_SEARCHING


async def anonym_chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    user_id = update.effective_user.id
    interlocutor_id = dialogue[user_id]
    if interlocutor_id != '':
        await context.bot.send_message(chat_id=dialogue[user_id], text=text)
    return ANONYM_CHAT


async def next_interlocutor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await dialogue_end(update, context)
    return await anonym_chat_searching(update, context)


async def anonym_chat_exit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await dialogue_end(update, context)
    return await at_start(update, context)


async def dialogue_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        ["Выйти из анонимного чата"]
    ]
    markup = ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True, one_time_keyboard=True)

    user_id = update.effective_user.id
    current_interlocutor = dialogue[user_id]

    if current_interlocutor != '':
        previous_interlocutors[user_id].add(current_interlocutor)
        previous_interlocutors[current_interlocutor].add(user_id)

        chat_queue.add(current_interlocutor)

        dialogue[current_interlocutor] = ''

        await context.bot.send_message(chat_id=current_interlocutor, text="Текущий собеседник окончил диалог(")
        await context.bot.send_message(chat_id=current_interlocutor, text="Поиск собеседника...", reply_markup=markup)
