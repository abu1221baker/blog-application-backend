"""
ViewSet for comments with CRUD and ownership permissions.
"""

from rest_framework import permissions, viewsets

from .models import Comment
from .serializers import CommentSerializer


class IsCommentOwnerOrReadOnly(permissions.BasePermission):
    """Only the comment author can edit or delete."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for comments.

    - List: filter by blog_id query param, returns only top-level comments
    - Create: Authenticated users
    - Update/Delete: Comment owner only
    """

    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCommentOwnerOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.select_related(
            'author', 'blog'
        ).prefetch_related('children')

        # Filter by blog if specified
        blog_id = self.request.query_params.get('blog_id')
        if blog_id:
            queryset = queryset.filter(blog_id=blog_id)

        # For list action, show only top-level comments (children are nested)
        if self.action == 'list':
            queryset = queryset.filter(parent__isnull=True)

        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
