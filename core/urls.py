"""
Root URL Configuration for Blog Application.

Routes all API endpoints, JWT auth, and Swagger documentation.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # JWT Authentication
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # App URLs
    path('api/users/', include('users.urls')),
    path('api/blogs/', include('blogs.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/likes/', include('likes.urls')),
    path('api/notifications/', include('notifications.urls')),


    # API Schema & Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
