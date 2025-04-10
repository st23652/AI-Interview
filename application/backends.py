from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


# OopCompanion:suppressRename

UserModel = get_user_model()

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """Authenticate user with email and password."""
        if username is None or password is None:
            return None  # Ensure both email and password are provided

        try:
            user = UserModel.objects.get(email=username)  # Django passes 'username' as email
        except ObjectDoesNotExist:
            return None
        except MultipleObjectsReturned:
            return None  # Handle duplicate emails gracefully

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None

    def get_user(self, user_id):
        """Retrieve user by ID."""
        try:
            return UserModel.objects.get(pk=user_id)
        except ObjectDoesNotExist:
            return None

    def user_can_authenticate(self, user):
        """Ensure user is active before authenticating."""
        return user.is_active  # Optional, but recommended
