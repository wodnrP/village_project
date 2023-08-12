from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
# Create your models here.
class CustomAbstractBaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(('email address'), max_length=255, unique=True)
    building_code = models.CharField(max_length=255, null=True)
    building_num = models.CharField(max_length=20, null=True)
    building_name = models.CharField(max_length=100, null=True)
    admin_check = models.BooleanField(default=False, null=True)

    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)    
    is_superuser = models.BooleanField(default=False)    
    is_staff = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email