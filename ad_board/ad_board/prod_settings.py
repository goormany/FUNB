import os
from pathlib import Path
from colorama import Fore, Style


BASE_DIR = Path(__file__).resolve().parent.parent

try:
    with open(os.path.join(BASE_DIR, 'secret/SECRET_KEY.txt'), 'r') as token:
        secret = token.read()
    SECRET_KEY = secret  # адрес сервера почты для всех один и тот же
except FileNotFoundError:
    print(Fore.RED + 'Не найден файл для SECRET_KEY')
    print(Style.RESET_ALL)
    SECRET_KEY = 'sefesfsefsefsfesff'

DEBUG = False

ALLOWED_HOSTS = ['185.23.108.189', 'localhost', '127.0.0.1']

# Настройки для базы данных на Postgresql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ad_board_db',
        'USER': 'ad_board',
        'PASSWORD': 'ad_board',
        'HOST': 'localhost',
        'PORT': '5432',
    },
}

STATIC_DIR = os.path.join(BASE_DIR, 'board/static/')
STATICFILES_DIRS = [STATIC_DIR,]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
