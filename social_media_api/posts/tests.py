from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Post, Comment
from posts.models import Post, Like
from notifications.models import Notification


# Create your tests here.

User = get_user_model()

class PostCommentAPITests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='pass')
        self.u2 = User.objects.create_user(username='u2', password='pass')
        self.post1 = Post.objects.create(author=self.u1, title='First', content='Hello')
        self.post2 = Post.objects.create(author=self.u2, title='Second', content='World')

    def test_list_posts(self):
        url = reverse('post-list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data['results']) >= 2)  # paginated response

    def test_create_post_requires_auth(self):
        url = reverse('post-list')
        res = self.client.post(url, {'title': 'New', 'content': 'X'})
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.login(username='u1', password='pass')
        res = self.client.post(url, {'title': 'New', 'content': 'X'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_only_author_can_update_post(self):
        url = reverse('post-detail', args=[self.post1.pk])
        self.client.login(username='u2', password='pass')
        res = self.client.patch(url, {'title': 'Hacked'})
        self.assertIn(res.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_405_METHOD_NOT_ALLOWED))
        self.client.login(username='u1', password='pass')
        res = self.client.patch(url, {'title': 'Updated'})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.title, 'Updated')

    def test_create_comment(self):
        url = reverse('comment-list')
        self.client.login(username='u2', password='pass')
        res = self.client.post(url, {'post': self.post1.pk, 'content': 'Nice'})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Comment.objects.filter(post=self.post1, author=self.u2).exists())

<<<<<<< HEAD
class LikeNotificationTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('u1', password='p')
        self.u2 = User.objects.create_user('u2', password='p')
        self.post = Post.objects.create(author=self.u2, title='T', content='C')

    def test_like_creates_notification(self):
        url = reverse('post-like', args=[self.post.pk])  # uses path '<int:pk>/like/'
        self.client.login(username='u1', password='p')
        res = self.client.post(url)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        # Notification created for u2
        self.assertTrue(Notification.objects.filter(recipient=self.u2, actor=self.u1, verb__icontains='liked').exists())

    def test_unlike_removes_like(self):
        # first like
        self.client.login(username='u1', password='p')
        self.client.post(reverse('post-like', args=[self.post.pk]))
        self.assertTrue(Like.objects.filter(post=self.post, user=self.u1).exists())
        # unlike
        res = self.client.delete(reverse('post-unlike', args=[self.post.pk]))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Like.objects.filter(post=self.post, user=self.u1).exists())
=======

from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

class FeedTests(APITestCase):
    def setUp(self):
        self.a = User.objects.create_user(username='a', password='pass')
        self.b = User.objects.create_user(username='b', password='pass')
        self.post_b1 = Post.objects.create(author=self.b, title='B1', content='x')
        self.client.login(username='a', password='pass')

    def test_feed_shows_followed_users_posts(self):
        # a follows b
        self.a.following.add(self.b)
        url = reverse('user-feed')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        # response paginated: results list contains post_b1
        data = res.json()
        found_titles = [p['title'] for p in data.get('results', [])]
        self.assertIn('B1', found_titles)
>>>>>>> cc156e84e17e1710c7779886ecd2fa4df2584a6a
