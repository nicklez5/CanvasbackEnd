
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



# @receiver(post_save, sender=Message)
# def update_thread_last_message(sender, instance, created, **kwargs):
#     # Get the associated thread for the message
#     thread = instance.thread

#     if thread:
#         # If it's a newly created message, update the last message info
#         if created:
#             thread.author = instance.author
#         else:
#             # If the message is updated, check if it is the most recent one
#             last_message = thread.messages.order_by('-timestamp').first()
#             if last_message:
#                 if last_message.pk == instance.pk:
#                     thread.last_author = instance.author
#                     thread.last_description = instance.description
#                     thread.last_timestamp = instance.timestamp
#             else:
#                 thread.last_author = ''
#                 thread.last_description = ''
#                 thread.last_timestamp = None
#         thread.save()

 # Adjust path if needed

# Generic cleanup signal for any model with related_name='courses'
