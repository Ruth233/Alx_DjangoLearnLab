from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

def profile_image_upload_to(instance, filename):
    return f'profile_pics/user_{instance.id}/{filename}'

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=profile_image_upload_to, blank=True, null=True)
    # followers: users who follow this user
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='following',
        symmetrical=False,
        blank=True
    )

    def follower_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()

    def __str__(self):
        return self.username


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to=profile_image_upload_to, blank=True, null=True)

    # Users this user follows (directional)
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    def follower_count(self):
        return self.followers.count()

    def following_count(self):
        return self.following.count()

    def __str__(self):
        return self.username
