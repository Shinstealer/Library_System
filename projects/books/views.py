from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import SignupForm ,LoginForm


class Index(TemplateView):

    def __init__(self):
        self.params = {
            'title': 'MY DIARY',
        }

    def get(self, request):
        self.nickname = request.user.nickname
        self.admin=request.user.is_admin
        if self.admin is True:
            self.params={
                'title' : 'admin page',
                'nickname' :'관리자님',
            }
            return render(request, 'books/index.html', self.params)
        else:
            self.params={
                'title': 'welcome',
                'username' :self.nickname,
                }
            return render(request, 'books/index.html', self.params)

    def post(self, request):
        pass

User = get_user_model()
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # note 자동 로그인
            return redirect(to='books/index')
        else:
            return HttpResponse('password check')
    else:
        form = SignupForm()
    return render(request, 'books/signup.html', {'form': form})


def signin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(to='books/index')
        else:
            return render(request, 'books/login.html', {'form': form, 'error': 'IDとPASSWORを確認よろしゅう'})
    else:
        form = LoginForm()
        return render(request, 'books/login.html', {'form': form, 'title': 'login page'})


def signout(request):
    logout(request)
    return redirect(to='index')

