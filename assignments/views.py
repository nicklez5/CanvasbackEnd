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
from django.shortcuts import get_object_or_404

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
    def perform_update(self, serializer):
        # Perform custom update logic here (e.g., saving the file)
        if self.request.FILES.get('assignment_file'):
            # Handle file upload logic if needed
            file = self.request.FILES['assignment_file']
            serializer.validated_data['assignment_file'] = file  # Example of setting the uploaded file
        serializer.save()
class AssignmentDelete(DestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = SerializeAssignment
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        # If you want to delete the file manually
        if instance.assignment_file:
            instance.assignment_file.delete(save=False)
        if instance.student_file:
            instance.student_file.delete(save=False) # Deletes the file from storage
        instance.delete()
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        # You can customize the response here, for example:
        return Response({"message": "Resource deleted successfully."}, status=200)
class AssignmentSubmitView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk, format=None):
        # Fetch the test by its primary key (test_id)
        assignment = get_object_or_404(Assignment, pk=pk)


        # Extract data from the request
        file = request.FILES.get("student_file")  # The file that the student submits
        student_points = request.data.get("student_points", None)  # Optional: If the student is submitting a score

        # Handle file upload if provided
        if file:
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            file_url = fs.url(filename)
            assignment.student_file = file_url  # Save the student file URL

        # Optionally: Save the student's score if submitted
        if student_points is not None:
            assignment.student_points = student_points  # Update the student's score

        # Update the submitter field to mark the assignment as submitted
        assignment.submitter = request.user.username  # Update the submitter to the current user (student)
        assignment.save()

        # Return the updated assignment as a response
        serializer = SerializeAssignment(assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)