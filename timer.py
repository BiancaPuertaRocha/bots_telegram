from asyncore import dispatcher
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s- %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

USER_ID = None

def start(update, context):
    update.message.reply_text('hi! define yor time /set <seconds>')

def alarm(context):
    job = context.job
    context.bot.send_message(job.context, text='beeeeeeeep')

def remove_job_if_exists(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)

    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    
    return True

def set_timer(update, context):
    chat_id = update.message.chat_id

    try:
        due = int(context.args[0])
        if due < 0:
            update.message.reply_text('sorry, thats wrong')
            return 

        job_removed = remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(alarm, due, context=chat_id, name=str(chat_id))

        text = 'defined'

        if job_removed:
            text += 'old removed'
        
        update.message.reply_text(text)
    except (IndexError, ValueError):
        update.message.reply_text('Usage /set <seconds>')

def unset(update, context):
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = 'removed' if job_removed else 'not found'
    update.message.reply_text(text)

def set_user(update, context):
    USER_ID = str(context.args[0])
    if not USER_ID:
        USER_ID = None

def main():
    updater = Updater('your_token')

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('selp', start))
    dispatcher.add_handler(CommandHandler('set', set_timer))
    dispatcher.add_handler(CommandHandler('unset', unset))
    dispatcher.add_handler(CommandHandler('setUser', set_user))
    

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
