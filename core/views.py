from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from posts.models import Post
from django.db import models

def home_view(request):
    """Homepage que mostra feed se logado, ou landing page se não logado"""
    if request.user.is_authenticated:
        # Feed personalizado: posts do usuário + posts de quem ele segue
        following_users = request.user.following.all()
        posts = Post.objects.filter(
            models.Q(user=request.user) | models.Q(user__in=following_users)
        ).select_related('user').order_by('-created_at')
        
        return render(request, 'posts/feed.html', {
            'posts': posts,
            'is_personalized_feed': True
        })
    else:
        # Usuário não logado: mostra landing page
        return render(request, 'core/landing.html')