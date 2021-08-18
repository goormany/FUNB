from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import pgettext_lazy



class User(AbstractUser):
    photo = models.ImageField(upload_to='accounts/image/%Y/%m/%d', blank=True)
    birth_date = models.DateField(blank=True, null=True,
                                  verbose_name=pgettext_lazy('help text for MyModel model', 'Дата рождения',),)


    @staticmethod
    def get_absolute_url():
        return '/profile'