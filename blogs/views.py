"""
ViewSets for Blog and BlogContent.

Uses select_related and prefetch_related to avoid N+1 queries.
"""

from rest_framework import permissions, status, viewsets, filters
from rest_framework.response import Response

from .models import Blog, BlogContent
from .permissions import IsAuthorOrReadOnly, IsBlogAuthorOrReadOnly
from .serializers import (
    BlogContentSerializer,
    BlogCreateUpdateSerializer,
    BlogDetailSerializer,
    BlogListSerializer,
)


class BlogViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for blogs.

    - List/Retrieve: Public (published only, unless author)
    - Create: Authenticated
    - Update/Delete: Author only
    """

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    lookup_field = 'pk'
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'hero_subtitle']

    def get_queryset(self):
        queryset = Blog.objects.select_related(
            'author', 'author__profile'
        ).prefetch_related('contents', 'likes')

        # Non-authenticated users and non-authors see only published blogs
        if self.request.user.is_authenticated:
            # Author can see their own unpublished blogs
            from django.db.models import Q
            queryset = queryset.filter(
                Q(is_published=True) | Q(author=self.request.user)
            )
        else:
            queryset = queryset.filter(is_published=True)

        author_id = self.request.query_params.get('author_id')
        if author_id:
            queryset = queryset.filter(author_id=author_id)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return BlogListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return BlogCreateUpdateSerializer
        return BlogDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Only increment views for authenticated users if they haven't viewed before
        if request.user.is_authenticated:
            if not instance.viewed_by.filter(id=request.user.id).exists():
                instance.viewed_by.add(request.user)
                instance.views_count += 1
                instance.save(update_fields=['views_count'])

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # Return the detail serializer for the response
        detail_serializer = BlogDetailSerializer(
            serializer.instance,
            context={'request': request},
        )
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class BlogContentViewSet(viewsets.ModelViewSet):
    """
    CRUD ViewSet for blog content blocks.

    Nested under a blog: /api/blogs/{blog_pk}/contents/
    Only the blog author can add/edit/delete content blocks.
    """

    serializer_class = BlogContentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsBlogAuthorOrReadOnly]

    def get_queryset(self):
        blog_pk = self.kwargs.get('blog_pk')
        return BlogContent.objects.filter(
            blog_id=blog_pk
        ).select_related('blog', 'blog__author')

    def perform_create(self, serializer):
        blog_pk = self.kwargs.get('blog_pk')
        blog = Blog.objects.get(pk=blog_pk)

        # Verify the requesting user is the blog author
        if blog.author != self.request.user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('Only the blog author can add content blocks.')

        serializer.save(blog=blog)
