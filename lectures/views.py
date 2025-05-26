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
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'
class LectureUpdate(UpdateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = SerializeLecture
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'pk'
  
class LectureDelete(DestroyAPIView):
    queryset = Lecture.objects.all()
    serializer_class = SerializeLecture
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.file and instance.file.name:
            try:
                instance.file.delete(save=False)
                file_deleted = True
            except Exception as e:
                logger.error(f"Failed to delete file {instance.file.name}: {e}")
                file_deleted = False
                # Log error or handle it gracefully
        else:
            file_deleted = False
        self.perform_destroy(instance)
        if file_deleted:
            return Response({"detail": "Lecture and file deleted successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Lecture deleted, but file deletion failed."}, status=status.HTTP_200_OK)

# Create your views here.