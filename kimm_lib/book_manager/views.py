from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import *
from .models import BookInfo , Book , Category
from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict


import datetime


class Index(TemplateView):

    def __init__(self):
        self.params ={
            'title' : 'book manager',
        }
    def get(self , request):
         return render(request , 'book_manager/index.html' , self.params)

    def post(self, request):
        pass

def isbnSearch(request):
    pass


#book info add
class BookInfoCreateView(CreateView):
    template_name ='book_manager/bookinfo_create.html'
    model = BookInfo
    form_class = BookInfoForm
    success_url=reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '[{}] \t の追加成功です!'.format(form.instance))
        return result
    def form_invalid(self, form):
        result = super().form_invalid(form)
        messages.warning(self.request , '必須項目を記入してください！')
        return result
#book add
class BookCreateView(CreateView):
    template_name ='book_manager/book_create.html'
    model = Book
    form_class = BookForm
    success_url=reverse_lazy('index')

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '[{}] \t の追加成功です!'.format(form.instance))
        return result
    def form_invalid(self, form):
        result = super().form_invalid(form)
        messages.warning(self.request , '必須項目を記入してください！')
        return result





#台帳削除
class CheckBookView(DetailView):
    template_name ='book_manager/check_book.html'
    model = Book
    #flag = False

    # def get_template_names(self):
    #     if flag :
    #         template_name = 'book_manager/index.html'
    #     else :
    #         template_name ='book_manager/check_book.html'
    #     return [template_name]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']

        # if Book.objects.get(id = id) is None:
        #     flag = True
        #     #return context
        #     return HttpResponse('ないです！')
        #
        # else:
        book = Book.objects.get(id = id)
        bookinfo = BookInfo.objects.get(id = book.bookinfo_id)
        context['title'] = bookinfo.title
        context['id'] = book.id
        print('CCC')
        return context

    # template_name ='book_manager/check_bookinfo.html'
    def post(self, request, *args, **kwargs):
        #資料台帳に削除年月日を記入
        book = Book.objects.get(id = self.kwargs['pk'])
        ddate = request.POST['ddate']
        book.disposal_date = ddate
        book.save()
        return redirect(to ='/book_manager/complete_book')

class CompleteBookView(TemplateView):
    template_name ='book_manager/complete_book.html'




#目録の削除
class CheckBookInfoView(DetailView):
    template_name ='book_manager/check_bookinfo.html'
    model = BookInfo
    def post(self, request, *args, **kwargs):
        print('uwaaaaaaaaaa')
        bookinfo = BookInfo.objects.get(id = self.kwargs['pk'])
        records = Book.objects.all()
        for i in range(1,records.count()+1):
            if Book.objects.filter(id = i).first() is None:
                continue
            else:
                book = Book.objects.get(id = i)
                if bookinfo.id == book.bookinfo_id:
                    return redirect(to = '/book_manager/error_bookinfo')
                else:
                    #資料目録に削除年月日を記入
                    bookinfo.delete_date = datetime.date.today()
                    bookinfo.save()
                    return redirect(to ='/book_manager/complete_bookinfo')
        print('uwaaaaaaaaaa')
        # book = Book.objects.get(bookinfo_id = bookinfo)
        # #もし台帳に情報があるなら
        # if book.disposal_date is not  None:
        #     return redirect(to = '/book_manager/erro_bookinfo')
        # else:
        #     #資料目録に削除年月日を記入
        #     bookinfo.delete_date = datetime.date.today()
        #     book.save()
        #     return redirect(to ='/book_manager/complete_bookinfo')



class ErrorBookInfoView(TemplateView):
    model = BookInfo
    template_name ='book_manager/error_bookinfo.html'


class CompleteBookInfoView(TemplateView):
    model = BookInfo
    template_name ='book_manager/complete_bookinfo.html'
