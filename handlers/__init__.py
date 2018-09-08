
import os
import re
import traceback
import importlib
from telebot import types
from functools import wraps


def init_handlers(bot):

    def is_logged(func):
        @wraps(func)
        def wrapped(message, *args, **kwargs):
            if message.from_user.id in bot.config.admins or\
               bot.db.User.is_logged(message.from_user.id):
                return func(message, *args, **kwargs)
            bot.logger.info("%s:%s: access denied %s",
                message.chat.id,
                message.from_user.id,
                repr(message.text))
            for admin in bot.config.admins:
                try: bot.forward_message(admin, message.chat.id, message.message_id)
                except: pass
        return wrapped
    bot.is_logged = is_logged

    def is_admin(func):
        @wraps(func)
        def wrapped(message, *args, **kwargs):
            if message.from_user.id in bot.config.admins or\
               bot.db.User.is_admin(message.from_user.id):
                return func(message, *args, **kwargs)
            bot.logger.info("%s:%s: access denied %s",
                message.chat.id,
                message.from_user.id,
                repr(message.text))
        return wrapped
    bot.is_admin = is_admin

    def is_private(func):
        @wraps(func)
        def wrapped(message, *args, **kwargs):
            if message.chat.id >= 0:
                return func(message, *args, **kwargs)
        return wrapped
    bot.is_private = is_private

    def is_canceled(func):
        @wraps(func)
        def wrapped(message, *args, **kwargs):
            if not str(message.text).strip().lower().startswith('/cancel'):
                return func(message, *args, **kwargs)
            bot.log(message)
        return wrapped
    bot.is_canceled = is_canceled

    def message_handler_safe(func):
        @wraps(func)
        def wrapped(message, *args, **kwargs):
            try: return func(message, *args, **kwargs)
            except Exception:
                tb = traceback.format_exc().strip()
                bot.logger.error('error in handler %s\n%s', func.__name__, tb)
                for admin in bot.config.admins:
                    try: bot.send_message(admin, 'error in handler %s\n%s' % (func.__name__, tb))
                    except: pass
        return wrapped
    bot.message_handler_safe = message_handler_safe

    def log(message):
        bot.logger.info("%s:%s: %s",
            message.chat.id,
            message.from_user.id,
            repr(message.text))
    bot.log = log

    def job(*args, **kwargs):
        def decorator(func):
            bot.scheduler.add_job(func, *args, id=func.__name__, name=func.__name__, **kwargs)
            return func
        return decorator
    bot.job = job

    for mod_name in os.listdir(os.path.dirname(__file__)):
        if mod_name.startswith('_') or not mod_name.endswith('.py'): continue
        try:
            mod_full_name = '%s.%s' % (__name__, mod_name[:-3])
            mod = importlib.import_module(mod_full_name)
            mod.init_handler(bot)
            bot.logger.info('init handler %s', mod_full_name)
        except Exception:
            tb = traceback.format_exc()
            bot.logger.error('%s\n%s', mod_name, tb.strip())

    @bot.message_handler(commands=["start", "help", "h"])
    @bot.message_handler_safe
    @bot.is_logged
    def _cmd_start(message):
        """
        Стартовая команда бота.
        Справка о боте и его командах.
        """
        bot.log(message)
        bot.send_chat_action(message.chat.id, 'typing')
        commands = []
        for i, handler in enumerate(bot.message_handlers):
            name = handler['function'].__name__
            if not name.startswith('cmd_'): continue
            doc = handler['function'].__doc__
            if doc is None or doc.strip() == '':
                doc = bot.lang.cmd_start_2
            doc = re.sub('\n\s+', '\n', doc).strip()
            commands.append("/%s\n%s\n" % (name[4:], doc))
        bot.reply_to(message,
            '%s\n\n%s' % (bot.lang.cmd_start_1, '\n'.join(commands)))

    @bot.message_handler(func=lambda message: True)
    @bot.message_handler_safe
    def all_message(message):
        bot.log(message)
