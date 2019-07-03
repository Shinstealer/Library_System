from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView
from book_rental.forms import *
from book_manager.models.book import Book
from book_manager.models.bookinfo import BookInfo
from book_rental.models.rental import Rental
from book_rental.models.wishbook import WishBook
from operator_manager.models.operator import Operator
from user_manager.models.user import User
from book_manager.models.status import Status
from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check
import datetime

#返却確認画面用
def return_check(request, pk):
    #オペレータチェック
    c = operatorcheck(request)
    if c is not None:
        return c
    #bookの取り出し
    book = Book.objects.filter(id=pk).first()
    params = {'book': book}
    return render(request, 'book_rental/return_check.html', params)
