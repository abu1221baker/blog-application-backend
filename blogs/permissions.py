"""
Custom permissions for blogs app.
"""

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object-level permission.

    Only the blog author can edit or delete; everyone else is read-only.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsBlogAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission for BlogContent.

    Only the parent blog's author can modify content blocks.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.blog.author == request.user
