from django.forms import ValidationError
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.parsers import FormParser, MultiPartParser
from course.models import Course
from .models import Tests,TestSubmission
from .serializers import TestSerializer,TestSubmissionSerializer
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status

from rest_framework.generics import UpdateAPIView,RetrieveAPIView,DestroyAPIView, CreateAPIView, ListAPIView,RetrieveUpdateAPIView

class TestListView(ListAPIView):
    queryset = Tests.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]

    
class TestPostView(CreateAPIView):
    queryset = Tests.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
    

class TestDetailView(RetrieveAPIView):
    queryset = Tests.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

class TestUpdateView(UpdateAPIView):
    queryset = Tests.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    lookup_field = 'pk'
    def perform_update(self, serializer):
        # Check if a file is provided in the request
        if self.request.FILES.get('test_file'):
            file = self.request.FILES['test_file']
            # Update the serializer with the new file
            serializer.validated_data['test_file'] = file
        # Save the updated object
        serializer.save()
class TestDeleteView(DestroyAPIView):
    queryset = Tests.objects.all()
    serializer_class = TestSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        try:
            if instance.test_file:
                instance.test_file.delete(save=False)
            instance.delete()
        except Exception as e:
            raise ValidationError(f"Error deleting files or instance: {str(e)}")
class TestSubmissionCreateView(CreateAPIView):
    """
    POST /api/tests/{test_id}/submit/
    """
    serializer_class   = TestSubmissionSerializer
    parser_classes     = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TestSubmission.objects.filter(test_id=self.kwargs["test_id"])

    def perform_create(self, serializer):
        student = self.request.user
        test = get_object_or_404(Tests, pk=self.kwargs["test_id"])
        if TestSubmission.objects.filter(test=test, student=student).exists():
            raise serializers.ValidationError("You already submitted this test.")
        serializer.save(test=test, student=student)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


# 2️⃣ Staff lists all submissions for one test (GET)
class TestSubmissionListView(ListAPIView):
    """
    GET /api/tests/{test_id}/submissions/
    """
    serializer_class   = TestSubmissionSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]

    def get_queryset(self):
        return TestSubmission.objects.filter(test_id=self.kwargs["test_id"])


# 3️⃣ Staff retrieve/update a single test submission (GET or PATCH)
class TestSubmissionDetailView(RetrieveUpdateAPIView):
    """
    GET /api/tests/submissions/{pk}/
    PATCH /api/tests/submissions/{pk}/
    """
    queryset           = TestSubmission.objects.all()
    serializer_class   = TestSubmissionSerializer

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
        return super().patch(request, *args, **kwargs)


