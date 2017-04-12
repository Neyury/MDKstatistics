import os
import django

# магическим образом подгружаем окружение django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from statsys.models import PostStatistics, Post
import requests
import time


wall_id = -57846937
count_post = 100
domain_api = 'https://api.vk.com/method/'
current_unixtime  = time.time()
method_wall_get = 'wall.get?owner_id={0}&count={1}&v=5.63'.format(wall_id, count_post)

list_posts = requests.get('{0}{1}'.format(domain_api, method_wall_get)).json()['response']['items']
list_statistics = list()

for obj in list_posts:
    post, created = Post.objects.get_or_create(id=obj['id'],owner_id=obj['owner_id'], date=obj['date'],
                                               post_type=obj['post_type'], marked_as_ads=obj['marked_as_ads'])

    list_statistics.append(PostStatistics(post=post, date=current_unixtime, comments=obj['comments']['count'],
                                          likes=obj['likes']['count'], reposts=obj['reposts']['count'],
                                          views=obj['views']['count']))

PostStatistics.objects.bulk_create(list_statistics)

