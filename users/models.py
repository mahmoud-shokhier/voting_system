from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length = 254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    name = models.CharField(blank=True, max_length=100)
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
class Token(models.Model):
    token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    