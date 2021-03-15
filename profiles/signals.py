from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import User

from .models import Profile

@receiver(post_save, sender=User)
def attach_profile(sender, instance, created, *args, **kwargs):
    if instance and created:
        sender.profile = Profile.objects.create(user=instance)
