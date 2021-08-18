from django.db.models.signals import m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import Post, Category
from accounts.models import User
from .tasks import send_mail_new_post  # Импортируем задачу для асинхронной задачи


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
@receiver(m2m_changed, sender=Post.post_category.through)
def notify_new_post(sender, instance, **kwargs):
    # Если тип изменения было добавление, то...
    if kwargs['action'] == "post_add":
        # Наблюдаем категорию, которая была изменена
        change_category = Category.objects.filter(postcategory__post=instance)
        if change_category.count() == 1:
            # Достаем через гет измененную категорию
            category = Category.objects.get(postcategory__post=instance)
            # Собираем всех пользователей, подписанных на данную категорию
            subscribers = User.objects.filter(categorysubscribers__category=category)
            # Создаем список емейл адресов из пользователей
            email_subscribers = []
            for email in subscribers:
                email_subscribers.append(email.email)
            print(email_subscribers)
            # Создаем html для передачи рассылки
            new_post = f' {instance.headline}'
            # Достаем ид добавленной новости, для формирования ссылки
            link = f'{Post.objects.get(postcategory__post=instance).id}'
            category = f'{category}'

            send_mail_new_post.apply_async([email_subscribers, new_post, link, category], countdown = 5)
