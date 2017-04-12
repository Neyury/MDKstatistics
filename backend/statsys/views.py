from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.contrib import auth
from django.template.context_processors import csrf
from .models import Post, PostStatistics





def login(request):
    context = dict()

    username = request.POST.get('login', '')
    password = request.POST.get('password', '')

    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return redirect('/')
    else:
        return render(request, 'statsys/login.html', context)

def logout(request):
    auth.logout(request)
    return redirect('/')


def statistics(request):
    context = dict()

    if request.user.is_authenticated():
        return render(request, 'statsys/statistics.html', context)
    else:
        return redirect('/statistics/login/')