from django.db import models
from django.conf import settings
 

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    first_name = models.CharField(max_length=200,null=True,blank=True)
    last_name = models.CharField(max_length=200,null=True,blank=True)
    date_of_birth = models.DateField(blank=True,null=True)
    #phone = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return str(self.user)


#post_save.connect(update_profile, sender=settings.AUTH_USER_MODEL)