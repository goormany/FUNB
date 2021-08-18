from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.views.generic import ListView, UpdateView
from django.utils import timezone
import pytz

from news.models import Author
from news.models import Category
from .forms import EditForm
from .models import User


# Кабинет пользователя
class UserProfile(LoginRequiredMixin, ListView):
    model = User
    template_name = 'accounts/cabinet.html'
    context_object_name = 'profile'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context['user'] = User.objects.get(username=self.request.user)
        category = Category.objects.filter(subscribers=self.request.user)
        # _________________________________________
        # Блок для получения подписанных категории
        list_category = []
        for i in category:
            list_category.append(str(i))
        context['category'] = ', '.join(list_category)
        # _________________________________________
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones #  добавляем в контекст все доступные часовые пояса
        return context

    #  по пост-запросу будем добавлять в сессию часовой пояс,
    #  который и будет обрабатываться написанным нами ранее middleware
    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/profile')


# Перевод пользователя в авторы
@login_required
def be_author(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
        Author.objects.create(author=user)
    return redirect('/profile')


# Редактирование профиля
class EditProfile(LoginRequiredMixin, UpdateView):
    form_class = EditForm
    template_name = 'accounts/edit_profile.html'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return User.objects.get(pk=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        return context