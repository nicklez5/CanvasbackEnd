from django.db import models
from django.conf import settings 
from django.utils.translation import gettext_lazy as _
from django import forms 
from django.core.files.storage import storages
def select_storage():
    return storages["mystorage"]
class Assignment(models.Model):
    name = models.CharField(max_length=100,unique=False)
    date_due = models.DateTimeField(null=True,blank=True)
    max_points = models.IntegerField(null=True,blank=True)
    description = models.TextField(max_length=100,blank=True)
    assignment_file = models.FileField(storage=select_storage,upload_to="assignments/",null=True,blank=True)
    def __str__(self):
        return self.name 


class AssignmentSubmission(models.Model):
    assignment     = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, related_name="submissions"
    )
    student        = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="assignment_submissions"
    )
    submitted_at   = models.DateTimeField(auto_now_add=True)
    student_file   = models.FileField(storage=select_storage,
        upload_to="assignments/submissions/", null=True, blank=True
    )
    student_points = models.IntegerField(null=True, blank=True)
    graded_at      = models.DateTimeField(null=True, blank=True)
    graded_by      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="graded_assignment_submissions",
    )
    feedback       = models.TextField(blank=True)

    class Meta:
        unique_together = ("assignment", "student")
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.student.username} → {self.assignment.name}"
