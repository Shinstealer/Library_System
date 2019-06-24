from django.db import models
from django.core.validators import *
# Create your models here.

class Category(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=30)