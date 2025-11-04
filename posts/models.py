import os
from PIL import Image
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError

User = get_user_model()

def validate_image_file(value):
    """Valida se o arquivo é uma imagem válida e segura."""
    if not value:
        return

    # Verifica extensão
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(f'Formato de imagem não suportado. Use: {", ".join(valid_extensions)}')

    # Verifica tipo MIME
    valid_mime_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if hasattr(value.file, 'content_type'):
        if value.file.content_type not in valid_mime_types:
            raise ValidationError('Tipo de arquivo não permitido.')

    # Verifica tamanho (máximo 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    if value.size > max_size:
        raise ValidationError('Imagem muito grande. Máximo 10MB.')

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(max_length=280, verbose_name='Conteúdo')
    image = models.ImageField(upload_to='post_images/', blank=True, null=True, verbose_name='Imagem', validators=[validate_image_file])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em', db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    def delete(self, *args, **kwargs):
        """Deleta a imagem do filesystem quando o post é excluído"""
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        """Deleta a imagem antiga quando uma nova é uploadada"""
        # Verifica se é uma atualização e se tem uma imagem antiga
        if self.pk:
            try:
                old_post = Post.objects.get(pk=self.pk)
                if old_post.image and old_post.image != self.image:
                    if os.path.isfile(old_post.image.path):
                        os.remove(old_post.image.path)
            except Post.DoesNotExist:
                pass
        
        super().save(*args, **kwargs)
        
        if self.image:
            self.optimize_post_image()
    
    def optimize_post_image(self):
        """Otimiza e redimensiona a imagem do post com limites de tamanho"""
        img_path = self.image.path
        img = Image.open(img_path)

        # Define os limites máximos
        max_width = 1200
        max_height = 800

        # Verifica se precisa redimensionar
        needs_resize = img.width > max_width or img.height > max_height

        if needs_resize:
            # Calcula as novas dimensões mantendo o aspect ratio
            if img.width / max_width > img.height / max_height:
                # Limita pela largura
                ratio = max_width / img.width
                new_width = max_width
                new_height = int(img.height * ratio)
            else:
                # Limita pela altura
                ratio = max_height / img.height
                new_height = max_height
                new_width = int(img.width * ratio)

            # Aplica o redimensionamento
            output_size = (new_width, new_height)
            img = img.resize(output_size, Image.Resampling.LANCZOS)
            img.save(img_path, optimize=True, quality=85)

        elif img.format in ['JPEG', 'JPG']:
            img.save(img_path, optimize=True, quality=85)

        # Converte para RGB se necessário (para compatibilidade)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
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
        return self.comments.count()
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']
    
    def __str__(self):
        return f"{self.user.username} curtiu {self.post.id}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(max_length=280, verbose_name='Comentário')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        ordering = ['created_at']  
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
    
    def __str__(self):
        return f"{self.user.username}: {self.content[:30]}"
    
    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.post.pk})