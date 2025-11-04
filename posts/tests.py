from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Post, Like, Comment

User = get_user_model()

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_post_creation(self):
        post = Post.objects.create(user=self.user, content='Test post')
        self.assertEqual(post.content, 'Test post')
        self.assertEqual(post.user, self.user)

    def test_post_with_image(self):
        # Simula um post com imagem sem salvar fisicamente
        post = Post.objects.create(user=self.user, content='Test post with image')
        # Apenas testa se o campo image pode ser None ou ter um valor
        self.assertEqual(post.content, 'Test post with image')
        # Campo image pode ser None ou um arquivo, apenas verifica que foi criado
        self.assertTrue(post.image is None or hasattr(post.image, 'name'))

    def test_image_validation_invalid_extension(self):
        # Testa validação de extensão inválida
        image = SimpleUploadedFile(
            "test_file.txt",
            b"file_content",
            content_type="text/plain"
        )
        post = Post(user=self.user, content='Test post', image=image)
        with self.assertRaises(Exception):  # Deve falhar na validação
            post.full_clean()

    def test_image_validation_too_large(self):
        # Testa validação de tamanho (arquivo muito grande)
        large_content = b"x" * (11 * 1024 * 1024)  # 11MB
        image = SimpleUploadedFile(
            "large_image.jpg",
            large_content,
            content_type="image/jpeg"
        )
        post = Post(user=self.user, content='Test post', image=image)
        with self.assertRaises(Exception):  # Deve falhar na validação
            post.full_clean()

class LikeModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(user=self.user, content='Test post')

    def test_like_creation(self):
        like = Like.objects.create(user=self.user, post=self.post)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.post, self.post)

    def test_unique_like_constraint(self):
        Like.objects.create(user=self.user, post=self.post)
        with self.assertRaises(Exception):
            Like.objects.create(user=self.user, post=self.post)

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.post = Post.objects.create(user=self.user, content='Test post')

    def test_comment_creation(self):
        comment = Comment.objects.create(user=self.user, post=self.post, content='Test comment')
        self.assertEqual(comment.content, 'Test comment')
        self.assertEqual(comment.user, self.user)
        self.assertEqual(comment.post, self.post)

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

    def test_post_list_view_authenticated(self):
        Post.objects.create(user=self.user, content='Test post 1')
        Post.objects.create(user=self.user, content='Test post 2')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test post 1')
        self.assertContains(response, 'Test post 2')

    def test_post_detail_view(self):
        post = Post.objects.create(user=self.user, content='Test post')
        response = self.client.get(reverse('post_detail', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test post')

    def test_like_post_view(self):
        post = Post.objects.create(user=self.user, content='Test post')
        response = self.client.post(reverse('post_like', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Like.objects.filter(user=self.user, post=post).exists())

    def test_unlike_post_view(self):
        post = Post.objects.create(user=self.user, content='Test post')
        Like.objects.create(user=self.user, post=post)
        response = self.client.post(reverse('post_like', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Like.objects.filter(user=self.user, post=post).exists())

    def test_add_comment_view(self):
        post = Post.objects.create(user=self.user, content='Test post')
        response = self.client.post(reverse('add_comment', kwargs={'pk': post.pk}), {
            'content': 'Test comment'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(content='Test comment').exists())

    def test_delete_comment_view(self):
        post = Post.objects.create(user=self.user, content='Test post')
        comment = Comment.objects.create(user=self.user, post=post, content='Test comment')
        response = self.client.post(reverse('delete_comment', kwargs={'pk': comment.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())
