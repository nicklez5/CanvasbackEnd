from django.shortcuts import render, redirect 
from rest_framework.decorators import action, permission_classes 
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response 
from rest_framework import status, viewsets
from course.serializers import SerializeCourse
from .serializers import SerializeCanvas
from .models import Canvas 
from course.models import Course
from rest_framework.generics import UpdateAPIView,RetrieveAPIView,DestroyAPIView, CreateAPIView, ListAPIView
from django.shortcuts import get_object_or_404

    
class CanvasView(RetrieveAPIView):
    serializer_class = SerializeCanvas
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        """
        Override to restrict Canvas objects to the current authenticated user.
        """
        user = self.request.user
        return Canvas.objects.filter(user=user)


class CanvasCourse(APIView):
    serializer_class = SerializeCanvas
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        """Helper method to retrieve the Canvas object or raise a 404 error"""
        return get_object_or_404(Canvas, pk=pk)

    def put(self, request, pk, format=None):
        """Remove a course from the Canvas' list_courses (ManyToManyField)"""
        data = request.data
        canvas = self.get_object(pk)

        course_ID = data.get('id')
        if not course_ID:
            return Response({"detail": "Course ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, pk=course_ID)
         # Get course, raises 404 if not found
        canvas.list_courses.remove(course)
        canvas.save()

        # Return the updated Canvas with courses
        serializer = self.serializer_class(canvas)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        """Add a course to the Canvas' list_courses (ManyToManyField)"""
        data = request.data
        canvas = self.get_object(pk)

        course_ID = data.get('id')
        if not course_ID:
            return Response({"detail": "Course ID is required."}, status=status.HTTP_400_BAD_REQUEST)

        course = get_object_or_404(Course, pk=course_ID)  # Get course, raises 404 if not found
        canvas.list_courses.add(course)
        canvas.save()

        # Return the updated Canvas with courses
        serializer = self.serializer_class(canvas)
        return Response(serializer.data)



