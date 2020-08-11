import urllib.request
import urllib.parse
import json
import os
import logging
import sys
"""
    Need  env[DEEPL_AUTH_KEY]
"""


class DeepL():
    def __init__(self):
        if 'DEEPL_AUTH_KEY' in os.environ:
            self.auth_key = os.environ['DEEPL_AUTH_KEY']
        else:
            msg = "\nSet the DEEPL_AUTH_KEY environment variable.\n"
            print(msg)
            logging.info(msg)
            sys.exit()

    def translateText(self, msg):
        URL = "https://api.deepl.com/v2/translate"
        TARGET_LANG = "JA"
        data = urllib.parse.urlencode({
            'auth_key': self.auth_key,
            'target_lang': TARGET_LANG,
            'text': msg
        }).encode('utf-8')
        request = urllib.request.Request(URL, data)
        response = urllib.request.urlopen(request)
        if response.getcode() == 200:
            ret = json.loads(response.read().decode('utf-8'))
            return (ret["translations"][0]["text"])
        else:
            return ("ERROR")
