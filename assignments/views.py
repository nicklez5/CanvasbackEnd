from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser, FormParser
from .models import Assignment
from .serializers import SerializeAssignment
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers , status 
from .forms import AssignmentForm
from rest_framework.generics import UpdateAPIView,RetrieveAPIView,DestroyAPIView, CreateAPIView, ListAPIView, RetrieveUpdateAPIView
class AssignmentListView(ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = SerializeAssignment
    permission_classes = [IsAuthenticated]
class AssignmentPostView(CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = SerializeAssignment
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
class AssignmentDetail(RetrieveAPIView):
    queryset = Assignment.objects.all()
    serializer_class = SerializeAssignment
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
class AssignmentUpdate(RetrieveUpdateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = SerializeAssignment
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'pk'
class AssignmentDelete(DestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = SerializeAssignment
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
