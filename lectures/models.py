from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files.storage import storages
def select_storage():
    return storages["mystorage"]
class Lecture(models.Model):
    description = models.TextField(blank=True)
    name = models.CharField(max_length=100,unique=True)
    file = models.FileField(storage=select_storage,null=True)
    

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = "lecture"
# Create your models here.