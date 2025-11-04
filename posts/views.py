from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Like, Comment
from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()

@login_required
def post_create_view(request):
    """Cria um novo post"""
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        if content:
            post = Post.objects.create(
                user=request.user,
                content=content,
                image=image
            )
            return redirect('home')
    
    return render(request, 'posts/create.html')

def post_list_view(request):
    """Lista todos os posts (feed) com paginação"""
    # Query base para posts
    if request.user.is_authenticated:
        # Posts de quem você segue + seus próprios posts
        following_ids = list(request.user.following.values_list('id', flat=True))
        following_ids.append(request.user.id)  # Inclui o próprio usuário

        posts = Post.objects.filter(
            user_id__in=following_ids
        ).select_related('user').prefetch_related('likes', 'comments').order_by('-created_at')
    else:
        posts = Post.objects.all().select_related('user').prefetch_related('likes', 'comments').order_by('-created_at')

    # Paginação - 10 posts por página
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'posts/feed.html', {'page_obj': page_obj, 'is_personalized_feed': request.user.is_authenticated})

def post_detail_view(request, pk):
    """Detalhes de um post específico"""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/detail.html', {'post': post})

@login_required
def post_delete_view(request, pk):
    """Exclui um post"""
    post = get_object_or_404(Post, pk=pk)
    
    if post.user != request.user:
        return redirect('home')
    
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    
    return render(request, 'posts/confirm_delete.html', {'post': post})

@login_required
def like_post_view(request, pk):
    """Curte ou descurte um post"""
    post = get_object_or_404(Post, pk=pk)
    
    like_exists = Like.objects.filter(user=request.user, post=post).exists()
    
    if like_exists:
        Like.objects.filter(user=request.user, post=post).delete()
        liked = False
    else:
        Like.objects.create(user=request.user, post=post)
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'liked': liked,
            'likes_count': post.likes_count
        })
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

#Sistema de comentários

@login_required
def add_comment_view(request, pk):
    """Adiciona um comentário a um post"""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        
        if content and content.strip():
            Comment.objects.create(
                user=request.user,
                post=post,
                content=content.strip()
            )
    
    return redirect('post_detail', pk=post.pk)

@login_required
def delete_comment_view(request, pk):
    """Exclui um comentário"""
    comment = get_object_or_404(Comment, pk=pk)
    
    # Verifica se o usuário é o dono do comentário
    if comment.user != request.user:
        return redirect('post_detail', pk=comment.post.pk)
    
    if request.method == 'POST':
        post_pk = comment.post.pk
        comment.delete()
        return redirect('post_detail', pk=post_pk)
    
    return render(request, 'posts/comment_confirm_delete.html', {'comment': comment})