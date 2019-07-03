from django import forms
from user_manager.models.user import User
from django.core.validators import *
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets


class PrivateUpdateForm(forms.ModelForm):
    password_check=forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['full_name','email', 'password','password_check' , 'address' , 'tel' ]
        widgets ={
            'password' : forms.PasswordInput,

        }
        labels = {
            'email' : 'メールアドレス',
            'full_name' : '氏名',
            'password' : 'パスワード',
            'password_check' : 'パスワード確認',
            'address' : '住所',
            'tel' : '電話番号',
        }
        
    def clean_FIELD(self):
        clean_data = super(PrivateUpdateForm,self).clean()
        password = clean_data.get('password')
        password_check = clean_data.get('password_check')

        if password != password_check:
            raise forms.ValidationError(
                'パスワードをもう一度確認してください！'
            )
        return password