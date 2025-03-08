from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth.password_validation import UserAttributeSimilarityValidator

class CustomPasswordValidator:
    def validate(self, password, user=None):
        # Minimum length check (at least 8 characters)
        if len(password) < 8:
            raise ValidationError(
                _("This password is too short. It must contain at least 8 characters."),
                code='password_too_short',
            )

        # Check if the password is entirely numeric
        if password.isdigit():
            raise ValidationError(
                _("This password is entirely numeric."),
                code='password_entirely_numeric',
            )

        # Check if the password is a commonly used password
        common_passwords = [
            'password', '123456', '123456789', 'qwerty', 'abc123', 'password1', '12345678', '12345'
        ]
        if password.lower() in common_passwords:
            raise ValidationError(
                _("This password is too common."),
                code='password_common',
            )

        # Check if the password is too similar to user attributes (e.g., username, email)
        if user:
            user_attributes = [user.username, user.email]
            if any(attr.lower() in password.lower() for attr in user_attributes):
                raise ValidationError(
                    _("Your password can’t be too similar to your other personal information."),
                    code='password_too_similar',
                )

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters, "
            "not be entirely numeric, and not be a commonly used password."
        )

# You may also choose to inherit from Django's built-in validators
class CustomUserAttributeSimilarityValidator(UserAttributeSimilarityValidator):
    def validate(self, password, user=None):
        super().validate(password, user)
        # Any additional custom checks can be added here

    def get_help_text(self):
        return _("Your password can’t be too similar to your other personal information.")
