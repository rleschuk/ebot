
import re
import random
import requests
from bs4 import BeautifulSoup


def init_handler(bot):

    @bot.message_handler(func=lambda x: x.text and (x.text == "/boobs" or\
                                        re.search("сиськ", x.text, re.I)))
    @bot.message_handler_safe
    @bot.is_logged
    def cmd_boobs(message):
        """
        Рандомные boobs
        """
        bot.log(message)
        bot.send_chat_action(message.chat.id, 'typing')
        site = 'http://bombler.ru'
        resource = site + '/girls/page/'
        resources = [resource + str(i) + '/' for i in range(1,85)]
        try:
            link = random.choice(resources)

            html = requests.get(link, headers={'User-Agent' : "Magic Browser"}).text
            soup = BeautifulSoup(html, "lxml")
            h2 = random.choice(soup.find_all('h2'))
            link = h2.find('a').get('href')

            html = requests.get(link, headers={'User-Agent' : "Magic Browser"}).text
            soup = BeautifulSoup(html, "lxml")
            imgs = soup.find_all('img', alt=h2.text, title=h2.text)
            link = random.choice([site + img.get('src') for img in imgs])

            bot.send_photo(message.chat.id, link)
        except Exception as err:
            bot.reply_to(message, bot.lang.error % repr(err))
