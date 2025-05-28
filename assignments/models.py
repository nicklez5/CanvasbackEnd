from django.db import models
from django.conf import settings 
from django.utils.translation import gettext_lazy as _
from django import forms 
from django.core.files.storage import storages
def select_storage():
    return storages["mystorage"]
class Assignment(models.Model):
    name = models.CharField(max_length=100,unique=False)
    submitter = models.CharField(max_length=100,unique=False,null=True,blank=True)
    date_due = models.DateTimeField(null=True,blank=True)
    max_points = models.IntegerField(null=True,blank=True)
    student_points = models.IntegerField(default=0,null=True,blank=True)
    description = models.TextField(max_length=100,blank=True)
    assignment_file = models.FileField(storage=select_storage,upload_to="assignments/",null=True,blank=True)
    student_file = models.FileField(storage=select_storage,upload_to="assignments/", null=True, blank=True)
    def __str__(self):
        return self.name 

    class Meta:
        ordering = ['date_due']
        db_table = "assignment"
