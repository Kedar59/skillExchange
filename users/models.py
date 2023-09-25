from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    userBio=models.CharField(max_length=255,blank=False)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    