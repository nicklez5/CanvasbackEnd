from django.core.files.storage import FileSystemStorage
import logging
from django.shortcuts import render
from .models import Lecture
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser,FormParser
from rest_framework import serializers, status 
from .serializers import SerializeLecture 
from rest_framework.generics import UpdateAPIView,RetrieveAPIView,DestroyAPIView, CreateAPIView, ListAPIView
from django.forms import ValidationError
logger = logging.getLogger(__name__)  
class LectureList(ListAPIView):
    queryset = Lecture.objects.all()
    serializer_class = SerializeLecture
    permission_classes = [IsAuthenticated]

class LecturePost(CreateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = SerializeLecture
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

class LectureDetail(RetrieveAPIView):
    queryset = Lecture.objects.all()
    serializer_class = SerializeLecture
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
class LectureUpdate(UpdateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = SerializeLecture
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'pk'
    def update(self, request, *args, **kwargs):
        """Override the update method to handle custom logic, including file uploads"""
        lecture = self.get_object()  # Retrieve the lecture object based on pk

        # Check if the data is valid and perform the update
        serializer = self.get_serializer(lecture, data=request.data, partial=True)  # partial=True allows partial updates

        if serializer.is_valid():
            # Save the updated lecture data
            serializer.save()

            # Custom logic if needed (e.g., logging or notifications)
            # For example, sending a notification or logging the update.

            # Return the serialized updated lecture data
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LectureDelete(DestroyAPIView):
    queryset = Lecture.objects.all()
    serializer_class = SerializeLecture
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # Try to delete the associated file first, then delete the instance.
        try:
            if instance.file:
                instance.file.delete(save=False)  # Remove file from storage
            instance.delete()  # Delete the instance itself
        except Exception as e:
            # Log the error for debugging purposes
            logger.error(f"Error deleting lecture with id {instance.pk}: {str(e)}")
            # Raise a ValidationError or a NotFound error with a custom message
            raise ValidationError(f"Error deleting files or instance: {str(e)}")

# Create your views here.