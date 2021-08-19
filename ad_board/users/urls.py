from django.urls import path
from .views import UserProfile, UserProfileEdit



urlpatterns = [
    path('', UserProfile.as_view(), name='profile'),
    path('edit/', UserProfileEdit.as_view(), name='edit_profile'),
    ]