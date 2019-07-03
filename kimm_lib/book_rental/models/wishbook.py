from django.db import models
from django.core.validators import *
from user_manager.models.user import User
from book_manager.models.book import Book
from book_manager.models.bookinfo import BookInfo

class WishBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    book = models.ForeignKey(Book, on_delete=models.PROTECT, null=True, blank=True)
    bookinfo = models.ForeignKey(BookInfo, on_delete=models.PROTECT)
    reserve_date = models.DateField()
    is_active = models.BooleanField(default=True)
    remarks = models.CharField(max_length=200,blank=True, null=True)

    def __str__(self):
        return str(self.id) +self.user.full_name + "の予約"
