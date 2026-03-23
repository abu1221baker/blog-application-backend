"""Admin configuration for comments app."""

from django.contrib import admin

from .models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'blog', 'body_preview', 'parent', 'created_at']
    list_filter = ['created_at']
    search_fields = ['author__username', 'body']
    raw_id_fields = ['blog', 'author', 'parent']

    def body_preview(self, obj):
        return obj.body[:75] + '...' if len(obj.body) > 75 else obj.body
    body_preview.short_description = 'Body'
