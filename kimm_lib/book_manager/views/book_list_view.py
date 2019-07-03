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


#台帳(Book)一覧・検索
class BookListView(ListView):
    model = Book
    template_name = 'book_manager/book_list.html'
    paginate_by = 10

    #postでの処理
    def post(self , request, mode=None):
        if (request.method == 'POST'):
            request.session['form_value2'] = self.request.POST['find']
            request.session['type2'] = self.request.POST['type']
            return self.get(request, mode)

    #formをつくる(ページネーションしても情報維持)
    def get_context_data(self):
        context = super().get_context_data()
        form = SearchForm2()
        context['form'] = form
        if 'form_value2' in self.request.session:
            find = self.request.session['form_value2']
            type = self.request.session['type2']
            context['form'] = SearchForm2(initial = {'find': find, 'type': type})
            #typeに応じた文字表示の分岐
            if type == 'id':
                context['word'] =  '資料id：「' + str(self.request.session['form_value2']) + '」の検索結果'
            elif type == 'isbn':
                context['word'] =  'ISBN番号：「' + str(self.request.session['form_value2']) + '」の検索結果'
            elif type == 'title':
                context['word'] =  '資料タイトル：「' + str(self.request.session['form_value2']) + '」の検索結果'
            elif type == 'category':
                context['word'] =  '分類：「' + str(self.request.session['form_value2']) + '」の検索結果'
            elif type == 'author':
                context['word'] =  '著者：「' + str(self.request.session['form_value2']) + '」の検索結果'
            elif type == 'publisher':
                context['word'] =  '出版社：「' + str(self.request.session['form_value2']) + '」の検索結果'
        else:
            context['word'] = '全件一覧'
        return context

    #listの獲得
    def get_queryset(self):
        if 'form_value2' in self.request.session:
            find = self.request.session['form_value2']
            type = self.request.session['type2']

            if find is not None:
                #typeに応じた検索結果の分岐
                if type == 'id':
                    if str.isnumeric(find) == False:
                        return User.objects.none().order_by('id')
                    else:
                        return Book.objects.filter(Q(pk=int(find))&Q(disposal_date__isnull=True)&Q(disposal_date__isnull=True)).order_by('id')
                elif type == 'isbn':
                    return Book.objects.filter(Q(bookinfo__isbn__startswith=find)&Q(bookinfo__delete_date__isnull=True)&Q(disposal_date__isnull=True)).order_by('id')
                elif type == 'title':
                    return Book.objects.filter(Q(bookinfo__title__icontains=find)&Q(bookinfo__delete_date__isnull=True)&Q(disposal_date__isnull=True)).order_by('id')
                elif type == 'category':
                    return Book.objects.filter(Q(bookinfo__category__name__icontains=find)&Q(bookinfo__delete_date__isnull=True)&Q(disposal_date__isnull=True)).order_by('id')
                elif type == 'author':
                    return Book.objects.filter(Q(bookinfo__author__icontains=find)&Q(bookinfo__delete_date__isnull=True)&Q(disposal_date__isnull=True)).order_by('id')
                elif type == 'publisher':
                    return Book.objects.filter(Q(bookinfo__publisher__icontains=find)&Q(bookinfo__delete_date__isnull=True)&Q(disposal_date__isnull=True)).order_by('id')
            else:
                return Book.objects.all().order_by('id')
        else:
            return Book.objects.filter(bookinfo__delete_date__isnull=True, disposal_date__isnull=True).order_by('id')

    #modeによる分岐（mode=allの場合session[form_value2]を破棄)
    def get(self, request, mode=None):
        #オペレータチェック
        c = operatorcheck(request)
        if c is not None:
            return c
        if mode == 'all':
            if 'form_value2' in self.request.session:
                del self.request.session['form_value2']
                del self.request.session['type2']

        return super().get(self, request)
