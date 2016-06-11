# -*- coding: utf-8 -*-
import logging

import telegram
from telegram.ext import Updater, CommandHandler

from settings import TOKEN, UPDATE_TIME

logger = logging.getLogger(__name__)


class BoomStarterMoneyBot(object):
    CHATS = {}
    MONEY = 0
    OLD_MONEY = 0

    def __init__(self):
        # Create the EventHandler and pass it your bot's token.
        updater = Updater(TOKEN)
        self.job_queue = updater.job_queue

        # Get the dispatcher to register handlers
        dp = updater.dispatcher

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("stop", self.stop))

        # log all errors
        dp.add_error_handler(self.error)

        # Start the Bot
        updater.start_polling()

        # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
        # SIGTERM or SIGABRT. This should be used most of the time, since
        # start_polling() is non-blocking and will stop the bot gracefully.
        updater.idle()

    def start(self, bot, update):
        self.CHATS[update.message.chat_id] = ''
        chat_id = update.message.chat_id
        bot.sendMessage(
            chat_id,
            text='Welcome to fate core boomstarter! Now we getting *%s r*!' % self.MONEY,
            parse_mode=telegram.ParseMode.MARKDOWN)

        def alert(self, bot):
            """ Inner function to send the alarm message """
            if self.MONEY > self.OLD_MONEY:
                self.OLD_MONEY = self.MONEY
                bot.sendMessage(
                    chat_id, text='Now we getting *%s r*!' % self.MONEY,
                    parse_mode=telegram.ParseMode.MARKDOWN)

        self.job_queue.put(alert, UPDATE_TIME, repeat=True)

    def stop(self, bot, update):
        self.CHATS.pop(update.message.chat_id)
        bot.sendMessage(chat_id=update.message.chat_id, text='farewell')

    def error(self, bot, update, error):
        logger.warn('Update "%s" caused error "%s"' % (update, error))

if __name__ == '__main__':
    BoomStarterMoneyBot()
