from telegram import ReplyKeyboardMarkup
from telegram.ext import Filters, MessageHandler, Updater, CommandHandler


TOKEN = '5361232542:AAHPXl8NMHL2hwl2pShFcGa-am59i-u7yCg'
ALL_CHAT_ID = '@with_tutor_rep'
TEXT = 'Ваше обращение обрабатывается, скоро вам напишет наш специалист.'
ID_AND_QUESTION = {}
NUMBER_OF_ASKS = {}

updater = Updater(token=TOKEN)


def bot_started(update, context):
    chat_id = update.effective_chat.id
    message = 'Задайте ваш вопрос и вам напишет специалист'
    context.bot.send_message(
        chat_id=chat_id,
        text=message
    )


def save_person(chat_id, message):
    if chat_id in ID_AND_QUESTION:
        ID_AND_QUESTION[chat_id].append(message)
    else:
        ID_AND_QUESTION[chat_id] = [message]
    if chat_id in NUMBER_OF_ASKS:
        NUMBER_OF_ASKS[chat_id] += 1
        return
    NUMBER_OF_ASKS[chat_id] = 1


def get_current_questions(update, context):
    context.bot.send_message(
        chat_id=ALL_CHAT_ID,
        text=ID_AND_QUESTION
    )


def ask_closed(update, context):
    chat_id = update.effective_chat.id
    try:
        to_be_deleted_id = update.message.text.split()[1]
        del ID_AND_QUESTION[int(to_be_deleted_id)]
    except Exception as error:
        message = f'Что-то не так: {error}'
        context.bot.send_message(
            chat_id=chat_id,
            text=message
        )
    else:
        message = 'Временный ID был удален'
        context.bot.send_message(
            chat_id=chat_id,
            text=message
        )


def send_client_to_chat(update, context):
    chat = update.effective_chat
    chat_id = chat.id
    message = update.message.text
    space = '  ' * 150
    asks = NUMBER_OF_ASKS.get(chat_id, 0)
    name = chat.username
    text = (f'Пришло сообщение от пользователя: ----{chat_id}----, ----@{name}---- '
            f'Колличество заданных вопросов: --{asks}--'
            f'{space}'
            f'------------{message}------------')
    try:
        context.bot.send_message(
            chat_id=ALL_CHAT_ID,
            text=text)
        context.bot.send_message(
            chat_id=chat_id,
            text=TEXT
        )
        save_person(chat_id, message)
    except Exception:
        context.bot.send_message(
            chat_id=chat_id,
            text=('Неккоректно составлено сообщение'
                  '(возможно оно слишком длинное)')
        )


def send_buttons_to_chat(update, context):
    button = ReplyKeyboardMarkup([['/delete', '/get_answers']])
    context.bot.send_message(
        chat_id=ALL_CHAT_ID,
        text='Кнопки включены',
        reply_markup=button
        )


def main():
    updater.dispatcher.add_handler(CommandHandler(
        'start',
        bot_started
    ))
    updater.dispatcher.add_handler(CommandHandler(
        'get_buttons',
        send_buttons_to_chat))
    updater.dispatcher.add_handler(CommandHandler(
        'get_answers',
        get_current_questions))
    updater.dispatcher.add_handler(CommandHandler(
        'delete',
        ask_closed))
    updater.dispatcher.add_handler(MessageHandler(
        Filters.text,
        send_client_to_chat))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
