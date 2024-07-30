
from telegram import *
from telegram.ext import *

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Я твой Telegram бот.')

def main():
    updater = Updater("7362467897:AAHrluc3JLzPq7XXOGZ5V--6zUPXx4GC8fI", use_context=True)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
