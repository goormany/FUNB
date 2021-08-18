from allauth.account.forms import SignupForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import User
from django.forms import TextInput, PasswordInput, EmailInput, DateTimeInput
from django.forms import ModelForm


# Метод переопределяет форму регистрации через allauth. Достаем пользователя из реквест, достаем группу
# common через гет, в эту группу добавляем пользователя
class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        # Также создаем профиль для нового пользователя
        return user


# Форма редактирования профиля пользователя
class EditForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'birth_date','email',]

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'введите логин'
            }),
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ваше имя'
            }),
            'last_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ваше имя'
            }),
            'birth_date': DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ваше имя'
            }),
        }


# Стандартный метод регистрации джанго. В данном проекте не используется
class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'password1', 'password2']

        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'введите логин'
            }),
            'first_name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ваше имя'
            }),
            'password1': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'не менее 8 символов'
            }),
            'password2': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'повторите пароль'
            }),
        }
