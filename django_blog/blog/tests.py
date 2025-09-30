from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Comment, Tag

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


class CommentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='alice', password='pass')
        self.other = User.objects.create_user(username='bob', password='pass')
        self.post = Post.objects.create(title='T', content='C', author=self.user)

    def test_create_comment_requires_login(self):
        url = reverse('comment-create', args=[self.post.pk])
        res = self.client.post(url, {'content': 'Nice post!'})
        self.assertNotEqual(res.status_code, 200)  # should redirect to login

    def test_create_comment_authenticated(self):
        self.client.login(username='alice', password='pass')
        url = reverse('comment-create', args=[self.post.pk])
        res = self.client.post(url, {'content': 'Nice post!'}, follow=True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(self.post.comments.filter(content='Nice post!').exists())

    def test_edit_comment_by_author(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='First')
        self.client.login(username='alice', password='pass')
        url = reverse('comment-update', args=[self.post.pk, comment.pk])
        res = self.client.post(url, {'content': 'Edited'}, follow=True)
        self.assertEqual(res.status_code, 200)
        comment.refresh_from_db()
        self.assertEqual(comment.content, 'Edited')

    def test_edit_comment_forbidden_for_non_author(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='First')
        self.client.login(username='bob', password='pass')
        url = reverse('comment-update', args=[self.post.pk, comment.pk])
        res = self.client.get(url)
        self.assertIn(res.status_code, (302, 403))  # redirect to login or 403 due to test_func

    def test_delete_comment_by_author(self):
        comment = Comment.objects.create(post=self.post, author=self.user, content='First')
        self.client.login(username='alice', password='pass')
        url = reverse('comment-delete', args=[self.post.pk, comment.pk])
        res = self.client.post(url, follow=True)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())


from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Post, Tag

class TagSearchTests(TestCase):
    def setUp(self):
        self.u = User.objects.create_user('u', password='p')
        self.post1 = Post.objects.create(title='Django tips', content='Use views', author=self.u)
        self.post2 = Post.objects.create(title='Python tricks', content='Use list comprehensions', author=self.u)
        tag = Tag.objects.create(name='django')
        self.post1.tags.add(tag)

    def test_posts_by_tag(self):
        res = self.client.get(reverse('posts-by-tag', args=[ 'django' ]))  # slug is 'django'
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.post1.title)
        self.assertNotContains(res, self.post2.title)

    def test_search_title_content(self):
        res = self.client.get(reverse('search-results') + '?q=Django')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.post1.title)

    def test_search_by_tag_name(self):
        res = self.client.get(reverse('search-results') + '?q=django')
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.post1.title)

