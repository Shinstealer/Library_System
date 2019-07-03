from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView
from book_manager.forms import *
from book_manager.models.book import Book
from book_manager.models.bookinfo import BookInfo
from book_manager.models.category import Category
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

class Index(TemplateView):

    def __init__(self):
        self.params ={
            'title' : 'book manager',
        }
    def get(self , request):
        #オペレータユーザ
        c = operatorcheck(request)
        if c is not None:
            return c

        if 'mode' in request.session:
            if self.request.session['mode'] == 'operator_mode':
                operator = Operator.objects.get(id=request.session['id'])
                name = operator.full_name
                welcome_word = {'welcome_word': 'ようこそ！オペレータ：' + name + ' 様'}
                self.params.update(welcome_word)
            if self.request.session['mode'] == 'user_mode':
                user = User.objects.get(id=request.session['id'])
                name = user.full_name
                welcome_word = {'welcome_word': 'ようこそ！ユーザ：' + name + ' 様'}
                self.params.update(welcome_word)
        return render(request , 'book_manager/index.html' , self.params)

    def post(self, request):
        pass
