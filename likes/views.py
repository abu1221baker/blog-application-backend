"""
ViewSet for liking and unliking blogs.
"""

from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from blogs.models import Blog

from .models import Like
from .serializers import LikeSerializer


class LikeViewSet(viewsets.GenericViewSet):
    """
    ViewSet for handling Likes.

    Only authenticated users can like/unlike.
    Using a custom 'toggle' action instead of generic CRUD.
    """

    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'], url_path='toggle/(?P<blog_id>[^/.]+)')
    def toggle_like(self, request, blog_id=None):
        """
        Toggle a like on a blog post.

        POST /api/likes/toggle/{blog_id}/
        """
        blog = get_object_or_404(Blog, pk=blog_id)
        user = request.user

        like, created = Like.objects.get_or_create(blog=blog, user=user)

        if not created:
            # User already liked it, so unlike it
            like.delete()
            return Response(
                {'message': 'Unliked', 'is_liked': False, 'like_count': blog.likes.count()},
                status=status.HTTP_200_OK,
            )

        # Successfully liked
        return Response(
            {'message': 'Liked', 'is_liked': True, 'like_count': blog.likes.count()},
            status=status.HTTP_201_CREATED,
        )
