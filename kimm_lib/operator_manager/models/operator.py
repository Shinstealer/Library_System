from django.db import models
from django.core.validators import *
from operator_manager.models.position import Position
# Create your models here.

class Operator(models.Model):
    email = models.EmailField(max_length=100, unique=True)
    full_name = models.CharField(max_length=50)
    password = models.CharField(max_length=32)
    birthday = models.DateField()
    position = models.ForeignKey(Position, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name + " " + self.email