# Generated by Django 3.1.7 on 2021-04-16 23:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('board', '0013_auto_20210416_2232'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='responses',
            field=models.ManyToManyField(related_name='response', to=settings.AUTH_USER_MODEL, verbose_name='отклики'),
        ),
    ]