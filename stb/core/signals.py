from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from stb.core.models import Profile
from django.contrib.auth.models import User


@receiver(pre_save, sender=User)
def update_user_profile(sender, instance, *args, **kwargs):
    instance.is_staff = True


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        profile.save()


"""
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
"""
