# Generated by Django 3.1.7 on 2021-04-11 16:49

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_auto_20210411_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='Текст'),
        ),
    ]