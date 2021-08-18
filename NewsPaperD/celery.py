import os
# импортируем библиотеку для взаимодействия с операционной системой и саму библиотеку Celery.
from celery import Celery
from celery.schedules import crontab

# связываем настройки Django с настройками Celery через переменную окружения.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaperD.settings')

# создаем экземпляр приложения Celery и устанавливаем для него файл конфигурации
app = Celery('NewsPaperD')
app.config_from_object('django.conf:settings', namespace='CELERY')
# указываем Celery автоматически искать задания в файлах tasks.py каждого приложения проекта.
app.autodiscover_tasks()

# Добавляем периодическую задачу для еженедельной рассылки
app.conf.beat_schedule = {
    'weekly_newsletter': {
        'task': 'news.tasks.newsletter',
        'schedule': crontab(minute='0', hour='8', day_of_week='mon'),
    },
}