from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView

from operator_manager.forms.operator_form import Operator_Form
from operator_manager.models.operator import Operator
from operator_manager.models.operator import Position

from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check
from accounts.views.admincheck import admincheck

class OperatorCreateView(CreateView):
    template_name ='operator_manager/operator_create.html'
    model = Operator
    form_class = Operator_Form
    success_url=reverse_lazy('operator_list', kwargs={'mode':'all'})

    """
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['isbn'] = self.request.session['isbn']
        context['form'] = Operator_Form(initial={'isbn' : context['isbn']})
        print(context)
        return context
    """
    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        password_check= form.cleaned_data.get('password_check')
        if password == password_check:
            result = super().form_valid(form)
            messages.success(
                self.request, 'オペレータユーザupdate成功です')
            return result
        else:
            result = super().form_invalid(form)
            messages.warning(
                self.request,'パスワードチェックしてください！'
                )
            return result

    def get(self, request, **kwargs):
        #アドミンチェック
        c = admincheck(request)
        if c is not None:
            return c

        return super().get(self, request, **kwargs)
