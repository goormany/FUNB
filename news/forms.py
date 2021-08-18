from django.forms import ModelForm
from .models import Post
from django.forms import Select, TextInput, SelectMultiple, Textarea, FileInput


# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета как обычно надо написать модель по которой будет строится форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['headline', 'post_text', 'post_category', 'post_picture',]

        widgets = {
            'headline': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название статьи или новости'
            }),
            'post_text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...'
            }),
            'post_author': Select(attrs={
                'class': 'custom-select',
                'option selected': 'Выбрать автора'
            }),
            'post_category': SelectMultiple(attrs={
                'multiple class': 'form-control',
            }),
            'post_picture': FileInput(attrs={
                'class': 'custom-select',
                'placeholder': 'Выберите рисунок'
            }),
        }
