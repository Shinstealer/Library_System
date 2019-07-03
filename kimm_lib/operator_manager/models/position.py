from django.db import models
from django.core.validators import *

class Position(models.Model):
    name = models.CharField(max_length=50)
    code = models.IntegerField(unique=True)

    def __str__(self):
        return self.name