from django.test import TestCase
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post

# Create your tests here.
class PostViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='u', password='p')
        self.other = User.objects.create_user(username='o', password='p')
        self.post = Post.objects.create(title='T', content='C', author=self.user)

    def test_create_requires_login(self):
        response = self.client.get(reverse('post-create'))
        self.assertRedirects(response, '/login/?next=' + reverse('post-create'))

    def test_author_can_edit(self):
        self.client.login(username='u', password='p')
        response = self.client.get(reverse('post-update', args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)

    def test_non_author_cannot_edit(self):
        self.client.login(username='o', password='p')
        response = self.client.get(reverse('post-update', args=[self.post.pk]))
        self.assertEqual(response.status_code, 403)  # UserPassesTestMixin returns 403
