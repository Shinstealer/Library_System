from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView

from book_rental.models.rental import Rental
from book_rental.models.wishbook import WishBook
from user_manager.models.user import User

from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict

import datetime
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check
from reviews.models.review import Review

def overdue(request):

    #オペレータチェック
    c = operatorcheck(request)
    if c is not None:
        return c
    #延滞者を探す
    if Rental.objects.filter(return_deadline__lt = datetime.date.today(),return_date = None,user__is_active = True):
        #10日以上の人
        if Rental.objects.filter(return_deadline__lt = datetime.date.today() - datetime.timedelta(10),return_date = None,user__is_active = True):
            #30日以上の人
            if Rental.objects.filter(return_deadline__lt = datetime.date.today() - datetime.timedelta(30),return_date = None,user__is_active = True):
                #30以上
                overde_list = Rental.objects.filter(return_deadline__lt = datetime.date.today() - datetime.timedelta(30),return_date = None,user__is_active = True).order_by('id')
                overde_list1 = Rental.objects.filter(return_deadline__lt = datetime.date.today() - datetime.timedelta(10) , return_deadline__gte = datetime.date.today() - datetime.timedelta(30),return_date = None,user__is_active = True).order_by('id')
                overde_list2 = Rental.objects.filter(return_deadline__lt = datetime.date.today(), return_deadline__gte = datetime.date.today() - datetime.timedelta(10),return_date = None,user__is_active = True).order_by('id')

                context = {
                    'object_list':overde_list,
                    'object_list1':overde_list1,
                    'object_list2':overde_list2,
                }
                #予約台帳から消す
                whish = WishBook.objects.all()
                for i in overde_list:
                    for j in whish:
                        if i.user.id == j.user.id:
                            j.is_active = False
                            j.save()
                        else:
                            continue
                return render(request,'book_rental/overdue.html',context)

            #10日以上の人表示
            overde_list1 = Rental.objects.filter(return_deadline__lt = datetime.date.today() - datetime.timedelta(10),return_date = None,user__is_active = True).order_by('id')
            overde_list2 = Rental.objects.filter(return_deadline__lt = datetime.date.today(), return_deadline__gte = datetime.date.today() - datetime.timedelta(10),return_date = None,user__is_active = True).order_by('id')

            context = {
                'object_list1':overde_list1,
                'object_list2':overde_list2,
            }
            return render(request,'book_rental/overdue.html',context)

        #数日過ぎた人
        overde_list2 = Rental.objects.filter(return_deadline__lt = datetime.date.today(),return_date = None,user__is_active = True)
        context = {
            'object_list2':overde_list2,
        }
        return render(request,'book_rental/overdue.html',context)
    #延滞者なし
    else :
        sugita = '延滞者なし'
        context = {
            'sugita':sugita
        }
        return render(request,'book_rental/overdue.html',context)
