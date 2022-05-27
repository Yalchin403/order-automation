from unittest.util import _MAX_LENGTH
from django.db import models


class Employee(models.Model):
    name = models.CharField(max_length=55)
    surname = models.CharField(max_length=55)
    profession = models.CharField(max_length=55)
    description = models.TextField()
    email = models.EmailField(max_length=55)
    image = models.ImageField(upload_to='employees/%Y/%m/%d')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    def __str__(self) -> str:
        return f"{self.name} {self.surname}"