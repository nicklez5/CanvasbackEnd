from django.forms import ValidationError
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.parsers import FormParser, MultiPartParser
from .models import Tests
from .serializers import SerializeTest
from django.shortcuts import get_object_or_404
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
    def perform_update(self, serializer):
        # Check if a file is provided in the request
        if self.request.FILES.get('file'):
            file = self.request.FILES['file']
            # Update the serializer with the new file
            serializer.validated_data['file'] = file
        # Save the updated object
        serializer.save()
class TestDeleteView(DestroyAPIView):
    queryset = Tests.objects.all()
    serializer_class = SerializeTest
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        try:
            if instance.file:
                instance.file.delete(save=False)
            if instance.student_file:
                instance.student_file.delete(save=False)
            instance.delete()
        except Exception as e:
            raise ValidationError(f"Error deleting files or instance: {str(e)}")
# Create your views here.a
class TestSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, test_id, format=None):
        # Fetch the test by its primary key (test_id)
        test = get_object_or_404(Tests, pk=test_id)

        # Check if the user is submitting the test
        if test.submitter != request.user.username:
            return Response({"detail": "You are not authorized to submit this test."}, status=status.HTTP_403_FORBIDDEN)

        # Extract data from the request
        file = request.FILES.get("student_file")  # The file that the student submits
        student_points = request.data.get("student_points", 0)  # Optional: If the student is submitting a score

        # Handle file upload if provided
        if file:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)
            test.student_file = file_url  # Save the student file URL

        # Optionally: Save the student's score if submitted
        if student_points != 0:
            test.student_points = student_points  # Update the student's score

        # Update the submitter field to mark the test as submitted
        test.submitter = request.user.username  # Update the submitter to the current user (student)
        test.save()

        # Return the updated test as a response
        serializer = SerializeTest(test)
        return Response(serializer.data, status=status.HTTP_200_OK)