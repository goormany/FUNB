# Фан блог
![picture](https://crownenglishclub.ru/wp-content/uploads/2020/02/76723bac02e0e6a353f3ade7aab8906c.png)

### Инструкции по запуску приложения:

1. Установите в систему Redis:\
$ sudo apt-get update\
$ sudo apt-get install redis\
затем запустите его:\
$ redis-server

2. Создайте виртуальное окружение и установите необходимые пакеты для работы приложения:\
pip3 install -r requirements.txt\
Дождитесь окончания установки всех зависимостей.

3. Настройте почтовый сервер!\
 Для этого перейдите в папку ad_board/secret. Создайте 4 текстовых файла с названием
* ADMINS.txt  -- Здесь нужно записать почту администраторов в виде кортежа: ('John', 'john@example.com'), ('Mary', 'mary@example.com')
* EMAIL_HOST.txt -- Здесь нужно записать smtp сервер почты
* EMAIL_HOST_PASSWORD.txt  -- Здесь нужно записать пароль от почтового ящика
* EMAIL_HOST_USER.txt  -- Здесь нужно записать логин от почтового ящика

4. Из корня проекта сдлайте миграции и запустите сервер. Корнем считается тот каталог, где находиться файл manage.py:\
python3 manage.py migrate\
python3 manage.py runserver

5. Из корня проекта запустите Celery:\
celery -A slackbot worker -l INFO -B

6. Откройте браузер и перейдите на адрес:\
http://127.0.0.1:8000/

На этом приложение установлено и запущено. 

Если нужно использовать базу данных postgresql, в settings.py нужно раскомментировать соответствующий блок и закомментировать базу sqllite3. Команды для быстрого создания таблицы в postgresql находятся в commands.md
