from asyncore import dispatcher
from cgitb import text
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s- %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text('bot started')

def set_user(update, context):
    user_id = str(context.args[0])
    if user_id:
        f = open('user.txt', 'w')
        f.write(user_id)

def echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    f = open('user.txt', 'r')
    user_id = f.read()
    if user_id:
        chat_id = user_id
    
    context.bot.send_message(chat_id=chat_id, text=update.message.text)



def main():
    updater = Updater('your_token')

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('setUser', set_user))
    
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
