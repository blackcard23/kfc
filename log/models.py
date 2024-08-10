from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class Role(models.Model):
    name = models.CharField('Name', max_length=50)
    name_code = models.CharField('Name To Coder', max_length=50)

    def __str__(self):
        return self.name


class User(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True)
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.username} - {self.role}'
