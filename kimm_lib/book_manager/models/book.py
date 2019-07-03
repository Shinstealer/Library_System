from django.db import models
from django.core.validators import *
from book_manager.models.bookinfo import BookInfo
from book_manager.models.status import Status
# Create your models here.

class Book(models.Model):
    bookinfo = models.ForeignKey(BookInfo, on_delete=models.PROTECT)
    arrival_date = models.DateField(null=True)
    disposal_date = models.DateField(null=True, blank=True)
    remarks = models.CharField(max_length=100, blank=True, null=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, default=Status.objects.filter(code = 0).first().id)

    def __str__(self):
        return self.bookinfo.title + " " + str(self.id)
