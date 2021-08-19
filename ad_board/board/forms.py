from django.forms import ModelForm, Select, TextInput, SelectMultiple, Textarea, FileInput, CharField
# Для загрузки изображении локально
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Post, Category, Comments
import re
from django.core.exceptions import ValidationError


class PostForm(ModelForm):
    """Создать модельную форму"""

    content = CharField(
        label='Содержание', widget=CKEditorUploadingWidget(), required=False)

    class Meta:
        model = Post

        fields = ['headline', 'content', 'post_picture', 'post_category', ]
        
        labels = {'post_author': 'Автор', 'headline': 'Заголовок',
                  'post_picture': 'Картинка на превью', 'post_category': 'Выберите категорию', }

        widgets = {
            'headline': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...'
            }),
            'post_category': Select(attrs={
                'multiple class': 'form-control',
            }),
            'post_picture': FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите рисунок'
            }),
        }

    # def clean_headline(self):
    #     """кастомный валидатор"""
    #     headline = self.cleaned_data['headline']
    #     if re.match(r'\d', headline):
    #         raise ValidationError('Название не должно начинаться с цифры')
    #     return headline


class CategoryForm(ModelForm):
    """Создать модельную форму"""

    class Meta:
        model = Category
        fields = ['category', ]

        widgets = {
            'category': TextInput(attrs={
                'class': 'form-control',
                'option selected': 'Категория'
            }),
        }


class CommentForm(ModelForm):
    """Создать модельную форму"""

    class Meta:
        model = Comments
        fields = ['comment_text', ]

        widgets = {
            'comment_text': Textarea(attrs={
                'class': 'form-control',
                'option selected': 'Комментарии'
            }),
        }

