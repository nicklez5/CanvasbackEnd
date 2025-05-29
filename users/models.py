from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from .managers import CustomUserManager
from profiles.models import Profile
from mycanvas.models import Canvas 
from datetime import datetime, timedelta 

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True,max_length=255,unique=True,default='')
    email = models.EmailField(_('email address'), unique=True)
    date_joined = models.DateField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateField(verbose_name='last login', auto_now=True)


    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()


    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True 
    
    @property
    def profile(self):
        return Profile.objects.get_or_create(user=self)[0]
    
    @property
    def canvas(self):
        return Canvas.objects.get_or_create(user=self)[0]


    
# Create your models here.
