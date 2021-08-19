from allauth.account.forms import LoginForm, SignupForm, BaseSignupForm
from django import forms
from django.forms import ModelForm, CharField, TextInput, EmailInput, FileInput, PasswordInput, EmailField
from django.core.exceptions import ValidationError
from .models import CustomUser
from board.models import Post


class UserForm(ModelForm):
    """Модельная форма редактировать профиль"""

    class Meta:
        model = CustomUser

        fields = ['username', 'first_name', 'last_name', 'email', 'photo', ]

        labels = {'username': 'Логин', 'first_name': 'Имя',
                    'last_name': 'Фамилия', 'email': 'email', 'photo': 'Аватарка', }

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'readonly': 'readonly',
                'style': 'width:40ch ',
            }),
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...',
                'style': 'width:40ch',
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите текст...',
                'style': 'width:40ch',
            }),
            'email': EmailInput(attrs={
                'multiple class': 'form-control',
                'style': 'width:40ch',
            }),
            'photo': FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите рисунок',
                'style': 'width:40ch',
            }),
        }

    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        # Достать всех пользователей с таким email, кроме себя
        if CustomUser.objects.filter(email=email).exclude(username=username).exists():
            raise ValidationError('Пользователь с таким email уже зарегистрирован')
        return email


class MyLoginForm(LoginForm):
    # условие для применения ACCOUNT_FORMS в settings
    """Переопределить форму вхожа allauth"""
    def __init__(self, *args, **kwargs):
        super(MyLoginForm, self).__init__(*args, **kwargs)

        self.fields['login'] = CharField(
            label=("E-MAIL"), widget=TextInput(attrs={'class': 'form-control', }))
        self.fields['password'].widget = PasswordInput(
            attrs={'class': 'form-control', })


class MySignupForm(SignupForm):
    # можно по разному переопределять форму. Так:
    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                "type": "email",
                "placeholder": "E-mail address",
                "autocomplete": "email",
            }
        )
    )
    # или так:
    def __init__(self, *args, **kwargs):
        super(MySignupForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget = PasswordInput(
            attrs={'class': 'form-control', })
        self.fields['password2'].widget = PasswordInput(
            attrs={'class': 'form-control', })
