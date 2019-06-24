from django.db import models
from django.core.validators import *
# Create your models here.

class Category(models.Model):
    code = models.CharField(max_length=2, unique=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.code + self.name

class BookInfo(models.Model):
    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=150)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    author = models.CharField(max_length=50, null=True)
    publisher = models.CharField(max_length=50, null=True)
    publish_date = models.DateField(null=True)
    delete_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title + str(self.category) + self.author + self.publisher  

class Book(models.Model):
    bookinfo = models.ForeignKey(BookInfo, on_delete=models.PROTECT)
    arrival_date = models.DateField(null=True)
    disposal_date = models.DateField(null=True, blank=True)
    remarks = models.CharField(max_length=100, blank=True, null=True)
