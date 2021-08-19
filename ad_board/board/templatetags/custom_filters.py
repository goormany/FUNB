from django import template
from board.models import Category


register = template.Library()


@register.simple_tag()
def get_categories():
    """вернуть список всех категории"""
    return Category.objects.all()


@register.filter(name='get_responsers')
def get_responsers(post):
    """вернуть список откликнувшихся пользователей"""
    user_list = []
    # достаем все связанные пользователи строки модели
    responses = post.responses.all().values('username')
    for response in responses:
        user_list.append(response.get('username'))
    return user_list # возвращает список пользователей


@register.filter(name='get_accepted_responses')
def get_accepted_responses(post):
    """вернуть список принятых откликов пользователей"""
    user_list = []
    # достаем все связанные пользователи строки модели
    responses = post.accepted_responses.all().values('username')
    for response in responses:
        user_list.append(response.get('username'))
    return user_list # возвращает список пользователей
    