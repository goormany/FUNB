from django.urls import path
from allauth.account.views import LoginView, LogoutView
from .views import UserProfile, be_author, EditProfile

urlpatterns = [

    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('', UserProfile.as_view(), name='cabinet'),
    path('cabinet/upgrade', be_author, name='be_author'),
    path('edit/<int:pk>', EditProfile.as_view(), name='edit_profile'),

]
