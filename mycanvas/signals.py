from django.db.models.signals import post_save 
from django.conf import settings
from django.dispatch import receiver
from .models import Canvas

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_canvas(sender, instance, created, **kwargs):
    if created:
        Canvas.objects.create(user=instance)
        print('Canvas created!')

#post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_canvas(sender, instance, **kwargs):
    instance.canvas.save()
    print('Canvas updated!')