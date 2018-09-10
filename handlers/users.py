
import os
import re
import time
import json
from telebot import types


def init_handler(bot):

    monitor = Followers(bot)

    @bot.message_handler(commands=["id"])
    @bot.message_handler_safe
    def _cmd_id(message):
        bot.log(message)
        bot.reply_to(message, '`%d`' % message.from_user.id,
            parse_mode='Markdown')

    @bot.message_handler(commands=["login"])
    @bot.message_handler_safe
    @bot.is_private
    def _cmd_login(message):
        """
        Авторизация пользователя для получения доступа к боту.
        Доступна только в личном чате с ботом.
        """
        if message.from_user.id in bot.config.admins\
        or bot.db.User.is_logged(message.from_user.id):
            return
        msg = bot.reply_to(message, bot.lang.cmd_login_4)
        bot.register_next_step_handler(msg, proc_login)

    @bot.message_handler_safe
    @bot.is_canceled
    def proc_login(message):
        bot.log(message)
        from .contacts import get_contact
        email = message.text.strip().lower()
        if re.search(r'^\S+@\S+$', email) and get_contact(email):
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
            for admin in bot.config.admins:
                try:
                    bot.send_message(admin, bot.lang.cmd_login_6 % (
                        message.from_user.first_name,
                        message.from_user.last_name,
                        message.from_user.username,
                        message.from_user.id,
                        email
                    ), reply_markup=reply_markup)
                except: pass
            bot.reply_to(message, bot.lang.cmd_login_5)
            return
        else:
            msg = bot.reply_to(message, bot.lang.cmd_login_9)
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

    @bot.message_handler(commands=["logout"])
    @bot.message_handler_safe
    @bot.is_private
    @bot.is_logged
    def cmd_logout(message):
        """
        Удалить пользователя.
        Отписаться от сообщений бота.
        Доступна только в личном чате с ботом.
        """
        bot.log(message)
        if message.from_user.id in bot.config.admins\
        or not bot.db.User.is_logged(message.from_user.id):
            return
        msg = bot.reply_to(message, bot.lang.cmd_logout_1)
        bot.register_next_step_handler(msg, proc_logout)

    @bot.message_handler_safe
    @bot.is_canceled
    def proc_logout(message):
        bot.log(message)
        text = message.text.strip().lower()
        if text == bot.lang.cmd_logout_3:
            bot.db.User.logout(message.from_user.id)
            bot.reply_to(message, 'Ok')
            return
        msg = bot.reply_to(message, bot.lang.cmd_logout_2)
        bot.register_next_step_handler(msg, proc_logout)

    @bot.message_handler(commands=["add_user"])
    @bot.message_handler_safe
    @bot.is_private
    @bot.is_admin
    def _cmd_add_user(message):
        """
        Добавление пользователя.
        Доступна только для администратора.
        """
        bot.log(message)
        msg = bot.reply_to(message, bot.lang.cmd_add_user_1)
        bot.register_next_step_handler(msg, proc_add_user)

    @bot.message_handler_safe
    @bot.is_canceled
    def proc_add_user(message):
        bot.log(message)
        email = message.text.strip().lower()
        if re.search(r'^\S+@.*?(?:domru.ru|enforta.com)$', email):
            id = bot.db.User.add(email)
            bot.reply_to(message, id)
            return
        msg = bot.reply_to(message, bot.lang.cmd_add_user_2)
        bot.register_next_step_handler(msg, proc_add_user)

    @bot.message_handler(commands=["status"])
    @bot.message_handler_safe
    @bot.is_admin
    def _cmd_status(message):
        bot.log(message)
        users = bot.db.User.query()
        bot.reply_to(message, '\n'.join([
            'uptime: %dsec' % int(time.time() - bot.start_time),
            'users count: %d' % len(users),
            'active users: %d' % len([u for u in users if u.enabled and u.user_id]),
            'unactive users: %d' % len([u for u in users if not u.user_id]),
            'disabled users: %d' % len([u for u in users if not u.enabled])
        ]))

    @bot.message_handler(commands=["spam"])
    @bot.message_handler_safe
    @bot.is_private
    @bot.is_admin
    def _cmd_spam(message):
        bot.log(message)
        msg = bot.reply_to(message, bot.lang.cmd_spam_1)
        bot.register_next_step_handler(msg, proc_spam)

    @bot.message_handler_safe
    @bot.is_canceled
    def proc_spam(message):
        bot.log(message)
        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.add(types.InlineKeyboardButton(
            bot.lang.cmd_spam_2,
            callback_data='spam_%s' % message.message_id
        ))
        bot.reply_to(message, message.message_id, reply_markup=reply_markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('spam_'))
    def forward_spam(call):
        users = bot.db.User.query(enabled=True)
        for user in [u for u in users if u.user_id != call.message.from_user.id and u.user_id]:
            bot.forward_message(user.user_id, call.message.chat.id, int(call.data[5:]))

    @bot.message_handler(commands=["monitor_on"])
    @bot.message_handler_safe
    @bot.is_admin
    def _cmd_monitor_on(message):
        bot.log(message)
        monitor.append(message.chat.id)

    @bot.message_handler(commands=["monitor_off"])
    @bot.message_handler_safe
    @bot.is_admin
    def _cmd_monitor_off(message):
        bot.log(message)
        monitor.delete(message.chat.id)

    def log(message):
        bot.logger.info("%s:%s: %s",
            message.chat.id,
            message.from_user.id,
            repr(message.text))
        monitor.forward(message)
    bot.log = log

    @bot.job('cron', hour=9)
    def check_users():
        from .contacts import get_contact
        for user in bot.db.User.query(enabled=True):
            if user.level == 'admin':
                continue
            elif user.user_id in bot.config.admins:
                user.level = 'admin'
                bot.db.session.add(user)
            elif not get_contact(user.email):
                user.enabled = False
                bot.db.session.add(user)


class Followers(set):
    def __init__(self, bot):
        self.bot = bot
        self.load()

    def load(self):
        filename = os.path.join(self.bot.config.base_dir, 'followers.json')
        if os.path.exists(filename):
            with open(filename) as f:
                self.update(json.load(f))

    def save(self):
        filename = os.path.join(self.bot.config.base_dir, 'followers.json')
        with open(filename, 'w') as f:
            json.dump(list(self), f)

    def append(self, item):
        self.add(item)
        self.save()

    def delete(self, item):
        self.remove(item)
        self.save()

    def forward(self, msg):
        if msg.chat.id in self or msg.from_user.id in self:
            return
        for follower in self:
            self.bot.forward_message(follower, msg.chat.id, msg.message_id)
