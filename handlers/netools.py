
import os
import re
import time
import json
import datetime
from threading import Thread
from telebot import types

from utils import Memory
from ._netools import MAC, IPv4, Device


def init_handler(bot):

    @bot.message_handler(commands=["ip"])
    @bot.message_handler_safe
    @bot.is_logged
    def cmd_ip(message):
        """
        Калькулятор IP
        """
        bot.log(message)
        msg = bot.reply_to(message, bot.lang.cmd_ip_1,
            parse_mode='Markdown')
        bot.register_next_step_handler(msg, proc_ip)

    @bot.message_handler_safe
    @bot.is_canceled
    def proc_ip(message):
        bot.log(message)
        try:
            addresses = map(IPv4, IPv4.REGX.findall(message.text))
            if not addresses:
                return bot.reply_to(message, bot.lang.cmd_ip_2)
            for address in addresses:
                bot.reply_to(message, '`%s`' % address.info(), parse_mode='Markdown')
        except Exception as err:
            bot.reply_to(message, bot.lang.error % repr(err))

    @bot.message_handler(commands=["ping"])
    @bot.message_handler_safe
    @bot.is_logged
    def cmd_ping(message):
        """
        Ping указанных адресов.
        Можно вводить несколько адресов через пробел
        или текст содержащий адреса.
        """
        bot.log(message)
        msg = bot.reply_to(message, bot.lang.cmd_ping_1,
            parse_mode='Markdown')
        bot.register_next_step_handler(msg, proc_ping)

    @bot.message_handler_safe
    @bot.is_canceled
    def proc_ping(message):
        bot.log(message)
        addresses = re.findall('(?:[0-9]{1,3}\.){3}[0-9]{1,3}', message.text, re.I)
        if not addresses:
            addresses = message.text.split()
        addresses = addresses[:5]
        for i, address in enumerate(addresses):
            bot.send_chat_action(message.chat.id, 'typing')
            address = address.strip()
            result = IPv4.ping(address)
            addresses[i] = '`%s`' % result
        return bot.reply_to(message, '\n\n'.join(addresses),
            parse_mode='Markdown')

    @bot.message_handler(commands=["trace"])
    @bot.message_handler_safe
    @bot.is_logged
    def cmd_trace(message):
        """
        Traceroute указанных адресов.
        Можно вводить несколько адресов через пробел
        или текст содержащий адреса.
        """
        bot.log(message)
        msg = bot.reply_to(message, bot.lang.cmd_trace_1)
        bot.register_next_step_handler(msg, proc_trace)

    @bot.message_handler_safe
    @bot.is_canceled
    def proc_trace(message):
        bot.log(message)
        addresses = re.findall('(?:[0-9]{1,3}\.){3}[0-9]{1,3}', message.text, re.I)
        if not addresses:
            addresses = message.text.split()
        addresses = addresses[:5]
        for i, address in enumerate(addresses):
            bot.send_chat_action(message.chat.id, 'typing')
            address = address.strip()
            result = IPv4.trace(address)
            addresses[i] = '`%s`' % result
        return bot.reply_to(message, '\n\n'.join(addresses),
            parse_mode='Markdown')

    @bot.message_handler(commands=["whois"])
    @bot.message_handler_safe
    @bot.is_logged
    def cmd_whois(message):
        """
        Whois указанных адресов.
        Можно вводить несколько адресов через пробел.
        """
        bot.log(message)
        msg = bot.reply_to(message, bot.lang.cmd_whois_1)
        bot.register_next_step_handler(msg, proc_whois)

    @bot.message_handler_safe
    @bot.is_canceled
    def proc_whois(message):
        bot.log(message)
        addresses = message.text.split()
        for address in addresses[:3]:
            bot.send_chat_action(message.chat.id, 'typing')
            address = address.strip()
            result = IPv4.whois(address)
            bot.reply_to(message, '%s:\n`%s`' % (address, result),
                parse_mode='Markdown')

    @bot.message_handler(func=lambda m: m.text and m.text.startswith("/mac"))
    @bot.message_handler_safe
    @bot.is_logged
    def cmd_mac(message):
        """
        Узнать вендора по MAC.
        Можно вводить несколько адресов через пробел
        или текст содержащий адреса.
        """
        bot.log(message)
        if len(message.text.split()) > 1:
            return proc_mac(message)
        msg = bot.reply_to(message, bot.lang.cmd_mac_1)
        bot.register_next_step_handler(msg, proc_mac)

    @bot.message_handler_safe
    @bot.is_canceled
    def proc_mac(message):
        bot.log(message)
        addresses = MAC.REGX.findall(message.text)
        if addresses:
            addresses = [re.sub('\.|-|:|\s+','',a)[:6]+'0'*6 for a in addresses]
            addresses = [a for i,a in enumerate(addresses) if a not in addresses[:i]]
            for i, address in enumerate(sorted(addresses)):
                bot.send_chat_action(message.chat.id, 'typing')
                address = address.strip()
                result = MAC.vendor(address)
                addresses[i] = '`%s: %s`' % (address, result)
            return bot.reply_to(message, '\n'.join(addresses), parse_mode='Markdown')
        return bot.reply_to(message, bot.lang.cmd_mac_2)

    @bot.message_handler(commands=["public"])
    @bot.message_handler_safe
    @bot.is_logged
    def cmd_public(message):
        """
        Поиск свободных публичный сетей на R1
        """
        bot.log(message)
        reply_markup = types.InlineKeyboardMarkup()
        reply_markup.add(types.InlineKeyboardButton(bot.lang.cmd_public_3,
            url=bot.lang.cmd_public_4))
        msg = bot.reply_to(message, bot.lang.cmd_public_1,
            reply_markup=reply_markup)

    
