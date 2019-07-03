from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView
from reviews.forms import *
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

def book_review(request, pk):

    #一般ユーザーチェック
    c = usercheck(request)
    if c is not None:
        return c

    #該当するbookinfoの取り出し
    bookinfo = BookInfo.objects.get(id=pk, delete_date__isnull=True)
    #該当するユーザの取り出し
    id = request.session['id']
    user = User.objects.get(id=id)

    #フォームの提供
    if request.method == 'GET':
        #既にレビューしているかの判断
        try:
            test = Review.objects.get(user=user, bookinfo=bookinfo, is_active=True)
            return render(request, 'reviews/review_error.html')
        except:
            pass

        form = ReviewForm(initial = {'grade': 3})
        params = {'form': form, 'bookinfo': bookinfo}
        return render(request, 'reviews/reviews.html', params)

    if request.method == 'POST':
        grade = request.POST['grade']
        comment = request.POST['comment']

        r = Review(user=user, bookinfo=bookinfo, grade=grade, comment=comment, is_active=True)
        r.save()
        params = {'bookinfo': bookinfo, 'review': r}
        return render(request, 'reviews/review_complete.html', params)
