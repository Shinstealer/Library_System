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

#貸し出し
def rental(request, pk):
    #オペレータチェック
    c = operatorcheck(request)
    if c is not None:
        return c

    #選択した本の抽出
    book = Book.objects.filter(id=pk).first()

    #会員ID用のフォームの提供
    if request.method == 'GET':
        form = RentalForm()
        params = {'form': form, 'book': book}
        return render(request, 'book_rental/rental_check.html', params)


    #DBの操作
    elif request.method == 'POST':

        #ユーザーが存在するか
        id = int(request.POST['id'])
        try:
            user = User.objects.get(id=id, is_active=True)
        except:
            params = {'word':'選択された会員IDのユーザは存在しません'}
            return render(request, 'book_rental/norental.html', params)

        #貸し出しが5冊以上かどうか
        rental_list = Rental.objects.filter(user=user, return_date__isnull=True)
        if len(rental_list) >= 5:
            params = {'word':'5冊の貸出本があるため貸し出しできません。'}
            return render(request, 'book_rental/norental.html', params)

        #延滞があるか
        judge = 1
        for rent in rental_list:
            if rent.return_deadline < datetime.date.today():
                judge = 0
        if judge == 0:
            params = {'word': '延滞している本があるため貸し出しできません。'}
            return render(request, 'book_rental/norental.html', params)


        #貸出中なら(status.code==1)
        if book.status.code == 1:
            params = {'word':'選択された本は現在貸出中のため貸し出しできません。'}
            return render(request, 'book_rental/norental.html', params)
        #予約中なら(status.code==2)
        elif book.status.code == 2:
            #ユーザが予約者かどうか
            try:
                wish = WishBook.objects.get(book=book, user=user, is_active=True)
                wish.is_active = False
                #wish.book = Null
                wish.save()
            except:
                params = {'word':'選択された本は現在予約されているため貸し出しできません。'}
                return render(request, 'book_rental/norental.html', params)
        #貸出可(status.code==0)
        elif book.status.code == 0:
            pass
        #貸出中にする。
        s = Status.objects.get(code=1)
        book.status = s
        book.save()

        #旧刊か新刊かで期限設定
        passday = (datetime.date.today() - book.bookinfo.publish_date).days
        if passday < 90:#新刊
            deadline = datetime.date.today() + datetime.timedelta(days=10)
        else:#旧刊
            deadline = datetime.date.today() + datetime.timedelta(days=15)

        rental = Rental(book=book, user=user, rental_date=datetime.date.today(), return_deadline=deadline)
        rental.save()

        #完了画面(資料id,タイトル、返却期限)
        params = {'book': book, 'rental': rental, 'user':user}
        return render(request, 'book_rental/rental_complete.html', params)
