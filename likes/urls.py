"""URL configuration for likes app."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'likes'

router = DefaultRouter()
router.register(r'', views.LikeViewSet, basename='like')

urlpatterns = [
    path('', include(router.urls)),
]
