from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateFilter, DateRangeFilter
from django.forms import TextInput, Select, DateInput
from users.models import CustomUser
from .models import Post, Category


class PostFilter(FilterSet):
    """фильтр поиска"""
    headline = CharFilter(field_name='headline', lookup_expr='icontains', label=u'Поиск по заголовкам',
                          widget=TextInput(attrs={'placeholder': 'название статьи', 'class': 'form-control'}))

    post_author = ModelChoiceFilter(field_name='post_author', queryset=CustomUser.objects.all(), label=u'Поиск поста по автору',
                                    widget=Select(attrs={'placeholder': 'название статьи', 'class': 'form-control'}))

    start_date = DateFilter(field_name='date_create', lookup_expr='gt', label=u'Начальная дата',
                            widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    end_date = DateFilter(field_name='date_create', lookup_expr='lt', label=u'Конечная дата',
                          widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    date_range = DateRangeFilter(field_name='date_create', label=u'Выбрать период',
                                 widget=Select(attrs={'placeholder': 'Выбрать период', 'class': 'form-control'}))
                                 
    post_category = ModelChoiceFilter(field_name='post_category', queryset=Category.objects.all(), label=u'Поиск категории',
                                      widget=Select(attrs={'placeholder': 'Поиск категории', 'class': 'form-control'}))

    class Meta:
        model = Post
        fields = ['headline', 'post_author',
                  'start_date', 'end_date', 'date_range', 'post_category', ]
