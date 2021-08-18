from django.contrib import admin
from .models import Author,Category, PostCategory, Post
from modeltranslation.admin import TranslationAdmin


class PostsAdmin(admin.ModelAdmin):
    list_display = ('post_author', 'date_create', 'headline', 'post_rating', )
    list_display_links = ('post_author', 'date_create', 'headline', 'post_rating', )
    ordering = ['-date_create']
    list_filter = ('post_author', 'date_create', )
    search_fields = ('headline', 'post_text' )


class PostTranslation(TranslationAdmin):
    model = Post


class CategoryTranslation(TranslationAdmin):
    model = Category


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)

admin.site.register(Author)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Post, PostsAdmin)

admin.site.site_title = 'Новостной портал'
admin.site.site_header = 'Новостной портал'

