from django.urls import path
from .views import PostList, PostDetail, PostDelete, PostCreate, PostUpdate, PostSearch, CategoryDetail, post_like, user_response


urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('add/', PostCreate.as_view(), name='add_post'),
    path('update/<int:pk>/', PostUpdate.as_view(), name='update_post'),
    path('search/', PostSearch.as_view(), name='search_post'),
    path('category/<int:pk>/', CategoryDetail.as_view(), name='category'),
    path('post_like/<int:pk>/', post_like, name='post_like'),
    path('response/<int:pk>/', user_response, name='post_response'),
]
