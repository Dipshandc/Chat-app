from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    def ready(self):
        from .signals.handlers import  create_profile
        from .models import CustomUser
        from django.db.models.signals import post_save
        post_save.connect(create_profile, sender=CustomUser)