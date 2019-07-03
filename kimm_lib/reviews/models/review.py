from django.db import models
from django.core.validators import *
from user_manager.models.user import User
from book_manager.models.bookinfo import BookInfo
from django.utils import timezone

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    bookinfo = models.ForeignKey(BookInfo, on_delete=models.PROTECT, blank=True, null=True)
    grade = models.IntegerField()
    comment = models.TextField(max_length=200)
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.full_name + "のレビュー"
