from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView

from book_rental.forms import *
from book_rental.models.rental import Rental
from book_rental.models.wishbook import WishBook

from book_manager.forms import BookInfoForm , BookForm , SearchForm ,SearchForm2
from book_manager.models.book import Book
from book_manager.models.bookinfo import BookInfo
from book_manager.models.category import Category
from django.db.models import *

from operator_manager.models.operator import Operator
from user_manager.models.user import User
from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check
from reviews.models.review import Review

class BookInfoDetailView(DetailView):
    template_name='book_rental/book_rental_bookinfo_detail.html'
    model = BookInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookinfo = BookInfo.objects.get(id=self.kwargs['pk'])
        book_list = Book.objects.filter(bookinfo=bookinfo, disposal_date__isnull=True)
        context['book_list'] = book_list
        review_list = Review.objects.filter(bookinfo=bookinfo, is_active=True)
        context['review_list'] = review_list
        return context

    def get(self, request, **kwargs):
        #ユーザチェック
        c = usercheck(request)
        if c is not None:
            return c

        return super().get(self, request, **kwargs)
