from django.shortcuts import render ,  redirect
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
from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check

#目録(BookInfo)一覧・検索
class BookInfoListView(ListView):
    model = BookInfo
    template_name = 'book_rental/book_rental_bookinfo_list.html'
    paginate_by = 10


    #postで受けた場合の処理
    def post(self , request, mode=None):
        #if (request.method == 'POST'):
        request.session['form_value'] = self.request.POST['find']
        request.session['type'] = self.request.POST['type']
        return self.get(request, mode)

    #formをつくる(ページネーションしても情報維持)
    def get_context_data(self):
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

    #listの獲得
    def get_queryset(self):
        if 'form_value' in self.request.session:
            find = self.request.session['form_value']
            type = self.request.session['type']

            if find is not None:
                #typeに応じた検索結果の分岐
                if type == 'isbn':
                    return BookInfo.objects.filter(Q(isbn__startswith=find)&Q(delete_date__isnull=True)).order_by('isbn')
                elif type == 'title':
                    return BookInfo.objects.filter(Q(title__icontains=find)&Q(delete_date__isnull=True)).order_by('isbn')
                elif type == 'category':
                    return BookInfo.objects.filter(Q(category__name__icontains=find)&Q(delete_date__isnull=True)).order_by('isbn')
                elif type == 'author':
                    return BookInfo.objects.filter(Q(author__icontains=find)&Q(delete_date__isnull=True)).order_by('isbn')
                elif type == 'publisher':
                    return BookInfo.objects.filter(Q(publisher__icontains=find)&Q(delete_date__isnull=True)).order_by('isbn')
            else:
                return BookInfo.objects.filter(delete_date__isnull=True).order_by('isbn')
        else:
            return BookInfo.objects.filter(delete_date__isnull=True).order_by('isbn')

    #modeによる分岐（mode=allの場合session[form_value]を破棄)
    def get(self, request, mode=None):
        self.id = request.session['id']
        #ユーザチェック
        c = usercheck(request)
        if c is not None:
            return c
        if mode == 'all':
            if 'form_value' in self.request.session:
                del self.request.session['form_value']
                del self.request.session['type']

        return super().get(self, request)
