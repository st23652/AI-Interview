from django.apps import AppConfig
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model


# OopCompanion:suppressRename

# Import or define your signal handler here
def user_saved_handler(sender, instance, created, **kwargs):
    if created:
        print(f"A new user {instance.email} has been created!")
    else:
        print(f"The user {instance.email} has been updated!")

class MyAppConfig(AppConfig):
    name = 'application'
    
    def ready(self):
        # Import the model inside the ready method to avoid circular imports
        User = get_user_model()

        # Connect the signal
        post_save.connect(user_saved_handler, sender=User)
