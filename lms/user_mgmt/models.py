from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES=(
        ('Employee','employee'),
        ('Manager','manager'),
        ('Admin','admin')
    )
    role=models.CharField(max_length=30,choices=ROLE_CHOICES)