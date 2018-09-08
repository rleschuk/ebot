
import re
import random
from telebot import types

from ._netools import IPv4


def init_handler(bot):
    return

    @bot.message_handler(func=lambda x: "/test" in str(x.text))
    @bot.message_handler_safe
    @bot.is_admin
    def test(message):
        bot.log(message)
        #if message.from_user.id in bot.config.admins\
        #or bot.db.User.is_logged(message.from_user.id):
        #    return
        msg = bot.reply_to(message, bot.lang.cmd_login_4)
        bot.register_next_step_handler(msg, proc_login)

    @bot.is_canceled
    def proc_login(message):
        bot.log(message)
        email = message.text.strip().lower()
        if re.search(r'^\S+@\S+$', email):
            id = bot.db.User.add(message.from_user.id, email, **{
                'user_name': message.from_user.username,
                'first_name': message.from_user.first_name,
                'last_name' : message.from_user.last_name,
                'enabled': False
            })
            reply_markup = types.InlineKeyboardMarkup()
            reply_markup.add(
                types.InlineKeyboardButton(bot.lang.cmd_login_7, callback_data='login_1_%s' % id),
                types.InlineKeyboardButton(bot.lang.cmd_login_8, callback_data='login_0_%s' % id),
            )
            bot.send_message(391158244, bot.lang.cmd_login_6 % (
                message.from_user.first_name,
                message.from_user.last_name,
                message.from_user.username,
                message.from_user.id,
                email
            ), reply_markup=reply_markup)
            bot.reply_to(message, bot.lang.cmd_login_5)
            return
        msg = bot.reply_to(message, bot.lang.cmd_add_user_2)
        bot.register_next_step_handler(msg, proc_login)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('login_'))
    def call_login(call):
        id = call.data[8:]
        if call.data.startswith('login_1'):
            user = bot.db.User.enable(id, True)
            bot.send_message(user.user_id, bot.lang.cmd_login_2)
        else:
            user = bot.db.User.enable(id, False)
            bot.send_message(user.user_id, bot.lang.cmd_login_3)
