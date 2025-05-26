from rest_framework import serializers
from rest_framework.exceptions import NotFound
from .models import Course
from lectures.models import Lecture
from profiles.models import Profile
from assignments.models import Assignment
from tests.models import Tests
from threads.models import Thread
from lectures.serializers import SerializeLecture
from profiles.serializers import SerializeProfile
from assignments.serializers import SerializeAssignment
from tests.serializers import SerializeTest
from threads.serializers import SerializeThread

class SerializeCourse(serializers.ModelSerializer):
    # For writing: Use PrimaryKeyRelatedField for many-to-many fields
    lectures = serializers.PrimaryKeyRelatedField(many=True, queryset=Lecture.objects.all(), write_only=True)
    profiles = serializers.PrimaryKeyRelatedField(many=True, queryset=Profile.objects.all(), write_only=True)
    assignments = serializers.PrimaryKeyRelatedField(many=True, queryset=Assignment.objects.all(), write_only=True)
    tests = serializers.PrimaryKeyRelatedField(many=True, queryset=Tests.objects.all(), write_only=True)
    threads = serializers.PrimaryKeyRelatedField(many=True, queryset=Thread.objects.all(), write_only=True)

    # For reading: SerializerMethodFields to display related objects
    lectures_detail = serializers.SerializerMethodField(read_only=True)
    profiles_detail = serializers.SerializerMethodField(read_only=True)
    assignments_detail = serializers.SerializerMethodField(read_only=True)
    tests_detail = serializers.SerializerMethodField(read_only=True)
    threads_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'lectures', 'profiles', 'assignments', 'tests', 'threads',
                  'lectures_detail', 'profiles_detail', 'assignments_detail', 'tests_detail', 'threads_detail']

    # Method to get related lectures details
    def get_lectures_detail(self, obj):
        try:
            lectures = obj.lectures.all()
            if not lectures:
                raise NotFound("No lectures found for this course.")
            return SerializeLecture(lectures, many=True).data
        except Exception as e:
            return {"detail": f"Error fetching lectures: {str(e)}"}

    # Method to get related profiles details
    def get_profiles_detail(self, obj):
        try:
            profiles = obj.profiles.all()
            if not profiles:
                raise NotFound("No profiles found for this course.")
            return SerializeProfile(profiles, many=True).data
        except Exception as e:
            return {"detail": f"Error fetching profiles: {str(e)}"}

    # Method to get related assignments details
    def get_assignments_detail(self, obj):
        try:
            assignments = obj.assignments.all()
            if not assignments:
                raise NotFound("No assignments found for this course.")
            return SerializeAssignment(assignments, many=True).data
        except Exception as e:
            return {"detail": f"Error fetching assignments: {str(e)}"}

    # Method to get related tests details
    def get_tests_detail(self, obj):
        try:
            tests = obj.tests.all()
            if not tests:
                raise NotFound("No tests found for this course.")
            return SerializeTest(tests, many=True).data
        except Exception as e:
            return {"detail": f"Error fetching tests: {str(e)}"}

    # Method to get related threads details
    def get_threads_detail(self, obj):
        try:
            threads = obj.threads.all()
            if not threads:
                raise NotFound("No threads found for this course.")
            return SerializeThread(threads, many=True).data
        except Exception as e:
            return {"detail": f"Error fetching threads: {str(e)}"}

    # Override the update() method to dynamically add/remove related objects
    def update(self, instance, validated_data):
        # Get the related fields from the validated_data (if they exist)
        lectures_data = validated_data.pop('lectures', [])
        profiles_data = validated_data.pop('profiles', [])
        assignments_data = validated_data.pop('assignments', [])
        tests_data = validated_data.pop('tests', [])
        threads_data = validated_data.pop('threads', [])

        # Update the basic fields (e.g., course name)
        instance.name = validated_data.get('name', instance.name)

        # Add new lectures to the course
        if lectures_data:
            lectures_to_add = Lecture.objects.filter(id__in=lectures_data)
            instance.lectures.add(*lectures_to_add)

        # Remove lectures from the course
        if 'remove_lectures' in validated_data:
            lectures_to_remove = validated_data.get('remove_lectures')
            instance.lectures.remove(*lectures_to_remove)

        # Add/remove profiles, assignments, tests, threads similarly

        if profiles_data:
            profiles_to_add = Profile.objects.filter(id__in=profiles_data)
            instance.profiles.add(*profiles_to_add)
            
        if 'remove_profiles' in validated_data:
            profiles_to_remove = validated_data.get('remove_profiles')
            instance.profiles.remove(*profiles_to_remove)

        if assignments_data:
            assignments_to_add = Assignment.objects.filter(id__in=assignments_data)
            instance.assignments.add(*assignments_to_add)
        
        if 'remove_assignments' in validated_data:
            assignments_to_remove = validated_data.get('remove_assignments')
            instance.assignments.remove(*assignments_to_remove)

        if tests_data:
            tests_to_add = Tests.objects.filter(id__in=tests_data)
            instance.tests.add(*tests_to_add)
        
        if 'remove_tests' in validated_data:
            tests_to_remove = validated_data.get('remove_tests')
            instance.tests.remove(*tests_to_remove)

        if threads_data:
            threads_to_add = Thread.objects.filter(id__in=threads_data)
            instance.threads.add(*threads_to_add)
        
        if 'remove_threads' in validated_data:
            threads_to_remove = validated_data.get('remove_threads')
            instance.threads.remove(*threads_to_remove)

        # Save the updated course
        instance.save()
        return instance
