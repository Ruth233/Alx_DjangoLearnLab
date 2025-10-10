from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions, status
from django.contrib.contenttypes.models import ContentType
from .models import Post, Like
from .serializers import LikeSerializer
# import notification creation helper (we'll create it below)
from notifications.utils import create_notification_for_like

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author').prefetch_related('comments').all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author__username']     # allow filtering by author username
    search_fields = ['title', 'content']       # full-text-like search (icontains)
    ordering_fields = ['created_at', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'], url_path='comments', url_name='comments')
    def list_comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related('author', 'post').all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['post', 'author__username']
    search_fields = ['content']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        # Expect client to pass 'post' ID in payload; set author automatically
        serializer.save(author=self.request.user)


class LikeCreateView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        """
        Like a post (pk: post id). Prevent duplicate likes.
        """
        post = get_object_or_404(Post, pk=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            return Response({'detail': 'Already liked.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create notification for the post author (unless author likes their own post, optional)
        if post.author != request.user:
            create_notification_for_like(actor=request.user, recipient=post.author, target=post)

        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LikeDestroyView(generics.GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        """
        Unlike a post (pk: post id). Returns 204 on success.
        """
        post = get_object_or_404(Post, pk=pk)
        like_qs = Like.objects.filter(post=post, user=request.user)
        if not like_qs.exists():
            return Response({'detail': 'Not liked yet.'}, status=status.HTTP_400_BAD_REQUEST)
        like_qs.delete()
        # Optionally delete related notification(s) if you created one (keep simple: not deleting notifications here)
        return Response(status=status.HTTP_204_NO_CONTENT)
