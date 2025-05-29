from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import m2m_changed
from .models import Canvas
from course.models import Course
@receiver(m2m_changed, sender=Canvas.list_courses.through)
def add_profile_to_course(sender, instance, action, reverse, model, pk_set, **kwargs):
    """
    Whenever a course is added to a user's canvas (ManyToManyField), 
    add the profile to the course.
    """
    if action == "post_add":
        # We only want to act when courses are added to the Canvas
        for course_id in pk_set:
            course = Course.objects.get(id=course_id)
            # Add the profile to the course's profiles field
            course.profiles.add(instance.user.profile)  # Assuming `profile` is linked to `user`
            course.save()
    elif action == "post_remove":
        for course_id in pk_set:
            course = Course.objects.get(id=course_id)
            # Remove the profile from the course's profiles field
            course.profiles.remove(instance.user.profile)  # Assuming `profile` is linked to `user`
            course.save()
@receiver(post_save, sender=Canvas.list_courses.through)
def add_profile_to_course(sender, instance, action, reverse, model, pk_set, **kwargs):
    """
    Whenever a course is added to a user's canvas (ManyToManyField), 
    add the profile to the course.
    """
    

#post_save.connect(create_profile, sender=settings.AUTH_USER_MODEL