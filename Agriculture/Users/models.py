
import base64

from django.db import models

from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin


def image_data_url(image_data, content_type):
    if not image_data:
        return ''

    encoded_image = base64.b64encode(bytes(image_data)).decode('ascii')
    return f"data:{content_type or 'image/jpeg'};base64,{encoded_image}"


class Designation(models.Model):
    DESIGNATION_CHOICES = [
        ("Admin", "Admin"),
        ("VC", "VC"),
        ("Supervisor", "Supervisor"),
        ("People", "People"),
    ]
    name = models.CharField(max_length=50,choices=DESIGNATION_CHOICES,unique=True)
    def __str__(self):
        return self.name

class customusermanager(BaseUserManager):

    def create_user(self,username,firstname,personal_phone_number,password=None,**extra_fields):
        if not username:
            raise ValueError("Username is mandatory")
        user = self.model(username=username,firstname=firstname,personal_phone_number=personal_phone_number,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, firstname, personal_phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(username,firstname,personal_phone_number,password,**extra_fields)

class Details(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=200, null=False,blank=False, unique=True)

    firstname = models.CharField(max_length=100, null=True, blank=True)
    lastname = models.CharField(max_length=100, null=True, blank=True)
    nickname = models.CharField(max_length=100, null=True, blank=True)

    email = models.EmailField(max_length=50, unique=True, null=True,blank=True)

    personal_phone_number = models.CharField(max_length=10, null=True, blank=True)
    home_phone_number = models.CharField(max_length=15, null=True, blank=True)

    bike = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)


    password = models.CharField(max_length=300, null=True)
    designation = models.ForeignKey(Designation,on_delete=models.SET_NULL,null=True,blank=True,related_name="users")

    profilepic = models.BinaryField(null=True, blank=True)
    profilepic_content_type = models.CharField(max_length=100, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["firstname", "personal_phone_number"]

    last_login = None

    objects = customusermanager()

    @property
    def profilepic_data_url(self):
        return image_data_url(self.profilepic, self.profilepic_content_type)
    
