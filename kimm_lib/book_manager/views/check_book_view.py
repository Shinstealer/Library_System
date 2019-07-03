from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView
from book_manager.forms import *
from book_manager.models.book import Book
from book_manager.models.bookinfo import BookInfo
from book_manager.models.category import Category
from book_manager.models.status import Status
from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check
from book_rental.models.wishbook import WishBook
from book_rental.models.rental import Rental

import datetime


class CheckBookView(DetailView):
    template_name ='book_manager/check_book.html'
    model = Book
    #flag = False

    # def get_template_names(self):
    #     if flag :
    #         template_name = 'book_manager/index.html'
    #     else :
    #         template_name ='book_manager/check_book.html'
    #     return [template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']

        # if Book.objects.get(id = id) is None:
        #     flag = True
        #     #return context
        #     return HttpResponse('ないです！')
        #
        # else:
        book = Book.objects.get(id = id)
        bookinfo = BookInfo.objects.get(id = book.bookinfo_id)
        context['title'] = bookinfo.title
        # context['id'] = book.id
        return context

    # template_name ='book_manager/check_bookinfo.html'
    def post(self, request, *args, **kwargs):
        #資料台帳に削除年月日を記入
        book = Book.objects.get(id = self.kwargs['pk'])
        if book.status.code == 1:
            rental = Rental.objects.filter(book = book).first()
            rental.return_date = datetime.date.today()
            rental.save()
        if book.status.code == 2:
            wish = WishBook.objects.filter(book = book).first()
            isAnnihilation = Book.objects.filter(bookinfo__id = book.bookinfo.id, disposal_date = None).exclude(id = self.kwargs['pk'])
            if isAnnihilation.first() is not None:
                canwish = Book.objects.filter(bookinfo__id = book.bookinfo.id ,status__code = 0, disposal_date = None).exclude(id = self.kwargs['pk']).first()
                if canwish is not None:
                    canwish.status = Status.objects.filter(code = 2).first()
                    canwish.save()
                    wish.book = canwish
                else :
                    wish.book = None
                wish.save()
            else :
                wish.is_active = False
            wish.save()
        ddate = request.POST['ddate']
        book.disposal_date = ddate
        book.save()
        return redirect(to ='/book_manager/complete_book')

    def get(self, request, **kwargs):
        #オペレータチェック
        c = operatorcheck(request)
        if c is not None:
            return c

        return super().get(self, request, **kwargs)
