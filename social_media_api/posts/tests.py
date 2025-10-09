from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Post, Comment

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
