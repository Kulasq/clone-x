from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model  

User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Validações
        if password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
            return render(request, 'users/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe.')
            return render(request, 'users/register.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'E-mail já cadastrado.')
            return render(request, 'users/register.html')
        
        # Criar usuário
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            login(request, user)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo(a), {user.username}!')
            return redirect('home')
        except Exception as e:
            messages.error(request, 'Erro ao criar conta. Tente novamente.')
    
    return render(request, 'users/register.html')

@login_required
def profile_view(request):
    """Página de perfil do usuário logado"""
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def profile_edit_view(request):
    """Edição do perfil do usuário"""
    if request.method == 'POST':
        user = request.user
        
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.bio = request.POST.get('bio', user.bio)
        user.location = request.POST.get('location', user.location)
        user.website = request.POST.get('website', user.website)

        if 'profile_picture' in request.FILES:
            user.profile_picture = request.FILES['profile_picture']
        
        user.save()
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('profile')
    
    return render(request, 'users/profile_edit.html')

def public_profile_view(request, username):
    """Perfil público de qualquer usuário"""
    user = get_object_or_404(User, username=username)
    return render(request, 'users/public_profile.html', {'profile_user': user})