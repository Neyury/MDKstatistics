from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .models import Post, PostStatistics

amount_given_elements = 5

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
def posts(request):
    posts = list(Post.objects.all().values())
    last_post_id = request.GET.get('post')

    if  last_post_id:
        for i, post in enumerate(posts):
            if post['id'] == int(last_post_id):
                next_post = i + 1
                return JsonResponse(posts[next_post:next_post+amount_given_elements], safe=False)

    return JsonResponse(posts[:amount_given_elements], safe=False)

# возвращает статистику по указанным постам
def statistics(request):
    list_post_ids =  request.GET.getlist('post')
    response = list()

    for post_id in list_post_ids:
        statistics = list(PostStatistics.objects.filter(post=post_id).values_list())
        values = list(zip( *list(reversed(statistics))))
        post_data = {
            'id': post_id,
            'ids': list_post_ids,
            'data': [
                [ 'дата', *values[2] ],
                [ 'лайки', *values[3] ],
                [ 'комментарии', *values[4] ],
                [ 'репосты', *values[5] ],
                [ 'просмотры', *values[6] ]
            ]
        }

        response.append( post_data )

    return JsonResponse(response, safe=False)

























