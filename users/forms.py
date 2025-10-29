from django import forms
from django.forms import ClearableFileInput
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': field.label
            })


class ProfileEditForm(forms.ModelForm):
    """Formulário para edição de perfil, incluindo remoção da foto."""
    remove_profile_picture = forms.BooleanField(
        required=False,
        label='Remover foto atual'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'location', 'website', 'profile_picture']
        widgets = {
            'profile_picture': ClearableFileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }
