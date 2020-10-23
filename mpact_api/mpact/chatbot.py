import os
from datetime import datetime
import telegram.ext
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help! Tell me what you want?')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def callback_minute(context: telegram.ext.CallbackContext):
    """Scheduled for every minute"""
    context.bot.send_message(chat_id="1229987655", text="This message will hit after every 60 seconds")


def main():
    """Start the bot."""
    updater = Updater(os.environ.get('TOKEN'), use_context=True)
    print(f"STARTED {datetime.now()}")

    # Job Queue to schedule the messages
    job_queue = updater.job_queue

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # scheduled job for every minute, starting from 0 (i.e now)
    job_queue.run_repeating(callback_minute, interval=60, first=0)

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()