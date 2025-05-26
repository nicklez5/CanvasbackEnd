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
def remove_from_courses(instance):
    try:
        for course in instance.courses.all():
            field = None
            if isinstance(instance, Lecture):
                course.lectures.remove(instance)
            elif isinstance(instance, Assignment):
                course.assignments.remove(instance)
            elif isinstance(instance, Profile):
                course.profiles.remove(instance)
            elif isinstance(instance, Tests):
                course.tests.remove(instance)
            elif isinstance(instance, Thread):
                course.threads.remove(instance)
            update_canvas_for_course(course)
    except Exception as e:
        print(f"[ERROR] Failed to remove {instance} from related courses: {e}")

@receiver(post_delete, sender=Lecture)
def lecture_deleted(sender, instance, **kwargs):
    remove_from_courses(instance)

@receiver(post_delete, sender=Assignment)
def assignment_deleted(sender, instance, **kwargs):
    remove_from_courses(instance)

@receiver(post_delete, sender=Profile)
def profile_deleted(sender, instance, **kwargs):
    remove_from_courses(instance)

@receiver(post_delete, sender=Tests)
def tests_deleted(sender, instance, **kwargs):
    remove_from_courses(instance)

@receiver(post_delete, sender=Thread)
def thread_deleted(sender, instance, **kwargs):
    remove_from_courses(instance)