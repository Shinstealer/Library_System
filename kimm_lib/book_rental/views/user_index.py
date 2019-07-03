from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView


from book_rental.forms import *
from book_rental.models.rental import Rental
from book_rental.models.wishbook import WishBook

from book_manager.forms import BookInfoForm , BookForm , SearchForm ,SearchForm2
from book_manager.models.book import Book
from book_manager.models.bookinfo import BookInfo
from book_manager.models.category import Category
from django.db.models import *

from operator_manager.models.operator import Operator
from user_manager.models.user import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check

class UserIndex(TemplateView):

    template_name = 'book_rental/user_index.html'

    def get(self , request):
        self.id = self.request.session['id']
        return super().get(self,request)

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
        #ユーザネームの表示
        user = User.objects.get(id=self.request.session['id'])
        name = user.full_name
        welcome_word = 'ようこそ！' + name + ' 様'
        context['welcome_word'] = welcome_word
        return context

    def get(self, request, **kwargs):
        self.id = request.session['id']
        #ユーザチェック
        c = usercheck(request)
        if c is not None:
            return c

        return super().get(self, request, **kwargs)
