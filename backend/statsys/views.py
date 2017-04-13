from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import Post, PostStatistics

amount_given_elements = 10

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


def board(request):
    context = dict()

    if request.user.is_authenticated():
        return render(request, 'statsys/board.html', context)
    else:
        return redirect('/board/login/')


# возвращает список постов
def posts(request,):
    posts = list(Post.objects.all().values())
    last_post_id = request.GET.get('last_post_id')

    if  last_post_id:
        for i, post in enumerate(posts):
            if post['id'] == int(last_post_id):
                next_post = i + 1
                return JsonResponse(posts[next_post:next_post+amount_given_elements], safe=False)

    return JsonResponse(posts[:amount_given_elements], safe=False)

# возвращает статистику по указанным постам
def statistics(request):
    list_post_ids = [12797091, 12800935] #request.GET.getlist('post')
    # statistics  = list(PostStatistics.objects.filter(post__in=list_post_ids).values_list())
    # response = list(zip(*statistics))
    response = list()

    for post_id in list_post_ids:
        statistics = list(PostStatistics.objects.filter(post=post_id).values_list())
        values = list(zip(*statistics))
        post_data = {
            'id': post_id,
            'data': {
                'date': values[2],
                'likes': values[3],
                'comments': values[4],
                'reposts': values[5],
                'views':  values[6],
            }
        }

        response.append( post_data )

    return JsonResponse(response, safe=False)

























