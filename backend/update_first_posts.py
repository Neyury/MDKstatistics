import os
import django

# магическим образом подгружаем окружение django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from statsys.models import PostStatistics, Post
from django.db import IntegrityError
from django.utils.timezone import datetime
import requests


def start():
    wall_id = -57846937
    count_post = 100
    API_domain = 'https://api.vk.com/method/'
    API_params = 'wall.get?owner_id={0}&count={1}&v=5.63'.format(wall_id, count_post)

    response = requests.get('{0}{1}'.format(API_domain, API_params))

    current_unixtime = time.time()
    current_datetime = datetime.fromtimestamp(current_unixtime)
    list_posts_json = response.json()['response']['items']

    list_statistics = list()

    for post_json in list_posts_json:
        try:
            post = Post.objects.create(id=post_json['id'], owner_id=post_json['owner_id'], date=post_json['date'],
                                       post_type=post_json['post_type'], marked_as_ads=post_json['marked_as_ads'])
        except IntegrityError:
            post = Post.objects.get(id=post_json['id'])

        try:
            list_statistics.append(PostStatistics(post=post, date_unixtime=current_unixtime, date_datetime=current_datetime,
                                              comments=post_json['comments']['count'], likes=post_json['likes']['count'],
                                              reposts=post_json['reposts']['count'], views=post_json['views']['count']))
        except KeyError:
                print('KeyError')

    print('count updated posts: {0}'.format(len(list_statistics)))
    PostStatistics.objects.bulk_create(list_statistics)


if __name__ == "__main__":
    import time
    interval_updates = 5

    while True:
        start()
        time.sleep(interval_updates)

