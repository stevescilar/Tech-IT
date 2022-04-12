from enum import unique
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# custom user model
class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=50, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=50)

    # required
    date_joined     = models.DateTimeField(auto_now_add = True)
    last_login      = models.DateTimeField(auto_now_add = True)
    is_admin        = models.BooleanField(default=False)
    is_staff        = models.BooleanField(default=False)
    is_actve        = models.BooleanField(default=False)
    is_superadmin   = models.BooleanField(default=False)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']

    def __str__(self):
        return self.email

    # mandatory methods
    def has_perm(self, perm , obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


