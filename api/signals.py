from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

from rest_framework.authtoken.models import Token

from api.models import UserProfile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_token(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a token
    for a new user.
    """
    if created:
        token = Token.objects.create(user=instance)
        token.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a user profile
    for a new user.
    """
    if created:
        profile = UserProfile.objects.create(user=instance)
        profile.save()
