from rest_framework import serializers
from .models import Tests,TestSubmission

class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tests
        fields =  ["id", "name", "description", "date_due", "max_points", "test_file"]

class TestSubmissionSerializer(serializers.ModelSerializer):
    student_username = serializers.CharField(source="student.username", read_only=True)
    graded_by_name   = serializers.CharField(source="graded_by.username", read_only=True)
    test_max_points  = serializers.IntegerField(
        source="test.max_points", 
        read_only=True
    )
    class Meta:
        model  = TestSubmission
        fields = [
            "id",
            "test",
            "test_max_points", 
            "student_username",
            "submitted_at",
            "student_file",
            "student_points",
            "graded_at",
            "graded_by_name",
            "feedback",
        ]
        read_only_fields = [
            "id",
            "test_max_points", 
            "submitted_at",
            "student_username",
            "graded_at",
            "graded_by_name",
        ]
