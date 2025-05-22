from django.db import models

class Thread(models.Model):
    list_messages = models.ManyToManyField('message.Message',related_name='list_messages',blank=True)
    last_author = models.CharField(max_length=100,unique=False)
    last_description = models.TextField(max_length=200)
    last_timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)
# Create your models here.
