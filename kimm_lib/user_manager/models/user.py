from django.db import models
from django.core.validators import *
# Create your models here.

class User(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=150)
    tel = models.CharField(max_length=50)
    password = models.CharField(max_length=32)
    birthday = models.DateField()
    is_active = models.BooleanField(default=True)
    join_date = models.DateField()
    leave_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return str(self.id) + ':' + self.full_name + " " + self.email
