import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class StrongPasswordValidator:
    """
    Validador personalizado para senhas fortes
    """
    def validate(self, password, user=None):
        errors = []
        
        # Verifica comprimento mínimo
        if len(password) < 8:
            errors.append(ValidationError(
                _("Senha deve ter pelo menos 8 caracteres."),
                code='password_too_short',
            ))
        
        # Verifica letra maiúscula
        if not re.search(r'[A-Z]', password):
            errors.append(ValidationError(
                _("Senha deve conter pelo menos uma letra maiúscula."),
                code='password_no_upper',
            ))
            
        # Verifica letra minúscula
        if not re.search(r'[a-z]', password):
            errors.append(ValidationError(
                _("Senha deve conter pelo menos uma letra minúscula."),
                code='password_no_lower',
            ))
            
        # Verifica número
        if not re.search(r'[0-9]', password):
            errors.append(ValidationError(
                _("Senha deve conter pelo menos um número."),
                code='password_no_number',
            ))
            
        # Verifica caractere especial
        if not re.search(r'[@$!%*?&.,]', password):
            errors.append(ValidationError(
                _("Senha deve conter pelo menos um caractere especial (@$!%*?&.,)."),
                code='password_no_special',
            ))
        
        # Levanta todos os erros encontrados
        if errors:
            raise ValidationError(errors)

    def get_help_text(self):
        return _(
            "Sua senha deve conter:\n"
            "- Mínimo 8 caracteres\n"
            "- Pelo menos 1 letra maiúscula\n" 
            "- Pelo menos 1 letra minúscula\n"
            "- Pelo menos 1 número\n"
            "- Pelo menos 1 caractere especial (@$!%*?&.,)"
        )
