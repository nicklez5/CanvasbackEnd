
from django.db.models.signals import post_save ,post_delete
from django.conf import settings
from .models import Message
from django.dispatch import receiver
from course.models import Course
from lectures.models import Lecture
from assignments.models import Assignment
from profiles.models import Profile
from tests.models import Tests
from threads.models import Thread
from course.signals import update_canvas_for_course


receiver(post_save, sender=Message)
def update_thread_last_message(sender, instance, created, **kwargs):
    if created:
        # Get the associated thread for the message
        thread = instance.thread
        
        if thread:
            # Update the last fields on the thread
            thread.last_author = instance.author
            thread.last_description = instance.description
            thread.last_timestamp = instance.timestamp
            thread.save()
 # Adjust path if needed

# Generic cleanup signal for any model with related_name='courses'
