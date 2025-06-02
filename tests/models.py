from django.db import models
from django.core.files.storage import storages
from django.conf import settings 
def select_storage():
    return storages["mystorage"]
class Tests(models.Model):
    description = models.TextField(max_length=1000)
    date_due = models.DateTimeField(null=True,blank=True)
    name= models.CharField(max_length=200,unique=False)
    test_file=models.FileField(storage=select_storage,upload_to="tests/",null=True,blank=True)
    max_points= models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.name

class TestSubmission(models.Model):
    test           = models.ForeignKey(
        Tests, on_delete=models.CASCADE, related_name="submissions"
    )
    student        = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="test_submissions"
    )
    submitted_at   = models.DateTimeField(auto_now_add=True)
    student_file   = models.FileField(
        storage=select_storage,
        upload_to="tests/submissions/", null=True, blank=True
    )
    student_points = models.IntegerField(null=True, blank=True)
    graded_at      = models.DateTimeField(null=True, blank=True)
    graded_by      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="graded_test_submissions",
    )
    feedback       = models.TextField(blank=True)

    class Meta:
        unique_together = ("test", "student")
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.student.username} → {self.test.name}"


    