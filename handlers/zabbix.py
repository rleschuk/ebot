
import re
import os
import time
import requests
from telebot import types

ZABBIX_ADD_IP='http://10.66.4.203:8080/api/add_public_ip?ip=%s'

def init_handler(bot):

    @bot.message_handler(commands=["zabbix_add_ip"])
    @bot.message_handler_safe
    @bot.is_logged
    def cmd_zabbix_add_ip(message):
        """
        Постановка на мониторинг в zabbix ip адреса
        """
        bot.log(message)
        msg = bot.reply_to(message, bot.lang.cmd_zabbix_add_ip_1)
        bot.register_next_step_handler(msg, proc_zabbix_add_ip)

    @bot.message_handler_safe
    @bot.is_canceled
    def proc_zabbix_add_ip(message):
        bot.log(message)
        m = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', message.text)
        if not m:
            msg = bot.reply_to(message, bot.lang.cmd_zabbix_add_ip_3)
            bot.register_next_step_handler(msg, proc_zabbix_add_ip)
            return
        url = ZABBIX_ADD_IP % m.group(1)
        r = requests.get(url).json()
        reply_markup = types.InlineKeyboardMarkup()
        for device in r['devices']:
            reply_markup.add(types.InlineKeyboardButton(device['name'], url=device['url']))
        bot.reply_to(message, bot.lang.cmd_zabbix_add_ip_2,
            reply_markup=reply_markup)
