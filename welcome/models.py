from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class PageView(models.Model):
    hostname = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)


class User(AbstractUser):
    db_table = "auth_user"


class Hobby(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=300)
    users = models.ManyToManyField(User, related_name="hobbies")

    def __str__(self):
        return f"{self.name}, {self.description}"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'api': reverse('hobby-api', kwargs={'hobby_id': self.id})
        }
