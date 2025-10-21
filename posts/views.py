from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Like
from django.contrib.auth import get_user_model

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
            messages.success(request, 'Post criado com sucesso!')
            return redirect('home')
        else:
            messages.error(request, 'O conteúdo do post não pode estar vazio.')
    
    return render(request, 'posts/create.html')

def post_list_view(request):
    """Lista todos os posts (feed)"""
    posts = Post.objects.all().select_related('user')
    return render(request, 'posts/feed.html', {'posts': posts})

def post_detail_view(request, pk):
    """Detalhes de um post específico"""
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/detail.html', {'post': post})

@login_required
def post_delete_view(request, pk):
    """Exclui um post"""
    post = get_object_or_404(Post, pk=pk)
    
    # Verifica se o usuário é o dono do post
    if post.user != request.user:
        messages.error(request, 'Você não tem permissão para excluir este post.')
        return redirect('post_detail', pk=post.pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post excluído com sucesso!')
        return redirect('home')
    
    return render(request, 'posts/confirm_delete.html', {'post': post})

@login_required
def like_post_view(request, pk):
    """Curte ou descurte um post"""
    post = get_object_or_404(Post, pk=pk)
    
    # Verifica se o usuário já curtiu o post
    like_exists = Like.objects.filter(user=request.user, post=post).exists()
    
    if like_exists:
        # Descurtir
        Like.objects.filter(user=request.user, post=post).delete()
        messages.info(request, 'Post descurtido.')
    else:
        # Curtir
        Like.objects.create(user=request.user, post=post)
        messages.success(request, 'Post curtido!')
    
    return redirect('home')