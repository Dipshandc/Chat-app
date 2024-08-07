from django.db.models.signals import post_save
from authentication.models import CustomUser,UserProfile
from django.dispatch import receiver
from django.utils import timezone
 
@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)