
import os
import re


class Config:
    base_dir = os.path.abspath(os.path.dirname(__file__))
    log_level = os.getenv('LOG_LEVEL') or 'INFO'
    log_format = '%(asctime)s %(levelname)s %(message)s'
    bot_polling_none_stop = True
    bot_polling_interval = 1
    bot_polling_timeout = 60
    bot_threaded = True
    bot_skip_pending = True
    bot_num_threads = 4
    bot_scheduler = True
    dburi = 'sqlite:///db/ebot.db'
    proxy = {
        'https': os.getenv('HTTPS_PROXY') or '',
        'ssh': os.getenv('SSH_PROXY') or ''
    }
    admins = list(map(int, os.getenv('ADMINS').split(','))) if os.getenv('ADMINS') else []

    @classmethod
    def get_ssh_proxy(cls):
        m = re.search(r'^(?:(\S+?):(\S+?)@)?(\S+?)(?::(\d+))?$', cls.proxy.get('ssh', ''))
        return {
            'host': m.group(3),
            'port': int(m.group(4)) or 22,
            'user': m.group(1),
            'pass': m.group(2)
        } if m else None


class Development(Config):
    token = os.getenv('DEV_TOKEN') or ''
    bot_scheduler = False


class Production(Config):
    token = os.getenv('TOKEN')
    bot_num_threads = 10


def get_config(config='default'):
    return {
        'default': Development,
        'development': Development,
        'production': Production
    }.get(config) or Development
