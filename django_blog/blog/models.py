from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = TaggableManager()   #tagging support

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # convenient for CreateView/UpdateView to redirect to detail
        return reverse('post-detail', args=[str(self.pk)])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # update timestamp on save

    class Meta:
        ordering = ['created_at']  # oldest first

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

    def get_edit_url(self):
        return reverse('comment-update', args=[self.post.pk, self.pk])

    def get_delete_url(self):
        return reverse('comment-delete', args=[self.post.pk, self.pk])


    def __str__(self):
        return self.title
