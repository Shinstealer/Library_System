from django import forms
from user_manager.models.user import User
from django.core.validators import *
from django.contrib.admin.widgets import AdminDateWidget
from django.contrib.admin import widgets


class User_Form(forms.ModelForm):
    password_check=forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ['email', 'full_name','password','password_check' , 'address' , 'tel'  ,'birthday'  ,'is_active' , 'join_date' , 'leave_date']
        widgets ={
            'password' : forms.PasswordInput,
            'birthday': forms.SelectDateWidget(years=[x for x in range(1970, 2030)]),
            'join_date': forms.SelectDateWidget(years=[x for x in range(2000, 2030)]),
            'leave_date': forms.SelectDateWidget(years=[x for x in range(2000, 2030)]),
        }

        labels = {
            'email' : 'メールアドレス',
            'full_name' : '氏名',
            'password' : 'パスワード',
            'password_check' : 'パスワード確認',
            'address' : '住所',
            'tel' : '電話番号',
            'birthday' : '生年月日',
            'join_date' : '入会年月日',
            'leave_date' : '退会年月日',
        }
        
    def clean_FIELD(self):
        clean_data = super(User_Form,self).clean()
        password = clean_data.get('password')
        password_check = clean_data.get('password_check')

        if password != password_check:
            raise forms.ValidationError(
                'パスワードをもう一度確認してください！'
            )
        return password