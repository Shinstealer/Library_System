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

class BookInfoUpdateView(UpdateView):
    template_name ='book_manager/book_create.html'
    model = BookInfo
    form_class = BookInfoForm
    success_url=reverse_lazy('bookinfo_list')

    def form_valid(self , form):
        result = super().form_valid(form)
        messages.success(
            self.request, 'Update \t [{}] \t successfully!'.format(form.instance)
        )   
        return result