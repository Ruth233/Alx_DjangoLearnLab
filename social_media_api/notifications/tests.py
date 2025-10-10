from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from notifications.models import Notification

# Create your tests here.

User = get_user_model()

class NotificationsViewTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('u1', password='p')
        self.u2 = User.objects.create_user('u2', password='p')
        Notification.objects.create(recipient=self.u1, actor=self.u2, verb='started following you')

    def test_list_notifications(self):
        self.client.login(username='u1', password='p')
        res = self.client.get(reverse('notifications-list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(res.data), 1)

    def test_mark_all_read(self):
        self.client.login(username='u1', password='p')
        res = self.client.post(reverse('notifications-mark-all-read'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertFalse(Notification.objects.filter(recipient=self.u1, unread=True).exists())
