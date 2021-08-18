# Библиотека питона
from datetime import datetime

from django.conf import settings
from django.db import models
from django.core.cache import cache

from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy


# Модель, содержащая объекты всех авторов
class Author(models.Model):
    author = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  verbose_name=pgettext_lazy('Автор', 'Автор'))
    author_rating = models.IntegerField(default=0, verbose_name=pgettext_lazy('Рейтинг автора', 'Рейтинг автора'))

    # Обновляет рейтинг пользователя
    def update_rating(self):
        sum_post = 0
        post = Post.objects.filter(post_author=self).values('post_rating')
        for i in post:
            sum_post = sum_post + i.get('post_rating') * 3

        sum_comment = 0
        comment = Comment.objects.filter(user=self.author).values('comment_rating')
        for i in comment:
            sum_comment = sum_comment + i.get('comment_rating')

        sum_post_comment = 0
        post_comment = Comment.objects.filter(post__post_author=self).values('comment_rating')
        for i in post_comment:
            sum_post_comment = sum_post_comment + i.get('comment_rating')

        self.author_rating = sum_post + sum_comment + sum_post_comment
        self.save()


    # Возвращает автора с наивысшим рейтингом
    @staticmethod
    def best_author():
        return Author.objects.all().order_by('-author_rating')[0]

    # Строковое отабражение автора
    def __str__(self):
        return f'{self.author}'

    class Meta:
        verbose_name = pgettext_lazy('Автор', 'Автор')
        verbose_name_plural = pgettext_lazy('Авторы', 'Авторы')


# Категории новостей/статей
class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, through='CategorySubscribers')

    # Строковое отабражение категории
    def __str__(self):
        return f'{self.category}'

    class Meta:
        verbose_name = pgettext_lazy('Категория', 'Категория')
        verbose_name_plural = pgettext_lazy('Категории', 'Категории')


class CategorySubscribers(models.Model):
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.category}'

# Эта модель должна содержать в себе статьи и новости, которые создают пользователи
class Post(models.Model):
    article = 'artl'
    news = 'news'
    PAPER = [(article, 'статья'), (news, 'новость')]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name=pgettext_lazy('Автор', 'Автор'),)
    post_type = models.CharField(max_length=4, choices=PAPER, default=news)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name=pgettext_lazy('Дата публикации', 'Дата публикации'))
    post_category = models.ManyToManyField(Category, through='PostCategory', help_text=_('соеденить категорию'))
    headline = models.CharField(max_length=255, null=False,
                                verbose_name=pgettext_lazy('Заголовок', 'Заголовок'))
    post_text = models.TextField(null=False, verbose_name=pgettext_lazy('Текст', 'Текст'))
    post_rating = models.IntegerField(default=0, verbose_name=pgettext_lazy('Рейтинг', 'Рейтинг'))
    post_picture = models.ImageField(upload_to='news/image/%Y/%m/%d', blank=True)

    # Возвращает название категории с которой связан текущий пост
    def post_categories(self):
        data = Category.objects.filter(post__post_category__post=self)
        # Множество удобна тем, что одинаковые значения не дублируются
        category = set()
        for i in data:
            category.add(i.category)
        return ' '.join(list(category))


    # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с постом
    def get_absolute_url(self):
        return f':8000/news/{self.id}'

    # Увеличивает рейтинг поста на единицу
    def like(self):
        self.post_rating += 1
        self.save()

    # Уменьшает рейтинг поста на единицу
    def dislike(self):
        self.post_rating -= 1
        self.save()

    # Превью поста
    def preview(self):
        return self.post_text[0:124] + '...'

    # Находит пост с наивысшим реитингом
    @staticmethod
    def find_best_post():
        return Post.objects.all().order_by('-post_rating')[0]

    # Возвращает пост с наивысшим реитингом
    @staticmethod
    def best_post():
        return Post.find_best_post()

    # Строковое отображение поста
    def __str__(self):
        return f'{self.post_author}, {self.headline}, {datetime.ctime(self.date_create)}, {self.post_categories()},'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) # сначала вызываем метод родителя, чтобы объект сохранился
        print('Выполнен save')
        print(cache.get(f'post-{self.pk}')) # проверка, есть ли кеш по этому ключу
        cache.delete(f'post-{self.pk}') # затем удаляем его из кэша, чтобы сбросить его

    class Meta:
        verbose_name = pgettext_lazy('Новость', 'Новость')
        verbose_name_plural = pgettext_lazy('Новости', 'Новости')


# Промежуточная модель для связи «многие ко многим»
class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name=pgettext_lazy('Новость', 'Новость'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=pgettext_lazy('Категория', 'Категория'))

    def __str__(self):
        return f'{self.category} - {self.post}'

    class Meta:
        verbose_name = pgettext_lazy('Связь категории', 'Связь категории')
        verbose_name_plural = pgettext_lazy('Связь категории', 'Связь категории')


# Модуль хранения комментариев под постами
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_text = models.TextField(null=False)
    date_comment = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    # Увеличивает рейтинг комментария на единицу
    def like(self):
        self.comment_rating += 1
        self.save()

    # Уменьшает рейтинг комментария на единицу
    def dislike(self):
        self.comment_rating -= 1
        self.save()

    # Выводит все комментарии из поста с наивысшим рейтингом
    @staticmethod
    def all_comments_for_best_post():
        best_post = Comment.objects.filter(post=Post.find_best_post())
        for i in best_post:
            print(i)

    # Строковое отабражение комментария
    def __str__(self):
        return f' Пользователь:{self.user}, Дата:{datetime.ctime(self.date_comment)}, Рейтинг:{self.comment_rating}, ' \
               f'Текст:{self.comment_text}'

    class Meta:
        verbose_name = pgettext_lazy('Комментарий', 'Комментарий')
        verbose_name_plural = pgettext_lazy('Комментарии', 'Комментарии')