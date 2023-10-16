from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    email=models.EmailField(unique=True)
    userBio=models.CharField(max_length=255,blank=False)
    prof_path=models.CharField(max_length=1024,null=True,blank=True)
    has_prof_pic=models.BooleanField(default=False)
    prof_extension=models.CharField(max_length=15,null=True,blank=True)
    skills = models.ManyToManyField(Skill, blank=True)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']

User = get_user_model()
class Credential(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    links = models.JSONField(default=list)  # A list of JSON objects

    def __str__(self):
        return f"{self.user.username}'s {self.skill.name} Credential"