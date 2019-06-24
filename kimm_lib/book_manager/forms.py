from django import forms
from .models import BookInfo , Book , Category
from django.contrib.auth.models import User
from django.core.validators import *



class BookInfoForm(forms.ModelForm):
    
    class Meta:
        model = BookInfo
        fields = [ 'title'  , 'category' ,'author' ,'publisher' ,'publish_date']
        widgets ={
            'publish_date' : forms.SelectDateWidget
        }
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['bookinfo' , 'arrival_date'  , 'remarks']
        
        widgets ={
            'arrival_date' : forms.SelectDateWidget,
        }



