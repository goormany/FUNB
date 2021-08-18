from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter, get_account_adapter
from django.contrib.auth.models import Group
from .models import User


# функция переопределения редиректов allauth
class MyAccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        path = "/news"
        return path

    def get_logout_redirect_url(self, request):
        path = "/news"
        return path

    def get_signup_redirect_url(self, request):
        path = "/news"
        return path


# функция переопределения формы регистрации allauth через соц сети
class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        # с помощью super выполняем свой код библиотеки, и дальнее добавим свой
        u = super(SocialAccountAdapter,self).save_user(request, sociallogin, form=None)
        # Вытаскиваем из бд группу common и прикрепляем к нему нового пользователя
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(u)
        return u
