from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView
from book_manager.forms import *
from book_manager.models.book import Book
from book_manager.models.bookinfo import BookInfo
from book_manager.models.category import Category
from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check

def isbnSearch(request):
    c = operatorcheck(request)
    if c is not None:
        return c
    if (request.method == 'POST'):
        isbn = request.POST['isbnsearch']
        if isbn == "":
            messages.error(request, 'ISBN番号が未入力です')
            return redirect('isbnsearch')
        book_isbn =BookInfo.objects.filter(isbn=isbn)
        if book_isbn.first() is None:
            request.session['isbn'] = isbn
            #return render(request , 'book_manager/bookinfo_create.html' )
            return redirect(to='bookinfo_create')
        else:
            id = book_isbn.first().id
            #return render(request , 'book_manager/book_create.html' )
            return redirect(to='book_create', pk=id)
    else:
        return render(request , 'book_manager/isbnsearch.html')
