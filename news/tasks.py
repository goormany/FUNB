from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.utils.timezone import localtime
from django.conf import settings
from accounts.models import User
from news.models import Post, Category


# Функция для асинхронной отправки емейл сообщения при добавления новости
@shared_task
def send_mail_new_post(email_subscribers, new_post, link, category):
    # Собираем контексты для html странички в емейл
    html_content = render_to_string('news/mailing_new_content.html',
                                    {
                                        'new_post': new_post, 'link': link, 'category': category})
    # Собираем тело сообщения
    msg = EmailMultiAlternatives(
        subject=f'Появились обновления в категории на которую вы подписаны',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=email_subscribers,
    )
    msg.attach_alternative(html_content, "text/html")  # добавляем html
    msg.send()  # отсылаем
    print(f'Письмо отправлено {email_subscribers}')


# Отправка письма при подписке пользователя на категорию
@shared_task
def send_mail_subscribe(category, email):
    send_mail( # отправляем письмо
        subject=f'Уважаемый пользователь ', # имя
        message=f'Вы были подписаны на категорию {category}',  # сообщение с кратким описанием
        from_email=settings.DEFAULT_FROM_EMAIL,  # здесь указываете почту
        recipient_list=[email, ]  # здесь список получателей
            )
    print(f'письмо о подписке отправлено {email}')


# Отправка письма при отписке пользователя из категории
@shared_task
def send_mail_unsubscribe(category, email):
    send_mail( # отправляем письмо
        subject=f'Уважаемый пользователь  ', # имя
        message=f'Вы успешно отписались из категории {category}',  # сообщение с кратким описанием
        from_email=settings.DEFAULT_FROM_EMAIL,  # здесь указываете почту
        recipient_list=[email, ]  # здесь список получателей
            )
    print(f'письмо об отписке отправлено {email}')


# Еженедельная рассылка
@shared_task
def newsletter():
    print(f'Start at {localtime()}')
    # Если день недели воскресенье
    if datetime.isoweekday(datetime.now()) == 1:
        # Высчитываем время 7 дней назад
        week = localtime() - timedelta(days=7)
        # По очереди берем каждую категорию, и делаем рассылку его подписчикам
        categories = Category.objects.all()
        for category in categories:
            # Берем всех подписчиков этой темы, и создаем список почтовых адресов
            subscribers = User.objects.filter(categorysubscribers__category=category)
            subscribers_emails = []
            for user in subscribers:
                subscribers_emails.append(user.email)
                # Достаем все новости этой категории за последние 7 дней
                post_list = Post.objects.filter(postcategory__category=category, date_create__gt=week)
                print(post_list)

                # HTML страница для мыло
                html_content = render_to_string('news/weekly_newsletter.html',
                                                {'posts': post_list, 'category': category,})
                # Достаем
                # Собираем тело сообщения
                msg = EmailMultiAlternatives(
                    subject=f'Все новости за прошедшую неделю',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=subscribers_emails,
                )
                msg.attach_alternative(html_content, "text/html")  # добавляем html
                msg.send()  # отсылаем
                print('Еженедльная рассылка успешна отправлена')
