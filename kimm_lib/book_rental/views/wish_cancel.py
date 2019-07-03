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
from reviews.models.review import Review

#予約のキャンセル
def wish_cancel(request, pk):
    #ログインチェック
    c = check(request)
    if c is not None:
        return c

    #該当する予約の抽出
    wish = WishBook.objects.get(id=pk, is_active=True)
    #該当するユーザの抽出
    user = wish.user


    #キャンセル確認画面の提供
    if request.method == 'GET':
        if request.session['mode'] == 'operator_mode':#オペレーターがログインしているとき
            params = {'wish': wish}
            return render(request, 'book_rental/wish_cancel_check.html', params)

        elif request.session['mode'] == 'user_mode':#一般ユーザがログインしているとき
            userid = request.session['id']
            params = {'wish':wish, 'userid': userid}
            return render(request, 'book_rental/user_wish_cancel_check.html', params)

    #DB処理（キャンセル処理）
    if request.method == 'POST':
        #予約のアクティブを消す
        wish.is_active=False
        wish.save()

        #資料idを取得しているかで分岐
        if wish.book is None:#Idを取得していなかった場合
            pass
        elif wish.book is not None:#idを取得していた場合
            #予約リストの中で一番若いのの取り出し
            wish2 = WishBook.objects.filter(bookinfo=wish.bookinfo, book__isnull=True, is_active=True).order_by('id').first()
            if wish2 is not None:#予約があった場合
                wish2.book = wish.book
                wish2.save()
                #（一応）確保中にする。
                s = Status.objects.get(code=2)
                wish.book.status = s
                wish.book.save()
            else:#予約なかった場合
                #貸出可にする。
                s = Status.objects.get(code=0)
                wish.book.status = s
                wish.book.save()

        if request.session['mode'] == 'operator_mode':#オペレーターがログインしているとき
            params = {'user': user}
            return render(request, 'book_rental/wish_cancel_complete.html', params)

        elif request.session['mode'] == 'user_mode':#一般ユーザがログインしているとき
            params = {'user': user}
            return render(request, 'book_rental/user_wish_cancel_complete.html', params)
