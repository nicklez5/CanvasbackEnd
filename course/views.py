from django.shortcuts import get_object_or_404, render
from django.conf import settings
from rest_framework.decorators import action, permission_classes 
from .models import Course
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework import serializers, status, viewsets 
from rest_framework.decorators import api_view, parser_classes, permission_classes
from .serializers import SerializeCourse,SerializeAssignment, SerializeLecture
from lectures.models import Lecture 
from assignments.models import Assignment
from profiles.models import Profile 
from tests.models import Tests
from users.models import CustomUser
from mycanvas.models import Canvas
from threads.models import Thread 
from django.core.files.storage import FileSystemStorage
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from .signals import update_canvas_for_course
import json
import django.dispatch 
from rest_framework.generics import UpdateAPIView,RetrieveAPIView,DestroyAPIView, CreateAPIView, ListAPIView,RetrieveUpdateAPIView
class CourseListView(ListAPIView):
    queryset = Course.objects.all()
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Using prefetch_related for efficient querying
        courses = Course.objects.prefetch_related(
            'lectures', 
            'profiles', 
            'assignments', 
            'tests', 
            'threads'
        )
        serializer = SerializeCourse(courses, many=True)
        return Response(serializer.data)
class CoursePostView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = SerializeCourse
    permission_classes = [IsAdminUser]

class CourseDetailView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = SerializeCourse
    permission_classes = [IsAuthenticated]
class CourseUpdateView(UpdateAPIView):
    queryset = Course.objects.all()  # Default queryset for retrieving all courses
    serializer_class = SerializeCourse
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        # Use prefetch_related to efficiently fetch related data
        return Course.objects.prefetch_related(
            'lectures', 'profiles', 'assignments', 'tests', 'threads'
        )

    def update(self, request, *args, **kwargs):
        # Fetch the course object using the custom queryset (including prefetching related data)
        course = self.get_object()
        data = request.data
        
        # Update basic fields
        course.name = data.get('name', course.name)

        # Update many-to-many relationships
        for field_name in ['lectures', 'assignments', 'profiles', 'tests', 'threads']:
            related_field_data = data.get(field_name, [])
            related_objects = globals()[field_name.capitalize()].objects.filter(id__in=related_field_data)
            getattr(course, field_name).set(related_objects)

        course.save()

        # Return the updated course data using the serializer
        serializer = self.get_serializer(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
class CourseUpdateLecturesAPIView(APIView):
    permission_classes = [IsAdminUser]  # Only admin users can modify the lectures for the course
    
    def get_object(self, pk):
        try:
            return Course.objects.prefetch_related('lectures').get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk, format=None):
        """
        Update the lectures of a specific course by adding or removing lectures.
        """
        course = self.get_object(pk)  # Get the Course object
        
        if isinstance(course, Response):  # If the course doesn't exist, return the error response
            return course
        
        # Data passed in the request for adding and removing lectures
        add_lectures = request.data.get('add_lectures', [])
        remove_lectures = request.data.get('remove_lectures', [])
        
        # Add new lectures to the course
        if add_lectures:
            lectures_to_add = Lecture.objects.filter(id__in=add_lectures)
            course.lectures.add(*lectures_to_add)
        
        # Remove lectures from the course
        if remove_lectures:
            lectures_to_remove = Lecture.objects.filter(id__in=remove_lectures)
            course.lectures.remove(*lectures_to_remove)
        
        # Save the course after making changes
        course.save()
        
        # Return the updated course data
        serializer = SerializeCourse(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
class CourseUpdateProfilesAPIView(APIView):
    permission_classes = [IsAdminUser]  # Only admin users can modify the lectures for the course
    
    def get_object(self, pk):
        try:
            return Course.objects.prefetch_related('profiles').get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk, format=None):
        """
        Update the profiles of a specific course by adding or removing profiles.
        """
        course = self.get_object(pk)  # Get the Course object
        
        if isinstance(course, Response):  # If the course doesn't exist, return the error response
            return course
        
        # Data passed in the request for adding and removing profiles
        add_profiles = request.data.get('add_profiles', [])
        remove_profiles = request.data.get('remove_profiles', [])
        
        # Add new profiles to the course
        if add_profiles:
            profiles_to_add = Profile.objects.filter(id__in=add_profiles)
            course.profiles.add(*profiles_to_add)
        
        # Remove profiles from the course
        if remove_profiles:
            profiles_to_remove = Profile.objects.filter(id__in=remove_profiles)
            course.profiles.remove(*profiles_to_remove)
        
        # Save the course after making changes
        course.save()
        
        # Return the updated course data
        serializer = SerializeCourse(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
class CourseUpdateAssignmentsAPIView(APIView):
    permission_classes = [IsAdminUser]  # Only admin users can modify the lectures for the course
    
    def get_object(self, pk):
        try:
            return Course.objects.prefetch_related('assignments').get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk, format=None):
        """
        Update the assignments of a specific course by adding or removing assignments.
        """
        course = self.get_object(pk)  # Get the Course object
        
        if isinstance(course, Response):  # If the course doesn't exist, return the error response
            return course
        
        # Data passed in the request for adding and removing assignments
        add_assignments = request.data.get('add_assignments', [])
        remove_assignments = request.data.get('remove_assignments', [])
        
        # Add new assignments to the course
        if add_assignments:
            assignments_to_add = Assignment.objects.filter(id__in=add_assignments)
            course.assignments.add(*assignments_to_add)
        
        # Remove assignments from the course
        if remove_assignments:
            assignments_to_remove = Assignment.objects.filter(id__in=remove_assignments)
            course.assignments.remove(*assignments_to_remove)
        
        # Save the course after making changes
        course.save()
        
        # Return the updated course data
        serializer = SerializeCourse(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
class CourseUpdateTestsAPIView(APIView):
    permission_classes = [IsAdminUser]  # Only admin users can modify the lectures for the course
    
    def get_object(self, pk):
        try:
            return Course.objects.prefetch_related('tests').get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk, format=None):
        """
        Update the tests of a specific course by adding or removing tests.
        """
        course = self.get_object(pk)  # Get the Course object
        
        if isinstance(course, Response):  # If the course doesn't exist, return the error response
            return course
        
        # Data passed in the request for adding and removing tests
        add_tests = request.data.get('add_tests', [])
        remove_tests = request.data.get('remove_tests', [])
        
        # Add new tests to the course
        if add_tests:
            tests_to_add = Tests.objects.filter(id__in=add_tests)
            course.tests.add(*tests_to_add)
        
        # Remove tests from the course
        if remove_tests:
            tests_to_remove = Tests.objects.filter(id__in=remove_tests)
            course.tests.remove(*tests_to_remove)
        
        # Save the course after making changes
        course.save()
        
        # Return the updated course data
        serializer = SerializeCourse(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
class CourseUpdateThreadsAPIView(APIView):
    permission_classes = [IsAdminUser]  # Only admin users can modify the lectures for the course
    
    def get_object(self, pk):
        try:
            return Course.objects.prefetch_related('threads').get(pk=pk)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, pk, format=None):
        """
        Update the threads of a specific course by adding or removing threads.
        """
        course = self.get_object(pk)  # Get the Course object
        
        if isinstance(course, Response):  # If the course doesn't exist, return the error response
            return course
        
        # Data passed in the request for adding and removing threads
        add_threads = request.data.get('add_threads', [])
        remove_threads = request.data.get('remove_threads', [])
        
        # Add new threads to the course
        if add_threads:
            threads_to_add = Thread.objects.filter(id__in=add_threads)
            course.threads.add(*threads_to_add)
        
        # Remove threads from the course
        if remove_threads:
            threads_to_remove = Thread.objects.filter(id__in=remove_threads)
            course.threads.remove(*threads_to_remove)
        
        # Save the course after making changes
        course.save()
        
        # Return the updated course data
        serializer = SerializeCourse(course)
        return Response(serializer.data, status=status.HTTP_200_OK)
class CourseDeleteView(DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = SerializeCourse
    permission_classes = [IsAdminUser]
    def destroy(self, request, *args, **kwargs):
        # You can add custom logic before deleting, like logging
        instance = self.get_object()  # Get the object to be deleted
        self.perform_destroy(instance)  # Perform the deletion
        
        # Return a custom response
        return Response({"message": "Course deleted successfully."}, status=200)

    




    
        

        
e
    

# Create your views here.