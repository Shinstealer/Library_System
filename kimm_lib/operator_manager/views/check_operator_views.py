from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView

# from operator_manager.forms. import *
from operator_manager.models.operator import Operator
from operator_manager.models.position import Position

from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check
from accounts.views.admincheck import admincheck


import datetime

class CheckOperator(DetailView):
    template_name ='operator_manager/check_operator.html'
    model = Operator

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     id = self.kwargs['pk']
    #     operator = Operator.objects.get(id = id)
    #     return context

    def get(self, request,  *args, **kwargs):
        #アドミンチェック
        c = admincheck(request)
        if c is not None:
            return c

        # 結合時にsession['id']に変更
        if request.session['id'] == int(self.kwargs['pk']):
            messages.success(self.request, 'ログインユーザ自身を削除することはできません')
            return redirect(self.request.META['HTTP_REFERER'])
        else :
            id = self.kwargs['pk']
            operator = Operator.objects.get(id = id)
            context = {
                'object' : operator,
            }
            return render(request,'operator_manager/check_operator.html',context)

    def post(self, request, *args, **kwargs):
        operator = Operator.objects.get(id = self.kwargs['pk'])
        operator.is_active = False
        operator.save()
        return redirect(to ='/operator_manager/complete_operator')
