from django_filters import FilterSet
from .models import Post

from django.forms import Select



class NewsFilter(FilterSet):
    class Meta:
        model = Post
        # fields = ('post_author')
        fields = {
                  'post_author':['exact'],
                  'date_create':['range']
                  }

