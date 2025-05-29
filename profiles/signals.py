from django.db.models.signals import post_save 
from django.conf import settings
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=Profile)
def sync_profile_with_courses(sender, instance, created, **kwargs):
    """
    This signal will update the courses associated with the profile
    when the profile is updated.
    """
    if not created:  # Only trigger when the profile is updated (not created)
        # Get all courses that are related to this profile
        courses = instance.courses.all()

        for course in courses:
            # You can add any custom logic here to sync or reflect profile changes in courses
            # For instance, updating the course name or adding/removing the profile in other ways
            # In this case, the profile data in the course should reflect the updated profile.
            # For example, you can update course info or other related fields if needed.
            
            # This example doesn't require updates to the course, but in a real-world
            # scenario, you may want to modify course fields based on the profile update.
            course.save()