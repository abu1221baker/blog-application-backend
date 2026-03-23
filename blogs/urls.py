"""URL configuration for blogs app using DRF routers."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'blogs'

router = DefaultRouter()
router.register(r'', views.BlogViewSet, basename='blog')

# Nested router for blog content blocks
content_list = views.BlogContentViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
content_detail = views.BlogContentViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    # Blog content nested endpoints — must be before router includes
    path('<int:blog_pk>/contents/', content_list, name='blog-content-list'),
    path('<int:blog_pk>/contents/<int:pk>/', content_detail, name='blog-content-detail'),

    # Blog endpoints
    path('', include(router.urls)),
]
