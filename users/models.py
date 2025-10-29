import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from PIL import Image

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True, 
        null=True,
        verbose_name='Foto de Perfil'
    )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)

    # Sistema de seguir
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True
    )
    
    # Métodos para o sistema de seguir
    def follow(self, user):
        """Segue um usuário"""
        if user != self and not self.is_following(user):
            self.following.add(user)
    
    def unfollow(self, user):
        """Deixa de seguir um usuário"""
        if user != self and self.is_following(user):
            self.following.remove(user)
    
    def is_following(self, user):
        """Verifica se está seguindo um usuário"""
        return self.following.filter(id=user.id).exists()
    
    def is_followed_by(self, user):
        """Verifica se é seguido por um usuário"""
        return self.followers.filter(id=user.id).exists()
    
    @property
    def followers_count(self):
        """Retorna o número de seguidores"""
        return self.followers.count()
    
    @property
    def following_count(self):
        """Retorna o número de usuários que segue"""
        return self.following.count()

    def save(self, *args, **kwargs):
        """Sobrescreve save para otimizar imagens"""
        super().save(*args, **kwargs)
        
        if self.profile_picture:
            self.optimize_profile_picture()
    
    def optimize_profile_picture(self):
        """Otimiza e redimensiona a imagem de perfil"""
        img_path = self.profile_picture.path
        img = Image.open(img_path)
        
        # Redimensiona para tamanho máximo
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size, Image.Resampling.LANCZOS)
            img.save(img_path, optimize=True, quality=85)
    
    def delete_profile_picture(self):
        """Remove a foto de perfil"""
        if self.profile_picture:
            # Deleta o arquivo físico
            if os.path.isfile(self.profile_picture.path):
                os.remove(self.profile_picture.path)
            # Limpa o campo
            self.profile_picture.delete(save=False)
            self.save()
    
    def __str__(self):
        return self.username