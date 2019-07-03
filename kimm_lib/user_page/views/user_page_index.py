from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView 
from django.contrib.auth.mixins import UserPassesTestMixin
from user_page.forms.private_update_form import PrivateUpdateForm
from user_manager.models.user import User
from operator_manager.models.operator import Operator
from book_rental.models.rental import Rental
from book_manager.forms import BookInfoForm , BookForm , SearchForm ,SearchForm2


from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict


import datetime

class UserPageIndex(TemplateView):
    template_name ='user_page/user_page_index.html'
    
    
    def __init__(self, *args, **kwargs):
        super(UserPageIndex, self).__init__(*args, **kwargs)
    
    def get(self, request):
        self.id = self.request.session['id']
        return super().get(self, request)
    
    #postで受けた場合の処理
    def post(self , request):
        request.session['form_value'] = self.request.POST['find']
        request.session['type'] = self.request.POST['type']
        return self.get(request)

    #formをつくる(ページネーションしても情報維持)
    def get_context_data(self,**kwarges):
        context = super().get_context_data()
        form = SearchForm()
        context['form'] = form
        context['pk'] = int(self.id)

        if 'form_value' in self.request.session:
            find = self.request.session['form_value']
            type = self.request.session['type']
            context['form'] = SearchForm(initial = {'find': find, 'type': type})
            #typeに応じた文字表示の分岐
            if type == 'isbn':
                context['word'] =  'ISBN番号：「' + str(self.request.session['form_value']) + '」の検索結果'
            elif type == 'title':
                context['word'] =  '資料タイトル：「' + str(self.request.session['form_value']) + '」の検索結果'
            elif type == 'category':
                context['word'] =  '分類：「' + str(self.request.session['form_value']) + '」の検索結果'
            elif type == 'author':
                context['word'] =  '著者：「' + str(self.request.session['form_value']) + '」の検索結果'
            elif type == 'publisher':
                context['word'] =  '出版社：「' + str(self.request.session['form_value']) + '」の検索結果'
        else:
            context['word'] = '全件一覧'

        return context

    
