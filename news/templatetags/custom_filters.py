import json, os
from django import template
from django.conf import settings
from datetime import datetime
from django.utils import dateformat


# если мы не зарегестрируем наши фильтры, то django никогда не узнает где именно их искать фильтры
register = template.Library()


# Фильтрация цензурных слов
@register.filter(name='censor')
def censor(value):
    path = settings.BASE_DIR / 'news/static/news/Bad_Word_List.txt'

    # Открываем файл с цензурой и декодируем через json
    with open(path, 'r') as f:
        data = json.loads(f.read())
    # Составляем множество из цензурныв слов
    bad_word_dict = set()
    for i in data:
        bad_word_dict.add(i['fields']['word'])
    # Достаем фильтруемый текст и передаем множеству
    target_text = set(value.split(' '))
    # Если есть пересечение текста с цензурой, то достаем этот текс в виде списка
    if target_text.intersection(bad_word_dict):
        bad_words = list(target_text.intersection(bad_word_dict))
    # Каждое слово из списка меняем на ***
        for i in bad_words:
            value = value.replace(i, '[ censored ]')
    # Возвращаем отредактированный текст
    return value


# Фильтрация цензурных слов
@register.filter(name='date_translate')
def date_translate(value):
    formatted_date = dateformat.format(datetime.now(), settings.DATE_FORMAT)
    print(formatted_date)
