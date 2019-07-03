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

#返却のDB操作
def book_return(request, pk):
    #オペレータチェック
    c = operatorcheck(request)
    if c is not None:
        return c

    #bookの取り出し
    book = Book.objects.filter(id=pk).first()


    #貸出本が予約されているか
    #予約リストの中で一番若いのの取り出し
    wish = WishBook.objects.filter(bookinfo=book.bookinfo, book__isnull=True, is_active=True).order_by('id').first()
    if wish is not None:#予約があった場合
        wish.book = book
        wish.save()
        #確保中にする。
        s = Status.objects.get(code=2)
        book.status = s
        book.save()
    else:#予約なかった場合
        #貸出可にする。
        s = Status.objects.get(code=0)
        book.status = s
        book.save()

    #貸出台帳の返却日に今日の日付を登録
    rental = Rental.objects.get(book=book, return_date__isnull=True)
    rental.return_date = datetime.date.today()
    rental.save()

    #返却ユーザーの取り出し（htmlでのリンク用）
    user =  User.objects.get(id=rental.user.id)

    params = {'user': user}

    return render(request, 'book_rental/book_return.html', params)
