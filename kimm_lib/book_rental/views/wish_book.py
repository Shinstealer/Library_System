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




#予約
def wish_book(request, pk):

    #ログインチェック
    c = check(request)
    if c is not None:
        return c

    #選択した本情報の抽出
    bookinfo = BookInfo.objects.filter(id=pk).first()

    #会員ID用のフォームの提供
    if request.method == 'GET':
        if request.session['mode'] == 'operator_mode':#オペレーターがログインしているとき
            form = RentalForm()
            params = {'form': form, 'bookinfo': bookinfo}
            return render(request, 'book_rental/wish_check.html', params)

        elif request.session['mode'] == 'user_mode':#一般ユーザがログインしているとき
            userid = request.session['id']
            params = {'bookinfo': bookinfo, 'userid': userid}
            return render(request, 'book_rental/user_wish_check.html', params)



    if request.method == 'POST':

        #会員idの取り出し
        if request.session['mode'] == 'operator_mode':
            id = int(request.POST['id'])
        elif request.session['mode'] == 'user_mode':
            id = request.session['id']
        #ユーザーが存在するか
        try:
            user = User.objects.get(id=id, is_active=True)
        except:
            params = {'word':'選択された会員IDのユーザは存在しません'}
            if request.session['mode'] == 'operator_mode':#オペレーターがログインしているとき
                return render(request, 'book_rental/no_wish.html', params)
            elif request.session['mode'] == 'user_mode':#一般ユーザがログインしているとき
                return render(request, 'book_rental/user_no_wish.html', params)

        #台帳に存在があるか
        test_list = Book.objects.filter(bookinfo=bookinfo, disposal_date__isnull=True)
        if test_list.first() is None:#台帳にない場合
            params = {'word':'資料が存在しません'}
            if request.session['mode'] == 'operator_mode':#オペレーターがログインしているとき
                return render(request, 'book_rental/no_wish.html', params)
            elif request.session['mode'] == 'user_mode':#一般ユーザがログインしているとき
                return render(request, 'book_rental/user_no_wish.html', params)
        else:
            pass

        #ユーザーの取り出し
        user = User.objects.get(id=id, is_active=True)
        #貸出台帳の取り出し
        rental_list = Rental.objects.filter(user=user, return_date__isnull=True)
        #延滞があるか
        judge = 1
        for rent in rental_list:
            if rent.return_deadline < datetime.date.today():
                judge = 0
        if judge == 0:
            params = {'word': '延滞している本があるため予約ができません。'}
            if request.session['mode'] == 'operator_mode':#オペレーターがログインしているとき
                return render(request, 'book_rental/no_wish.html', params)
            elif request.session['mode'] == 'user_mode':#一般ユーザがログインしているとき
                return render(request, 'book_rental/user_no_wish.html', params)




        #既に予約しているかどうか
        try:
            wish = WishBook.objects.get(bookinfo=bookinfo, user=user, is_active=True)
            params = {'word':'すでに予約済みです'}
            if request.session['mode'] == 'operator_mode':#オペレーターがログインしているとき
                return render(request, 'book_rental/no_wish.html', params)
            elif request.session['mode'] == 'user_mode':#一般ユーザがログインしているとき
                return render(request, 'book_rental/user_no_wish.html', params)
        except:
            pass

        #予約本が一冊以上貸出可能かどうか
        book_list = Book.objects.filter(bookinfo=bookinfo, status__code=0 ,disposal_date__isnull=True)
        if book_list.first() is not None:#貸し出し可能な本がある場合
            book = book_list.first()#最初の貸出可のやつを確保中にする
            s = Status.objects.get(code=2)
            book.status = s
            book.save()
            wish = WishBook(user=user, book=book, bookinfo=bookinfo, reserve_date=datetime.date.today(), is_active=True)
            wish.save()
            word = '確保できましたのでいつでも貸し出し可能です'
        else:#貸し出し可能な本がない場合
            wish = WishBook(user=user, bookinfo=bookinfo, reserve_date=datetime.date.today(), is_active=True)
            wish.save()
            word = '現在貸出中または他の方が先に予約確保中ですので確保したらお知らせします。'

        params = {'word': word, 'user': user, 'bookinfo': bookinfo}

        if request.session['mode'] == 'operator_mode':#オペレーターがログインしているとき
            return render(request, 'book_rental/wish_complete.html', params)
        elif request.session['mode'] == 'user_mode':#一般ユーザがログインしているとき
            return render(request, 'book_rental/user_wish_complete.html', params)
