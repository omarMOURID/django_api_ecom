from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField("email address", unique=True)
    adresse = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=6)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
    profile_photo = models.ImageField(verbose_name="Photo de profile")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
