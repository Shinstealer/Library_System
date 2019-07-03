from django.shortcuts import render ,  redirect
from django.http import HttpResponse , HttpRequest
from django.views.generic import TemplateView ,ListView, DetailView, CreateView, UpdateView, DeleteView

from user_manager.models.user import User
from user_manager.forms import *

from django.db.models import *
from django.contrib import messages
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from accounts.views.usercheck import usercheck
from accounts.views.operatorcheck import operatorcheck
from accounts.views.check import check

#オペレータ一覧・検索
class UserListView(ListView):
    model = User
    template_name = 'user_manager/user_list.html'
    paginate_by = 10

    #postでの処理
    def post(self , request, mode=None):
        if (request.method == 'POST'):
            request.session['form_value4'] = self.request.POST['find']
            request.session['type4'] = self.request.POST['type']
            return self.get(request, mode)

    #formをつくる(ページネーションしても情報維持)
    def get_context_data(self):
        context = super().get_context_data()
        form = SearchForm4()
        context['form'] = form
        if 'form_value4' in self.request.session:
            find = self.request.session['form_value4']
            type = self.request.session['type4']
            context['form'] = SearchForm4(initial = {'find': find, 'type': type})
            #typeに応じた文字表示の分岐
            if type == 'id':
                context['word'] =  'ID：「' + str(self.request.session['form_value4']) + '」の検索結果'
            elif type == 'name':
                context['word'] =  '名前：「' + str(self.request.session['form_value4']) + '」の検索結果'
            elif type == 'address':
                context['word'] =  '住所：「' + str(self.request.session['form_value4']) + '」の検索結果'
            elif type == 'tell':
                context['word'] =  '電話番号：「' + str(self.request.session['form_value4']) + '」の検索結果'
            elif type == 'join_date':
                context['word'] =  '加入日：「' + str(self.request.session['form_value4']) + '」の検索結果'
        else:
            context['word'] = '全件一覧'
        return context

    #listの獲得
    def get_queryset(self):
        if 'form_value4' in self.request.session:
            find = self.request.session['form_value4']
            type = self.request.session['type4']
            if find is not None:
                #typeに応じた検索結果の分岐
                if type == 'id':
                    #数字（半角・全角）であるか判断
                    if str.isnumeric(find) == False:
                        return User.objects.none().order_by('id')
                    else:
                        return User.objects.filter(Q(pk=int(find))&Q(is_active=True)).order_by('id')
                elif type == 'name':
                    return User.objects.filter(Q(full_name__icontains=find)&Q(is_active=True)).order_by('id')
                elif type == 'address':
                    return User.objects.filter(Q(address__icontains=find)&Q(is_active=True)).order_by('id')
                elif type == 'tell':
                    return User.objects.filter(Q(tel__icontains=str(find))&Q(is_active=True)).order_by('id')
            else:
                return User.objects.all().order_by('id')
        else:
            return User.objects.filter(Q(is_active=True)).order_by('id')

    #modeによる分岐（mode=allの場合session[form_value3]を破棄)
    def get(self, request, mode=None):
        #オペレータチェック
        c = operatorcheck(request)
        if c is not None:
            return c

        if mode == 'all':
            if 'form_value4' in self.request.session:
                del self.request.session['form_value4']
                del self.request.session['type4']
        return super().get(self, request)
