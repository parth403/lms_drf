from django.db import models
from django.contrib.auth.models import AbstractUser
from lms.common.constants import ROLE_CHOICES,ROLE_EMPLOYEE
# Create your models here.

class User(AbstractUser):
    role=models.CharField(max_length=30,choices=ROLE_CHOICES,default=ROLE_EMPLOYEE)
    manager=models.ForeignKey('self',null=True,blank=True,on_delete=models.SET_NULL,related_name='subordinates')