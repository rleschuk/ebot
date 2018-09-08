
import re
import requests

from utils import Memory


class MAC(object):
    REGX = re.compile(r'\b(?:[0-9a-f]{2}(?::|-|\.| )?){5}[0-9a-f]{2}\b', re.I)

    @staticmethod
    @Memory.limited(10000)
    def vendor(address):
        url = "https://api.macvendors.com/%s" % address
        while True:
            resp = requests.get(url, timeout=(5, 5))
            if resp.status_code == 200:
                return resp.text
            elif resp.status_code == 429:
                time.sleep(0.1)
                continue
            return 'not found'
