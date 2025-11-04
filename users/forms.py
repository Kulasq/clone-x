from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .validators import StrongPasswordValidator

User = get_user_model()

def validate_strong_password(password):
    """Valida se a senha atende aos critérios de segurança modernos."""
    errors = []
    
    if len(password) < 8:
        errors.append("Senha deve ter pelo menos 8 caracteres")
    
    if not re.search(r'[A-Z]', password):
        errors.append("Inclua pelo menos uma letra maiúscula")
    
    if not re.search(r'[a-z]', password):
        errors.append("Inclua pelo menos uma letra minúscula")
    
    if not re.search(r'\d', password):
        errors.append("Inclua pelo menos um número")
    
    if not re.search(r'[@$!%*?&]', password):
        errors.append("Inclua pelo menos um caractere especial (@$!%*?&)")
    
    if errors:
        raise ValidationError(errors)

def validate_username_no_spaces(value):
    """Valida se o username não contém espaços."""
    if ' ' in value:
        raise ValidationError("O nome de usuário não pode conter espaços.")

class RegisterForm(UserCreationForm):
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite uma senha forte'
        }),
        help_text=StrongPasswordValidator().get_help_text()
    )
    
    password2 = forms.CharField(
        label="Confirmação de senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Repita a senha'
        }),
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        validator = StrongPasswordValidator()
        validator.validate(password1)
        return password1
        
    def clean_username(self):
        username = self.cleaned_data.get('username')
        validate_username_no_spaces(username)
        return username

class ProfileEditForm(forms.ModelForm):
    """Formulário para edição de perfil, incluindo remoção da foto."""
    remove_profile_picture = forms.BooleanField(
        required=False,
        label='🗑️ Remover foto atual'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'location', 'website', 'profile_picture']
        widgets = {
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].label = 'Alterar foto'
