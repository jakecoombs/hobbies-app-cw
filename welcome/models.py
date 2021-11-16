from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class PageView(models.Model):
    hostname = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)

class User(AbstractUser):
    db_table="auth_user"
