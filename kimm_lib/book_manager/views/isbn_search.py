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

def isbnSearch(request):
    if (request.method == 'POST'):
        isbn = request.POST['isbnsearch']
        book_isbn =BookInfo.objects.filter(isbn__contains=isbn)
        if book_isbn.first() is None:
            print(1)
            request.session['isbn'] = isbn
            #return render(request , 'book_manager/bookinfo_create.html' )
            return redirect(to='bookinfo_create')
        else:
            print(2)
            #return render(request , 'book_manager/book_create.html' )
            return redirect(to='book_create')
    else:
        print(3)
        return render(request , 'book_manager/isbnsearch.html')