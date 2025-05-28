from django.db import models
from django.conf import settings 
class Thread(models.Model):
    title = models.CharField(max_length=200,blank=False)
    list_of_messages = models.ManyToManyField('message.Message',related_name='threads', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
# Create your models here.
