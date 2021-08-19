from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget 
from .models import Post, Category, Comments



class PostAdminForm(forms.ModelForm):
    content = forms.CharField(label='Содержание', widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'

class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm


admin.site.register(Post, PostAdmin)
admin.site.register(Category, )
admin.site.register(Comments, )


admin.site.site_title = 'Доска объявлении'
admin.site.site_header = 'Доска объявлении'
