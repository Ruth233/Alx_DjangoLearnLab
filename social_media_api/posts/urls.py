from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
<<<<<<< HEAD
from django.urls import path, include
from .views import LikeCreateView, LikeDestroyView
=======
from .views import FeedView

>>>>>>> cc156e84e17e1710c7779886ecd2fa4df2584a6a
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
<<<<<<< HEAD
    path('<int:pk>/like/', LikeCreateView.as_view(), name='post-like'),
    path('<int:pk>/unlike/', LikeDestroyView.as_view(), name='post-unlike'),
]
=======
     path('feed/', FeedView.as_view(), name='user-feed'),
    path('feed/', FeedView.as_view(), name='feed'),
]
>>>>>>> cc156e84e17e1710c7779886ecd2fa4df2584a6a
