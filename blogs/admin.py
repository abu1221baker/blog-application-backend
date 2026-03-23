"""Admin configuration for blogs app."""

from django.contrib import admin

from .models import Blog, BlogContent


class BlogContentInline(admin.TabularInline):
    model = BlogContent
    extra = 1
    ordering = ['order']


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [BlogContentInline]
    date_hierarchy = 'created_at'


@admin.register(BlogContent)
class BlogContentAdmin(admin.ModelAdmin):
    list_display = ['blog', 'content_type', 'order']
    list_filter = ['content_type']
    ordering = ['blog', 'order']
