from django.db import models
from django.core.files.storage import storages

def select_storage():
    return storages["mystorage"]
class Tests(models.Model):
    description = models.TextField(max_length=1000)
    date_due = models.DateTimeField(null=True,blank=True)
    name= models.CharField(max_length=100)
    submitter = models.CharField(max_length=100)
    file=models.FileField(storage=select_storage,null=True,blank=True)
    student_file = models.FileField(storage=select_storage, null=True, blank=True)
    max_points= models.IntegerField(null=True,blank=True)
    student_points = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering=['date_due']
        db_table = "tests"


    