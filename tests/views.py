from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.parsers import FormParser, MultiPartParser
from .models import Tests
from .serializers import SerializeTest
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status
from .forms import TestForm
from rest_framework.generics import UpdateAPIView,RetrieveAPIView,DestroyAPIView, CreateAPIView, ListAPIView

class TestListView(ListAPIView):
    queryset = Tests.objects.all()
    serializer_class = SerializeTest
    permission_classes = [IsAuthenticated]
    
class TestPostView(CreateAPIView):
    queryset = Tests.objects.all()
    serializer_class = SerializeTest
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]


class TestDetailView(RetrieveAPIView):
    queryset = Tests.objects.all()
    serializer_class = SerializeTest
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class TestUpdateView(UpdateAPIView):
    queryset = Tests.objects.all()
    serializer_class = SerializeTest
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'pk'
    def update(self, request, *args, **kwargs):
        instance = self.get_object()  # Get the instance to update
        serializer = self.get_serializer(instance, data=request.data, partial=True)  # Allow partial updates
        serializer.is_valid(raise_exception=True)  # Validate incoming data

        # Perform additional logic before saving if needed
        # e.g., check if file is uploaded and handle it

        self.perform_update(serializer)  # Save the object

        return Response(serializer.data)  # R

class TestDeleteView(DestroyAPIView):
    queryset = Tests.objects.all()
    serializer_class = SerializeTest
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # If you want to delete the file manually
        if instance.file:
            instance.file.delete(save=False)
        if instance.student_file:
            instance.student_file.delete(save=False) # Deletes the file from storage
        instance.delete()
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        # You can customize the response here, for example:
        return Response({"message": "Resource deleted successfully."}, status=200)
# Create your views here.a
