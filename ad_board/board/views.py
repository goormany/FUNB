import logging
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, FormView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Post, Category, Comments
from .forms import PostForm, CategoryForm, CommentForm
from .filters import PostFilter
from users.models import CustomUser


logger = logging.getLogger(__name__)


class PostList(FormView, ListView):
    """Представление списка постов"""
    model = Post  # модель из БД
    template_name = 'board/board.html'  # имя шаблона html
    context_object_name = 'post_list'  # имя списка
    ordering = ['-id']
    paginate_by = 4
    

    form_class = CategoryForm
    success_url = reverse_lazy('posts')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        """кастомная валидация полей формы модели"""
        form.save()  # здесь применяется для FormView
        return super().form_valid(form)


class PostDetail(CreateView, DetailView):
    """Представление выбранного поста"""
    model = Post
    template_name = 'board/post_detail.html'
    context_object_name = 'post_detail'
    form_class = CommentForm


    def get_success_url(self, *args, **kwargs):
        """Redirect to the page listing all of the proxy urls"""
        pk = self.kwargs.get(self.pk_url_kwarg)
        return reverse_lazy('post_detail', kwargs={'pk' : pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = get_object_or_404(Post, id=self.kwargs.get(self.pk_url_kwarg))
        post_id = self.kwargs.get(self.pk_url_kwarg)
        context['all_comments'] = Comments.objects.filter(comment_post=post_id).order_by('-comment_date')
        if self.request.user == post.post_author:
            context['is_author'] = True
        else:
            context['is_not_author'] = True
        logger.info("Your log message is here")
        return context

    def form_valid(self, form):
        """Функция для кастомной валидации полей формы модели"""
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        # Через реквест передаем недостающую форму, которая обязательно
        post_id = self.kwargs.get(self.pk_url_kwarg)
        fields.comment_post = Post.objects.get(pk=post_id)
        fields.comment_author = self.request.user
        # Наконец сохраняем в БД
        fields.save()
        return super().form_valid(form)


class PostDelete(LoginRequiredMixin, DeleteView):
    """Представление удаления выбранного поста"""
    queryset = Post.objects.all()
    success_url = reverse_lazy('posts')
    login_url = reverse_lazy('profile')

    def get(self, *args, **kwargs):
        return self.delete(*args, **kwargs)


class PostCreate(LoginRequiredMixin, CreateView):
    """Представление создания поста"""
    form_class = PostForm
    template_name = 'board/add_post.html'
    login_url = reverse_lazy('profile')

    # Функция для кастомной валидации полей формы модели
    def form_valid(self, form):
        # создаем форму, но не отправляем его в БД, пока просто держим в памяти
        fields = form.save(commit=False)
        # Через реквест передаем недостающую форму, которая обязательно
        fields.post_author = self.request.user
        # Наконец сохраняем в БД
        fields.save()
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
    """Представление создания поста"""
    form_class = PostForm
    template_name = 'board/update_post.html'
    success_url = reverse_lazy('posts')
    login_url = reverse_lazy('profile')


    def get_object(self, **kwargs):
        """метод get_object чтобы получить информацию об
           объекте который мы собираемся редактировать"""
        post_id = self.kwargs.get(self.pk_url_kwarg)
        obj = Post.objects.get(pk=post_id)
        return obj


class PostSearch(ListView):
    """Представление для сортировки и поиска"""
    model = Post
    template_name = 'board/search_post.html'
    context_object_name = 'search_items'
    paginate_by = 1

    def get_queryset(self):  # здесь не применяется просто пример
        """фильтрация без джанго фильтра"""
        if self.request.GET.get('search'):
            return Post.objects.filter(headline__icontains=self.request.GET.get('search'))
        else:
            return Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('search'):
            context['search_list'] = Post.objects.filter(
                headline__icontains=self.request.GET.get('search'))
        context['search_filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class CategoryDetail(DetailView):
    """Представление списка постов в категории"""
    model = Category
    template_name = 'board/category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # найти pk текущей категории
        cat_pk = self.kwargs.get(self.pk_url_kwarg)
        context["posts"] = Post.objects.filter(
            post_category=cat_pk).order_by('-id')  # все посты из этой категории
        return context


@login_required(login_url='/accounts/login/')
def post_like(request, pk):
    """отработка лайков и дизлайков"""
    like = request.POST.get('post_like')
    dislike = request.POST.get('post_dislike')
    if like:
        post = get_object_or_404(Post, id=like)
        post.likes.add(request.user)
    elif dislike:
        post = get_object_or_404(Post, id=dislike)
        post.dislikes.add(request.user)
    # возврат на пред. страницу
    return redirect('post_detail', pk=pk)


@login_required(login_url='/accounts/login/')
def user_response(request, pk):
    """отклик на пост"""
    post = get_object_or_404(Post, id=request.POST.get('post_response'))
    post.responses.add(request.user)
    messages.info(request, 'Отклик успешно отправлен!')
    return redirect('post_detail', pk=pk)