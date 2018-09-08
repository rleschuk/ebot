
import os
import time

import click
import requests
import telebot
from apscheduler.schedulers.background import BackgroundScheduler
from telebot import apihelper
from dotenv import load_dotenv

load_dotenv()
from config import get_config
from lang import lang
from db import DB
from handlers import init_handlers

import logging
logger = logging.getLogger(__name__)
logging.getLogger('sqlalchemy').propagate = False
logging.getLogger('apscheduler').propagate = False
logging.getLogger('sshtunnel').propagate = False
logging.getLogger('paramiko').propagate = False


def create_bot(config):
    config_ = get_config(config)

    logger.setLevel(config_.log_level)
    formatter = logging.Formatter(config_.log_format)
    #fhandler = logging.FileHandler(config_.log_file)
    #fhandler.setLevel(config_.log_level)
    #fhandler.setFormatter(formatter)
    #logger.addHandler(fhandler)
    shandler = logging.StreamHandler()
    shandler.setLevel(config_.log_level)
    shandler.setFormatter(formatter)
    logger.addHandler(shandler)

    apihelper.proxy = config_.proxy

    bot = telebot.TeleBot(config_.token,
        threaded     = config_.bot_threaded,
        skip_pending = config_.bot_skip_pending,
        num_threads  = config_.bot_num_threads
    )
    bot.logger = logger
    bot.scheduler = BackgroundScheduler()
    bot.config = config_
    bot.lang = lang()
    bot.db = DB(config_)

    init_handlers(bot)

    return bot


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        run()


@cli.command()
@click.option('--config', default=os.getenv('CONFIG', 'default'),
              help='configuration')
def initdb(config):
    db = DB(get_config(config))
    db.create_all()
    click.echo('Initialized the database')


@cli.command()
def dropdb():
    click.echo('Dropped the database')


@cli.command()
@click.option('--config', default=os.getenv('CONFIG', 'default'),
              help='configuration')
def run(config):
    bot = create_bot(config)
    bot.start_time = time.time()
    if bot.config.bot_scheduler:
        bot.scheduler.start()
    for admin in bot.config.admins:
        try: bot.send_message(admin, 'bot started')
        except: pass
    bot.polling(
        none_stop = bot.config.bot_polling_none_stop,
        interval  = bot.config.bot_polling_interval,
        timeout   = bot.config.bot_polling_timeout)


if __name__ == '__main__':
    cli()
