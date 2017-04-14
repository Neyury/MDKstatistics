import os
import django

# магическим образом подгружаем окружение django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from statsys.models import PostStatistics, Post
from django.db import IntegrityError
import requests
import time


wall_id = -57846937
count_post = 100
API_domain = 'https://api.vk.com/method/'
API_method_wall_get = 'wall.get?owner_id={0}&count={1}&v=5.63'.format(wall_id, count_post)

response = requests.get('{0}{1}'.format(API_domain, API_method_wall_get))
list_posts_json = response.json()['response']['items']
list_statistics = list()
current_unixtime  = time.time()

for post_json in list_posts_json:
    try:
        post = Post.objects.create(id=post_json['id'],owner_id=post_json['owner_id'], date=post_json['date'],
                                               post_type=post_json['post_type'], marked_as_ads=post_json['marked_as_ads'])
    except IntegrityError:
        post = Post.objects.get(id=post_json['id'])

    list_statistics.append(PostStatistics(post=post, date=current_unixtime, comments=post_json['comments']['count'],
                                          likes=post_json['likes']['count'], reposts=post_json['reposts']['count'],
                                          views=post_json['views']['count']))

print(len(list_statistics) or 0)
PostStatistics.objects.bulk_create(list_statistics)

