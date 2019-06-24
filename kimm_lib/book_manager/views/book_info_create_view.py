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

class BookInfoCreateView(CreateView):
    template_name ='book_manager/bookinfo_create.html'
    model = BookInfo
    form_class = BookInfoForm
    success_url=reverse_lazy('index')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['isbn'] = self.request.session['isbn']
        return context
    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '資料目録の追加登録成功です!')
        return result
    def form_invalid(self, form):
        result = super().form_invalid(form) 
        messages.warning(self.request , '必須項目を記入してください！')
        return result