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
from django import forms

class BookCreateView(CreateView):
    template_name ='book_manager/book_create.html'
    model = Book
    form_class = BookForm
    success_url=reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        bookinfo = BookInfo.objects.filter(id = int(context['pk'])).first()
        if bookinfo is not None:
            context['form'] = BookForm(initial={'bookinfo' : bookinfo.id})
            context['form'].fields['bookinfo'].widget = forms.HiddenInput()
        else:
            pass
        context['bookinfo'] = {'title' : bookinfo.title, 'isbn' : bookinfo.isbn}
        return context
    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '資料登録完了です!')
        return result
    def form_invalid(self, form):
        result = super().form_invalid(form)
        messages.warning(self.request , '必須項目を記入してください！')
        return result

    def get(self, request, **kwargs):
        #オペレータチェック
        c = operatorcheck(request)
        if c is not None:
            return c

        return super().get(self, request, **kwargs)
