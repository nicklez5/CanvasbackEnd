from datetime import timezone
from django.db import models
from django.conf import settings 
from course.models import Course 
class Canvas(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='canvas'
    )
    list_courses = models.ManyToManyField('course.Course',blank=True)
    def __str__(self):
        return f"Canvas for {self.user.email}"

    