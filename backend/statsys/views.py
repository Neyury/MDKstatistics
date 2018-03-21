from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import JsonResponse
from django.utils.timezone import datetime
from .models import Post, PostStatistics


amount_given_elements = 5


# функция, возвращающая ограниченное количество точек для отображения на графике
def get_short_list_statistics(queryset, post_id, amount_dots=20):
    dot_list = list()
    qs_values = list(queryset.values())

    if queryset:
        for i in range(0, len(qs_values), max(len(qs_values) // amount_dots, 1)):
            dot_list.append(qs_values[i])

    post_data = {
        'id': post_id,
        'data': sorted(dot_list, key=lambda x: x['date_unixtime'], reverse=True),
    }

    return post_data


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

    if request.user.is_authenticated:
        return render(request, 'statsys/board.html', context)
    else:
        return redirect('/board/login/')


# возвращает или подгружает список постов
def posts(request):
    posts_list = list(Post.objects.all().values())

    last_post_id = request.GET.get('post')

    if last_post_id:
        for i, post in enumerate(posts_list):
            if post['id'] == int(last_post_id):
                next_post = i + 1
                return JsonResponse(posts_list[next_post:next_post+amount_given_elements], safe=False)

    return JsonResponse(posts_list[:amount_given_elements], safe=False)


# возвращает статистику по указанным постам за определенные период (range)
def statistics(request):
    list_post_ids = request.GET.getlist('post')
    response = list()

    if request.GET.get('range') == 'all':
        for post_id in list_post_ids:
            queryset = PostStatistics.objects.filter(post=post_id)
            response.append(get_short_list_statistics(queryset, post_id))

    elif request.GET.get('range') == 'month':
        for post_id in list_post_ids:
            queryset = PostStatistics.objects.filter(post=post_id, date_datetime__day__gte=datetime.now().day-31)
            response.append(get_short_list_statistics(queryset, post_id, 30))

    elif request.GET.get('range') == 'week':
        for post_id in list_post_ids:
            queryset = PostStatistics.objects.filter(post=post_id, date_datetime__day__gte=datetime.now().day-7)
            response.append(get_short_list_statistics(queryset, post_id, 21))

    elif request.GET.get('range') == 'day':
        for post_id in list_post_ids:
            queryset = PostStatistics.objects.filter(post=post_id, date_datetime__gte=datetime.now().date())
            response.append(get_short_list_statistics(queryset, post_id, 24))

    else:
        for post_id in list_post_ids:
            statistics_list = list(PostStatistics.objects.filter(post=post_id)[:20].values())
            post_data = {
                'id': post_id,
                'data': statistics_list,
            }

            response.append(post_data)

    return JsonResponse(response, safe=False)
