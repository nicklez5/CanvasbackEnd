from django.db import models
class Message(models.Model):
    author = models.CharField(max_length=100,unique=False)
    description = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    thread = models.ForeignKey('threads.Thread', on_delete=models.CASCADE,related_name='messages', null=True, blank=True)
# Create your models here.
