from django.db import models
from django.core.validators import *
from user_manager.models.user import User
from book_manager.models.book import Book

class Rental(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT)
    rental_date = models.DateField()
    return_deadline = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    remarks = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return self.user.full_name + " " + str(self.rental_date)
