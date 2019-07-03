from django import forms
from .models import BookInfo , Book , Category
from django.contrib.auth.models import User
from django.core.validators import *
class BookInfoForm(forms.ModelForm):

    class Meta:
        model = BookInfo
        fields = [ 'isbn', 'title'  , 'category' ,'author' ,'publisher' ,'publish_date']
        labels = {
            'isbn' : 'ISBN番号',
            'title' : 'タイトル',
            'category' : 'カテゴリー',
            'author' : '著者',
            'publisher' : '出版社',
            'publish_date' : '出版日',
        }
        widgets ={
            'publish_date' : forms.SelectDateWidget(years=[x for x in range(1970, 2030)]),
            'isbn' : forms.HiddenInput,
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['bookinfo' , 'arrival_date'  , 'remarks',]
        labels = {
            'bookinfo' : '資料目録',
            'arrival_date' : '入荷日',
            'remark' : '備考',
        }
        widgets ={
            'arrival_date' : forms.SelectDateWidget(years=[x for x in range(1970, 2030)]),
        }


TYPE_CHOICES = [
    ('title', '資料タイトル'),
    ('author', '著者'),
    ('isbn', 'ISBN番号'),
    ('category', '分類'),
    ('publisher', '出版社'),
]

TYPE_CHOICES2 = [
    ('id', '資料ID'),
    ('title', '資料タイトル'),
    ('author', '著者'),
    ('isbn', 'ISBN番号'),
    ('category', '分類'),
    ('publisher', '出版社'),
]
#目録検索用フォーム
class SearchForm(forms.Form):
    type = forms.ChoiceField(label='', required=True, choices=TYPE_CHOICES)
    find = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={'size' : 50, 'placeholder':'入力欄'}))

#台帳検索用フォーム
class SearchForm2(forms.Form):
    type = forms.ChoiceField(label='', required=True, choices=TYPE_CHOICES2)
    find = forms.CharField(label='', required=True, widget=forms.TextInput())

