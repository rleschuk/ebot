
import re
import random
import requests
from bs4 import BeautifulSoup


def init_handler(bot):

    @bot.message_handler(commands=["gif"])
    @bot.message_handler_safe
    @bot.is_logged
    def cmd_gif(message):
        """
        Рандомные gif
        """
        bot.log(message)
        bot.send_chat_action(message.chat.id, 'typing')
        resource = 'http://www.prikol.ru/tag/gif/page/'
        resources = [resource + str(i) for i in range(1,23)]
        try:
            link = random.choice(resources)

            html = requests.get(link, headers={'User-Agent' : "Magic Browser"}).text
            soup = BeautifulSoup(html, "lxml")
            link = random.choice(soup.find_all('a', rel="bookmark", title=re.compile("Permanent Link")))

            html = requests.get(link.get('href'), headers={'User-Agent' : "Magic Browser"}).text
            soup = BeautifulSoup(html, "lxml")
            imgs = soup.find_all('img', src=re.compile(r'gallery.*gif$'))
            link = random.choice([img.get('src') for img in imgs])

            bot.send_video(message.chat.id, link, timeout=30)
        except Exception as err:
            bot.reply_to(message, bot.lang.error % repr(err))
