from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet
from django.urls import path, include
from .views import LikeCreateView, LikeDestroyView
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>/like/', LikeCreateView.as_view(), name='post-like'),
    path('<int:pk>/unlike/', LikeDestroyView.as_view(), name='post-unlike'),
]