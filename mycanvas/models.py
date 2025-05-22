from django.db import models
from django.conf import settings 
from course.models import Course 
class Canvas(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,blank=True)
    list_courses = models.ManyToManyField('course.Course')

    