from django.db import models
from users.models import CustomUser
from django.conf import settings
class Message(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    body =  models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now=True,null=True,blank=True)
    
# Create your models here.
