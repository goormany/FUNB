from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post
from users.models import CustomUser
from django.urls import reverse_lazy
from .tasks import send_mail_new_response, send_mail_accept_response


# в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция,
# и в отправители надо передать также модель
@receiver(m2m_changed, sender=Post.responses.through)
def notify_new_response(sender, instance, **kwargs):
    """отправить письмо автору поста после отклика"""
    # Если тип изменения было добавление, то...
    if kwargs['action'] == "post_add":
        # instance в себе содержит измененный пост
        username = instance.post_author.username
        email = instance.post_author.email
        content = instance.headline
        HOST = 'http://127.0.0.1:8000'
        link = reverse_lazy('profile')
        link = HOST + f'{link}'
        send_mail_new_response.apply_async([email, username, link, content], countdown = 5)


@receiver(m2m_changed, sender=Post.accepted_responses.through)
def notify_accept_response(sender, instance, **kwargs):
    """отправить письмо юзеру оставившего отклик"""
    # Если тип изменения было добавление, то...
    if kwargs['action'] == "post_add":
        # instance в себе содержит измененный пост
        user = instance.accepted_responses.all().order_by('-id')[0]
        username = user.username
        email = user.email
        content = instance.headline
        HOST = 'http://127.0.0.1:8000'
        link = reverse_lazy('post_detail', kwargs={'pk': instance.id})
        link = HOST + f'{link}'
        send_mail_accept_response.apply_async([email, username, link, content], countdown = 5)
