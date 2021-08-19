from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .models import CustomUser
from .forms import UserForm
from board.models import Post


class UserProfile(LoginRequiredMixin, ListView):
    """кабинет пользователя"""
    model = CustomUser
    template_name = 'users/profile.html'
    context_object_name = 'profile'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = CustomUser.objects.get(username=self.request.user)
        context['your_posts'] = Post.objects.filter(post_author=self.request.user)
        # print(self.request.user.email)
        # print(CustomUser.objects.filter(email=self.request.user.email).exclude(username=self.request.user.username))
        return context

    def post(self, request, *args, **kwargs):
        """работа формы"""
        # Принять отклик
        if request.POST.get('accept_response'):
            accept_data = request.POST.get('accept_response').split(' ')
            post = Post.objects.get(id=accept_data[-1])
            user = CustomUser.objects.get(username=accept_data[0])
            post.responses.remove(user)
            post.accepted_responses.add(user)
            messages.info(request, 'Вы приняли отклик!')
        # Отклонить отклик
        elif request.POST.get('deny_response'):
            deny_data = request.POST.get('deny_response').split(' ')
            post = Post.objects.get(id=deny_data[-1])
            user = CustomUser.objects.get(username=deny_data[0])
            post.responses.remove(user)
            messages.info(request, 'Вы отклонили отклик!')
        return redirect('profile')




class UserProfileEdit(LoginRequiredMixin, UpdateView):
    """кабинет пользователя"""
    form_class = UserForm
    template_name = 'users/edit_profile.html'
    success_url = reverse_lazy('profile')
    login_url = '/accounts/login/'

    def get_object(self, **kwargs):
        """метод get_object чтобы получить информацию об
           объекте который мы собираемся редактировать"""
        obj = CustomUser.objects.get(username=self.request.user)
        return obj
        