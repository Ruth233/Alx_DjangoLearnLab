from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView
)

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/templates/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/templates/logout.html'), name='logout'),
    path('profile/', views.profile, name='profile'),
    
    path('posts/', PostListView.as_view(), name='post-list'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-update'),
<<<<<<< HEAD
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    
    # Comments (nested)
    path('post/<int:post_pk>/comments/new/', CommentCreateView.as_view(), name='comment-create'),
    path('post/<int:post_pk>/comments/<int:comment_pk>/edit/', CommentUpdateView.as_view(), name='comment-update'),
    path('post/<int:post_pk>/comments/<int:comment_pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]
=======
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
]
>>>>>>> a1ac96cf898bce52711c57fdd71b06283b099fd3
