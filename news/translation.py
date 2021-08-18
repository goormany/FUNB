from .models import Category, Post
# импортируем декоратор для перевода и класс настроек, от которого будем наследоваться
from modeltranslation.translator import register, TranslationOptions

# регистрируем наши модели для перевода


@register(Post)
class PostTranslationOptions(TranslationOptions ):
    fields = ('headline', 'post_text', 'date_create')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('category', ) # указываем, какие именно поля надо переводить в виде кортежа