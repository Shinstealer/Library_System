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

class Index(TemplateView):
    
    def __init__(self):
        self.params ={
            'title' : 'book manager',
        }
    def get(self , request):
         return render(request , 'book_manager/index.html' , self.params)

    def post(self, request):
        pass