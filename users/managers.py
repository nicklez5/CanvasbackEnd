from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self,username,email,password,**extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        if not username:
            raise ValueError(_('The Username must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email,username=username,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_staffuser(self,username,email,password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',False)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        user = self.create_user(username,email,password,**extra_fields)
        user.save(using=self._db)
        return user
    def create_superuser(self,username,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        user = self.create_user(username,email,password, **extra_fields)
        user.save(using=self._db)
        return user 