"""URL configuration for users app."""

from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:id>/', views.PublicProfileView.as_view(), name='public-profile'),
    path('follow/<int:user_id>/', views.FollowToggleView.as_view(), name='follow-toggle'),
]
