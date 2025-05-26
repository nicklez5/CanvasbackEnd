from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Canvas

#post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL