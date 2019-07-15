import json
import requests
from flask_babel import _
from flask import current_app


def get_yandex_key():
    if 'YA_TRANSLATOR_KEY' not in current_app.config or not current_app.config['YA_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    return current_app.config['YA_TRANSLATOR_KEY']


def translate(text, source_language, dest_language):
    key = get_yandex_key()
    lang = source_language + '-' + dest_language
    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate?key={}&text={}&lang={}'
                     .format(key, text, lang))
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    jesonString = json.loads(r.content.decode('utf-8-sig'))
    return jesonString['text']


def guess_my_language(text):
    key = get_yandex_key()
    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/detect?key={}&text={}'
                     .format(key, text))
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    jesonString = json.loads(r.content.decode('utf-8-sig'))
    return jesonString['lang']