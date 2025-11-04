from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from users.validators import StrongPasswordValidator
from users.forms import RegisterForm

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertTrue(self.user.check_password('testpass'))

    def test_follow_system(self):
        user2 = User.objects.create_user(username='user2', email='user2@example.com', password='pass')
        self.user.follow(user2)
        self.assertTrue(self.user.is_following(user2))
        self.assertEqual(user2.followers_count, 1)

class UserViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'NewPass@1234',
            'password2': 'NewPass@1234'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_change_password_view(self):
        """Testa alteração de senha"""
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('change_password'), {
            'old_password': 'testpass',
            'new_password1': 'NewTest@1234',
            'new_password2': 'NewTest@1234'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after success
        # Verifica se a senha foi alterada
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewTest@1234'))

class StrongPasswordValidatorTest(TestCase):
    def setUp(self):
        self.validator = StrongPasswordValidator()

    def test_valid_password(self):
        """Testa senha válida"""
        valid_passwords = [
            'Test@1234',
            'SenhaForte!99',
            'ABCabc123&',
            'Minha@Senha123'
        ]
        
        for password in valid_passwords:
            with self.subTest(password=password):
                # Não deve levantar exceção
                self.validator.validate(password)

    def test_short_password(self):
        """Testa senha muito curta"""
        with self.assertRaises(ValidationError) as context:
            self.validator.validate('Test@12')
        
        self.assertIn('Senha deve ter pelo menos 8 caracteres.', str(context.exception))

    def test_no_uppercase(self):
        """Testa senha sem maiúscula"""
        with self.assertRaises(ValidationError) as context:
            self.validator.validate('test@1234')
        
        self.assertIn('Senha deve conter pelo menos uma letra maiúscula.', str(context.exception))

    def test_no_lowercase(self):
        """Testa senha sem minúscula"""
        with self.assertRaises(ValidationError) as context:
            self.validator.validate('TEST@1234')
        
        self.assertIn('Senha deve conter pelo menos uma letra minúscula.', str(context.exception))

    def test_no_number(self):
        """Testa senha sem número"""
        with self.assertRaises(ValidationError) as context:
            self.validator.validate('Test@abcd')
        
        self.assertIn('Senha deve conter pelo menos um número.', str(context.exception))

    def test_no_special_char(self):
        """Testa senha sem caractere especial"""
        with self.assertRaises(ValidationError) as context:
            self.validator.validate('Test12345')
        
        self.assertIn('Senha deve conter pelo menos um caractere especial (@$!%*?&.,).', str(context.exception))

    def test_multiple_errors(self):
        """Testa senha com múltiplos erros"""
        with self.assertRaises(ValidationError) as context:
            self.validator.validate('test')
        
        errors = str(context.exception)
        self.assertIn('Senha deve ter pelo menos 8 caracteres.', errors)
        self.assertIn('Senha deve conter pelo menos uma letra maiúscula.', errors)
        self.assertIn('Senha deve conter pelo menos um número.', errors)
        self.assertIn('Senha deve conter pelo menos um caractere especial (@$!%*?&.,).', errors)

class RegisterFormTest(TestCase):
    def test_valid_registration(self):
        """Testa registro válido"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'Test@1234',
            'password2': 'Test@1234',
        }
        form = RegisterForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_weak_password_rejection(self):
        """Testa rejeição de senha fraca"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'test',  # Senha fraca
            'password2': 'test',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)

    def test_password_mismatch(self):
        """Testa senhas não coincidem"""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com', 
            'password1': 'Test@1234',
            'password2': 'Different@1234',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_username_no_spaces(self):
        """Testa rejeição de username com espaços"""
        form_data = {
            'username': 'test user',
            'email': 'test@example.com',
            'password1': 'Test@1234',
            'password2': 'Test@1234',
        }
        form = RegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
        self.assertIn('O nome de usuário não pode conter espaços.', str(form.errors['username']))
