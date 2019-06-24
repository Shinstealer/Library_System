from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import *
from .models import *
from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict

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
    if (request.method == 'POST'):
        isbn = request.POST['isbnsearch']
        book_isbn =BookInfo.objects.filter(isbn__contains=isbn)
        if book_isbn.first() is None:
            print(1)
            request.session['isbn'] = isbn
            #return render(request , 'book_manager/bookinfo_create.html' )
            return redirect(to='bookinfo_create')
        else:
            print(2)
            #return render(request , 'book_manager/book_create.html' )
            return redirect(to='book_create')
    else:
        print(3)
        return render(request , 'book_manager/isbnsearch.html')

#book info add
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
#book add
class BookCreateView(CreateView):
    template_name ='book_manager/book_create.html'
    model = Book
    form_class = BookForm
    success_url=reverse_lazy('index')


    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(
            self.request, '資料台帳の追加登録成功です!')
        return result
    def form_invalid(self, form):
        result = super().form_invalid(form) 
        messages.warning(self.request , '必須項目を記入してください！')
        return result

#book info list
class BookInfoListView(ListView):
    model = BookInfo
    template_name = 'book_manager/bookinfo_list'
    paginate_by = 5
class BookListView(ListView):
    model = Book
    template_name = 'book_manager/book_list'
    paginate_by = 5

class BookInfoDetailView(DetailView):

    model = BookInfo
class BookDetailView(DetailView):

    model= Book

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
class BookUpdateView(UpdateView):
    template_name ='book_manager/book_create.html'
    model = Book
    form_class = BookForm
    success_url=reverse_lazy('book_list')
    

    def form_valid(self , form):
        result = super().form_valid(form)
        messages.success(
            self.request, 'Update \t [{}] \t successfully!'.format(form.instance)
        )   
        return result
    