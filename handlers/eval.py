
import re
import random
import string
import math
from telebot import types
from pyfiglet import figlet_format

from ._netools import IPv4


def init_handler(bot):

    @bot.message_handler(commands=['eval'])
    @bot.message_handler_safe
    @bot.is_logged
    def cmd_eval(message):
        bot.log(message)
        msg = bot.reply_to(message, bot.lang.cmd_eval_1)
        bot.register_next_step_handler(msg, proc_eval)

    @bot.is_canceled
    def proc_eval(message):
        bot.log(message)
        try:
            result = eval(message.text, {
                'IPv4': IPv4,
                're': re,
                'random': random,
                'string': string,
                'math': math,
                'figlet_format': figlet_format
            }, {})
            bot.reply_to(message, '`%s`' % str(result), parse_mode='Markdown')
        except Exception as err:
            bot.reply_to(message, repr(err))
