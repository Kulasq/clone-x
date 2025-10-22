from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from posts.models import Post

def home_view(request):
    """Homepage que mostra feed se logado, ou landing page se não logado"""
    if request.user.is_authenticated:
        # Usuário logado: mostra feed
        posts = Post.objects.all().select_related('user')
        return render(request, 'posts/feed.html', {'posts': posts})
    else:
        # Usuário não logado: mostra landing page
        return render(request, 'core/landing.html')