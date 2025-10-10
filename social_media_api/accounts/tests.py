from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

# Create your tests here.

User = get_user_model()

class FollowTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username='u1', password='pass')
        self.u2 = User.objects.create_user(username='u2', password='pass')

    def test_follow_unfollow(self):
        self.client.login(username='u1', password='pass')
        url = reverse('follow-user', args=[self.u2.id])
        res = self.client.post(url)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.u2 in self.u1.following.all())
        # unfollow
        url2 = reverse('unfollow-user', args=[self.u2.id])
        res2 = self.client.post(url2)
        self.assertEqual(res2.status_code, 200)
        self.assertFalse(self.u2 in self.u1.following.all())
