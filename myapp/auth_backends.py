from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    def validate(self, password, user=None):
        # Example: Require passwords to have at least one uppercase letter and one special character
        if not any(char.isupper() for char in password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in password):
            raise ValidationError("Password must contain at least one special character.")

    def get_help_text(self):
        return "Your password must contain at least one uppercase letter and one special character."


class CustomUserAttributeSimilarityValidator:
    def validate(self, password, user=None):
        # Example: Prevent passwords similar to the username or email
        if user:
            if user.username and user.username.lower() in password.lower():
                raise ValidationError("Password cannot contain your username.")
            if user.email and user.email.split('@')[0].lower() in password.lower():
                raise ValidationError("Password cannot contain parts of your email address.")

    def get_help_text(self):
        return "Your password cannot contain your username or parts of your email address."
