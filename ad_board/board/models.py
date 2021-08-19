from django.db import models
from django.conf import settings
from django.urls import reverse
from ckeditor.fields import RichTextField
from users.models import CustomUser


class Category(models.Model):
    """Категории статей"""
    category = models.CharField(
        max_length=255, unique=True, verbose_name='Категория',)

    def __str__(self):
        '''Строковое отображение категории'''
        return f'{self.category}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        """получить ссылку на объект"""
        return reverse('category', kwargs={'pk': self.pk})


class Post(models.Model):
    """Статьи пользователей"""
    post_author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Автор',)
    date_create = models.DateField(
        auto_now_add=True, verbose_name='Дата публикации',)
    headline = models.CharField(
        max_length=255, null=False, verbose_name='Заголовок',)
    content = RichTextField(blank=True, null=True,)
    likes = models.ManyToManyField(CustomUser, related_name='post_likes',)
    dislikes = models.ManyToManyField(CustomUser, related_name='post_dislikes',)
    responses = models.ManyToManyField(CustomUser, related_name='post_responses',)
    accepted_responses = models.ManyToManyField(CustomUser, related_name='post_accepted_responses',)
    post_picture = models.ImageField(upload_to='board/image/%Y/%m', blank=True)
    post_category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='Категория',)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        '''Строковое отображение поста'''
        return f'{self.headline}'

    def get_absolute_url(self):
        """получить ссылку на объект"""
        return reverse('post_detail', kwargs={'pk': self.pk})

    def count_like(self):
        """сколько лайков у поста"""
        return self.likes.count()

    def count_dislike(self):
        """сколько дизлайков у поста"""
        return self.dislikes.count()

class PostLikes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, )


class Comments(models.Model):
    """Модуль хранения комментариев под постами"""
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment_text = models.TextField(null=False, verbose_name='напишите комментарии')
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def __str__(self):
        """Строковое отображение комментария"""
        return f'{self.comment_text}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    # def get_absolute_url(self):
    #     """получить ссылку на объект"""
    #     return reverse('category', kwargs={'pk': self.pk})
