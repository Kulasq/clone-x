from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from .forms import RegisterForm, ProfileEditForm
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuario ou senha inválidos.')
    
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            # Form errors will be displayed in template
            pass
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_view(request):
    """Página de perfil do usuário logado"""
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def profile_edit_view(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            remove_photo = form.cleaned_data.get('remove_profile_picture')

            # Remove a foto se marcado
            if remove_photo and user.profile_picture:
                user.delete_profile_picture()
            
            # Salva o usuário (isso vai lidar com a substituição de imagem automaticamente)
            form.save()

            return redirect('profile')
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'users/profile_edit.html', {'form': form})

def public_profile_view(request, username):
    """Perfil público de qualquer usuário"""
    user = get_object_or_404(User, username=username)
    return render(request, 'users/public_profile.html', {'profile_user': user})

@login_required
def account_delete_view(request):
    """Exclui permanentemente a conta do usuário"""
    if request.method == 'POST':
        user = request.user
        
        # Logout antes de deletar
        from django.contrib.auth import logout
        logout(request)
        
        # Deleta o usuário
        user.delete()
        
        return redirect('home')
    
    return render(request, 'users/account_delete_confirm.html')

# Sistema de seguir
@login_required
def follow_user_view(request, username):
    """Segue ou deixa de seguir um usuário"""
    user_to_follow = get_object_or_404(User, username=username)
    
    if request.user == user_to_follow:
        return redirect('public_profile', username=username)
    
    if request.user.is_following(user_to_follow):
        request.user.unfollow(user_to_follow)
        following = False
    else:
        request.user.follow(user_to_follow)
        following = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'following': following,
            'followers_count': user_to_follow.followers_count
        })
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

@login_required
def following_list_view(request, username):
    """Lista de usuários que um usuário segue"""
    user = get_object_or_404(User, username=username)
    following = user.following.all()
    return render(request, 'users/following_list.html', {
        'profile_user': user,
        'users_list': following,
        'list_type': 'following'
    })

@login_required
def followers_list_view(request, username):
    """Lista de seguidores de um usuário"""
    user = get_object_or_404(User, username=username)
    followers = user.followers.all()
    return render(request, 'users/followers_list.html', {
        'profile_user': user,
        'users_list': followers,
        'list_type': 'followers'
    })

def user_search_view(request):
    """Busca simples de usuários com sugestões"""
    query = request.GET.get('q', '').strip()
    users = []
    suggested_users = []
    
    if query:
        # Busca por username, primeiro nome ou último nome
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).exclude(id=request.user.id if request.user.is_authenticated else None)
        results_count = users.count()  
    else:
        # Sugere usuários quando não há busca
        if request.user.is_authenticated:
            suggested_users = User.objects.exclude(id=request.user.id)[:8]
        else:
            suggested_users = User.objects.all()[:6]
        results_count = 0
    
    return render(request, 'users/search.html', {
        'query': query,
        'users': users,
        'suggested_users': suggested_users,
        'results_count': results_count 
    })

@login_required
def change_password_view(request):
    """View para alteração de senha"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Atualiza a sessão para não deslogar o usuário
            update_session_auth_hash(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'users/change_password.html', {'form': form})
