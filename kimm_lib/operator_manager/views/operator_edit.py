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
from django.contrib.messages.views import SuccessMessageMixin
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check
from accounts.views.admincheck import admincheck
from django import forms

class OperatorEditView(UpdateView):
    template_name ='operator_manager/operator_create.html'
    model = Operator
    form_class = Operator_Form
    success_url=reverse_lazy('operator_list')

    # def get(self, request,  *args, **kwargs):
    #     # 結合時にsession['id']に変更
    #     if request.session['id'] == int(self.kwargs['pk']):
    #         messages.success(self.request, 'ログインユーザ自身を編集することはできません')
    #         return redirect(self.request.META['HTTP_REFERER'])
    #     else :
    #         return UpdateView.get(self, request, *args, **kwargs)
    #         # id = self.kwargs['pk']
    #         # operator = Operator.objects.get(id = id)
    #         # form = Operator_Form(instance = operator)
    #         # context = {
    #         #     'object' : operator,
    #         #     'form' : form,
    #         # }
    #         # return render(request,'operator_manager/operator_create.html',context)


    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        password_check= form.cleaned_data.get('password_check')
        if password == password_check:
            result = super().form_valid(form)
            messages.success(
                self.request, 'オペレータユーザupdate成功です')
            del self.request.session['samePerson']
            return result
        else:
            result = super().form_invalid(form)
            messages.warning(
                self.request,'パスワードチェックしてください！'
                )
            return result
        
    def get(self, request , *args , **kwargs):
        c = admincheck(request)
        if c is not None:
            return c
        if request.session['id'] == int(self.kwargs['pk']):
            request.session['samePerson'] = True
            return super().get(self, request, **kwargs)
        else:
            request.session['samePerson'] = False
            return super().get(self, request, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session['samePerson']:
            context['form'].fields['is_admin'].widget = forms.HiddenInput()
        return context
        
        
        

        
