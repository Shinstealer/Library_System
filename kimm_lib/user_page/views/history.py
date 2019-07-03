from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView
from user_page.forms import *
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
import math

def history(request, no):

    #一般ユーザーチェック
    c = usercheck(request)
    if c is not None:
        return c

    #ユーザーidの取り出し
    id = request.session['id']
    #ユーザの取り出し
    user = User.objects.get(id=id, is_active=True)

    #貸し出し履歴の取り出し
    rental_history = Rental.objects.filter(user=user).order_by('-rental_date')
    #予約リストの取り出し
    wish_history = WishBook.objects.filter(user=user, is_active=True)

    #pagenation
    kazu = len(rental_history)
    page_kazu = math.ceil(kazu/5)

    plist = {i for i in range(1, page_kazu+1)}

    data = Paginator(rental_history, 5)
    rental_history = data.get_page(no)

    params = {'rental_history': rental_history,
                'wish_history': wish_history,
                'now_no': no,
                'plist': plist,
                'user': user
                }
    return render(request, 'user_page/history.html', params)
