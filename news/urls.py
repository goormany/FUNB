from django.urls import path
# импортируем представления
from .views import NewsList, NewsDetail, PostCreateView, PostDeleteView, PostUpdateView, NewsSearch, CategoryPost
from .views import subscribe_category, unsubscribe_category



urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для э
    path('', NewsList.as_view(), name='news'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('search/', NewsSearch.as_view(), name='post_search'),
    path('category/<int:pk>/', CategoryPost.as_view(), name='category'),
    path('category/subscribe/', subscribe_category, name='subscribe'),
    path('category/unsubscribe/', unsubscribe_category, name='unsubscribe'),

]
