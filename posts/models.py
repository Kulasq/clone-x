import os
from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=280, verbose_name='Conteúdo')
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name='Imagem')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.image:
            self.optimize_post_image()
    
    def optimize_post_image(self):
        """Otimiza e redimensiona a imagem do post"""
        img_path = self.image.path
        img = Image.open(img_path)
        
        # Redimensiona para tamanho máximo (800px de largura)
        if img.width > 800:
            ratio = 800 / img.width
            new_height = int(img.height * ratio)
            output_size = (800, new_height)
            img = img.resize(output_size, Image.Resampling.LANCZOS)
            img.save(img_path, optimize=True, quality=85)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def user_has_liked(self, user):
        """Verifica se um usuário curtiu este post"""
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:50]}"
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
    
    @property
    def likes_count(self):
        return self.likes.count()
    
    @property
    def comments_count(self):
        return 0
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']
    
    def __str__(self):
        return f"{self.user.username} curtiu {self.post.id}"