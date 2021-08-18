import logging
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from django.utils.translation import gettext as _  # импортируем функцию для перевода
from django.utils import timezone
from django.core.cache import cache # импортируем наш кэш
from .filters import NewsFilter
from .forms import PostForm
from .models import Post, Author, Category, CategorySubscribers
# Импортируем задачу для асинхронной задачи
from .tasks import send_mail_subscribe, send_mail_unsubscribe  




logger = logging.getLogger(__name__)


# Представление списка новостей
class NewsList(ListView):
    model = Post  # модель из БД
    template_name = 'news/news.html'  # имя шаблона html
    context_object_name = 'news_list'  # имя списка
    paginate_by = 4  # поставим постраничный вывод в один элемент
    ordering = ['date_create']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_politic'] = Category.objects.get(category=_('Политика')).id
        context['category_sport'] = Category.objects.get(category=_('Спорт')).id
        context['category_society'] = Category.objects.get(category=_('Общество')).id
        context['category_science'] = Category.objects.get(category=_('Наука')).id
        context['current_time'] = timezone.localtime(timezone.now())
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/profile')



class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'detail_news'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
        obj = cache.get(f'product-{self.kwargs["pk"]}',
                        None)  # кэш очень похож на словарь, и метод get действует также. Он забирает значение
                               # по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object()
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        return context


# Страница для сортировки и поиска
class NewsSearch(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'search_list'  # имя списка

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        context['current_time'] = timezone.localtime(timezone.now())
        return context


# Наследуем переопределяем функции в классе PermissionRequiredMixin, далее наследуемся от этого класса
class RedirectPermissionRequiredMixin(PermissionRequiredMixin):
    login_url = reverse_lazy('login')

    # Обработчик уведомлении
    def handle_no_permission(self):
        # Пишем сообщение при отказе из-за недостатка прав
        messages.error(self.request, 'У вас недостаточно прав!')
        return redirect(reverse_lazy('news'))


# Джененрик для создания поста
class PostCreateView(RedirectPermissionRequiredMixin, CreateView):
    template_name = 'news/create_post.html'
    form_class = PostForm
    permission_required = ('news.add_post')
    success_url = reverse_lazy('news')

    # Функция для кастомной валидации полей формы модели
    def form_valid(self, form):
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        # Через реквест передаем недостающую форму, которая обязательно
        fields.post_author = Author.objects.get(author=self.request.user)
        # Наконец сохраняем в БД
        fields.save()
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        return context


# дженерик для редактирования объекта
class PostUpdateView(RedirectPermissionRequiredMixin, UpdateView):
    template_name = 'news/update_post.html'
    form_class = PostForm
    permission_required = ('news.change_post')
    success_url = reverse_lazy('news')

    # метод get_object чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        return context


# дженерик для удаления поста
class PostDeleteView(RedirectPermissionRequiredMixin, DeleteView):
    template_name = 'news/delete_post.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('news')
    permission_required = ('news.delete_post')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        return context

# Представление категории
class CategoryPost(DetailView):
    model = Category
    template_name = 'news/category.html'
    context_object_name = 'PostCategory'

    def get_context_data(self, **kwargs):
        id = self.kwargs.get('pk')
        context = super().get_context_data(**kwargs)
        # Контекст для списка новостей в текущей категории
        context['category_news'] = (Post.objects.filter(post_category=id))
        # Контекст авторизован ли пользователь
        context['user_is_anonymous'] = self.request.user.is_anonymous
        # Контекст подписан ли пользователь на текущую категорию. .exists() возвращает булево значение
        context['current_time'] = timezone.localtime(timezone.now())
        if not self.request.user.is_anonymous:
            context['is_subscribe'] = CategorySubscribers.objects.filter(category=id, user=self.request.user).exists()
        return context


# Подписка пользователя в категорию новостей
@login_required
def subscribe_category(request):
    # Достаем текущего пользователя
    user = request.user
    # Получаем ссылку из адресной строки и берем pk как id категории
    id = request.META.get('HTTP_REFERER')[-2]
    # Получаем текущую категорию
    category = Category.objects.get(id=id)
    # Создаем связь между пользователем и категорией
    category.subscribers.add(user)
    # Сериалезируем переменные для передачи в селери
    category = f'{category}'
    email = f'{user.email}'
    # вызываем таск для асинхронной отправки письмо
    send_mail_subscribe.delay(category, email)
    return redirect('cabinet')


# Отписка пользователя из категории новостей
@login_required
def unsubscribe_category(request):
    # Достаем текущего пользователя
    user = request.user
    # Получаем ссылку из адресной строки и берем pk как id категории
    id = request.META.get('HTTP_REFERER')[-2]
    # Получаем текущую категорию
    category = Category.objects.get(id=id)
    # Разрываем связь между пользователем и категорией
    category.subscribers.remove(user)
    # Сериалезируем переменные для передачи в селери
    category = f'{category}'
    email = f'{user.email}'
    # вызываем таск для асинхронной отправки письмо
    send_mail_unsubscribe.delay(category, email)
    return redirect('cabinet')
