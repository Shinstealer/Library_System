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

class BookUpdateView(UpdateView):
    template_name ='book_manager/book_create.html'
    model = Book
    form_class = BookForm
    success_url=reverse_lazy('book_list', kwargs={'mode': 'all'})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = Book.objects.filter(id = int(self.kwargs['pk'])).first()
        context['form'].fields['bookinfo'].widget = forms.HiddenInput()
        context['bookinfo'] = {'title' : book.bookinfo.title, 'isbn' : book.bookinfo.isbn}
        return context

    def form_valid(self , form):
        result = super().form_valid(form)
        messages.success(
            self.request, 'Update \t [{}] \t successfully!'.format(form.instance)
        )
        return result

    def get(self, request, **kwargs):
        #オペレータチェック
        c = operatorcheck(request)
        if c is not None:
            return c

        return super().get(self, request, **kwargs)
