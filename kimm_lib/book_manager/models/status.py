from django.db import models
from django.core.validators import *

class Status(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name