from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import FileUploadParser, MultiPartParser, JSONParser, FormParser
from .models import Assignment,AssignmentSubmission
from .serializers import AssignmentSerializer,AssignmentSubmissionSerializer
from django.http import Http404
from course.models import Course
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers , status 
from django.shortcuts import get_object_or_404

from rest_framework.generics import UpdateAPIView,RetrieveAPIView,DestroyAPIView, CreateAPIView, ListAPIView, RetrieveUpdateAPIView
class AssignmentListView(ListAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]
class AssignmentPostView(CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
class AssignmentDetail(RetrieveAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
class AssignmentUpdate(RetrieveUpdateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
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
    serializer_class = AssignmentSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'
    def perform_destroy(self, instance):
        # If you want to delete the file manually
        if instance.assignment_file:
            instance.assignment_file.delete(save=False)
        instance.delete()
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        # You can customize the response here, for example:
        return Response({"message": "Resource deleted successfully."}, status=200)
class AssignmentSubmissionCreateView(CreateAPIView):
    """
    POST /api/assignments/{assignment_id}/submit/
    """
    serializer_class   = AssignmentSubmissionSerializer
    parser_classes     = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AssignmentSubmission.objects.filter(
            assignment_id=self.kwargs["assignment_id"]
        )

    def perform_create(self, serializer):
        student = self.request.user
        assignment = get_object_or_404(Assignment, pk=self.kwargs["assignment_id"])
        # Prevent duplicate if you want only one submission per student
        if AssignmentSubmission.objects.filter(
            assignment=assignment, student=student
        ).exists():
            raise serializers.ValidationError("You already submitted this assignment.")
        serializer.save(assignment=assignment, student=student)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# 2️⃣ Staff lists all submissions for one assignment (GET)
class AssignmentSubmissionListView(ListAPIView):
    """
    GET /api/assignments/{assignment_id}/submissions/
    """
    serializer_class   = AssignmentSubmissionSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get_queryset(self):
        return AssignmentSubmission.objects.filter(
            assignment_id=self.kwargs["assignment_id"]
        )


# 3️⃣ Staff retrieve/update a single submission (GET or PATCH)
class AssignmentSubmissionDetailView(RetrieveUpdateAPIView):
    """
    GET /api/assignments/submissions/{pk}/
    PATCH /api/assignments/submissions/{pk}/
    """
    queryset           = AssignmentSubmission.objects.all()
    serializer_class   = AssignmentSubmissionSerializer

    def get_permissions(self):
        if self.request.method in ["PATCH", "PUT"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get(self, request, *args, **kwargs):
        sub = self.get_object()
        if request.user == sub.student or request.user.is_staff:
            return super().get(request, *args, **kwargs)
        return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, *args, **kwargs):
        # Only staff can patch (grade) → IsAdminUser checked above
        return super().patch(request, *args, **kwargs)


# 4️⃣ Student’s grade page (all submissions for student in course)
