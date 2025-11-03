from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post, Like, Comment

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_post_creation(self):
        post = Post.objects.create(user=self.user, content='Test post')
        self.assertEqual(post.content, 'Test post')
        self.assertEqual(post.user, self.user)

class PostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_post_create_view(self):
        response = self.client.post(reverse('post_create'), {
            'content': 'New test post'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(content='New test post').exists())

    def test_like_post_view(self):
        post = Post.objects.create(user=self.user, content='Test post')
        response = self.client.post(reverse('post_like', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Like.objects.filter(user=self.user, post=post).exists())
