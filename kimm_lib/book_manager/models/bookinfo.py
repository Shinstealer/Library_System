from django.db import models
from django.core.validators import *
from book_manager.models.category import Category
# Create your models here.

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