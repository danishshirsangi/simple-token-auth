
from multiprocessing.sharedctypes import Value
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

# Create your models here.
BLOOD_CHOICES = (
    ("DONOR","DONOR"),
    ("RECIEVER","RECIEVER"),
)

BLOOD_GROUP_CHOICES = (
    ("A+","A+"),
    ("B+","B+"),
    ("O+","O+"),
    ("A-","A-"),
    ("B-","B-"),
    ("O-","O-"),
    ("AB-","AB-"),
    ("AB+","AB+")
)

GENDER_CHOICES = (
    ("M","Male"),
    ("F","Female"),
    ("O","Others"),
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password = None, **kwargs):
        if not email:
            raise ValueError("Email Cannot be Empty")
        
        if not password:
            raise ValueError("Password Cannot be Empty")
        
        user = self.model(
            email=self.normalize_email(email),
            **kwargs
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email,  password, **kwargs):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            **kwargs
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserCustom(AbstractBaseUser):
    email = models.EmailField(
        max_length=255,
        unique=True
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    blood_group = models.CharField(max_length=255,choices=BLOOD_GROUP_CHOICES)
    gender = models.CharField(max_length=255,choices=GENDER_CHOICES)
    age = models.IntegerField(null=True,blank=True)
    mobile = models.IntegerField(null=True,blank=True)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects =  CustomUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True    
    

    @property
    def is_staff(self):
        return self.is_active


class DonorDonee(models.Model):
    user_dd = models.ForeignKey(UserCustom,on_delete=models.CASCADE)
    bg_of_user = models.CharField(max_length=255)
    user_type = models.CharField(max_length=255,choices=BLOOD_CHOICES)

    def __str__(self) -> str:
        return self.user_dd.email