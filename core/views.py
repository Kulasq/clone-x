from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from posts.models import Post

@login_required
def home_view(request):
    posts = Post.objects.all().select_related('user')
    return render(request, 'posts/feed.html', {'posts': posts})
