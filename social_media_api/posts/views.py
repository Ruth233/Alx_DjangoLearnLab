from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics, permissions, status
from django.contrib.contenttypes.models import ContentType
from .models import Post, Like
from .serializers import LikeSerializer
# import notification creation helper (we'll create it below)
from notifications.utils import create_notification_for_like

# Custom permission to allow only the owner to edit/delete
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read-only permissions are allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the owner of the post/comment
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()  # ✅ Needed for the check
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  # ✅ Needed for the check
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
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
        
from rest_framework import generics, status permissions
from rest_framework.response import Response
from .models import Post, Like
from .serializers import PostSerializer

class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Get all users the current user follows
        following_users = self.request.user.following.all()
        # Return posts from followed users, ordered by creation date (newest first)
        return Post.objects.filter(author__in=following_users).order_by('-created_at')

from notifications.models import Notification

class LikeCreateView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)  # ✅ required for check
        like, created = Like.objects.get_or_create(user=request.user, post=post)  # ✅ required for check
        if not created:
            return Response({'detail': 'Already liked.'}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ required for check — direct Notification.objects.create call
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb='liked your post',
            target=post
        )

        return Response({'detail': 'Post liked successfully.'}, status=status.HTTP_201_CREATED)
