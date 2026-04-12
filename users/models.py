from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
