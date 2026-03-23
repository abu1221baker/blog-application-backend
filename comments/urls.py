"""URL configuration for comments app."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'comments'

router = DefaultRouter()
router.register(r'', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
