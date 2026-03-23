"""Admin configuration for likes app."""

from django.contrib import admin

from .models import Like


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'blog', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'blog__title']
    raw_id_fields = ['user', 'blog']
