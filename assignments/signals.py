from django.db.models.signals import post_delete
from django.dispatch import receiver
from course.models import Course
from lectures.models import Lecture
from assignments.models import Assignment
from profiles.models import Profile
from tests.models import Tests
from threads.models import Thread
from course.signals import update_canvas_for_course  # Adjust path if needed

# Generic cleanup signal for any model with related_name='courses'
