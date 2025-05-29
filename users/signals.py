
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from profiles.models import Profile
from mycanvas.models import Canvas
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
    else:
        # Update the profile if necessary (not always needed)
        instance.profile.save()
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_Canvas(sender, instance, created, **kwargs):
    if created:
        Canvas.objects.get_or_create(user=instance)

