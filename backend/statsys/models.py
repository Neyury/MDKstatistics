from django.db import models
verbose_name = "Статистика MDK"

class Post(models.Model):
    id = models.IntegerField('Идентификатор поста', primary_key=True, null=False, unique=True) # идентификатор полученый по vk api
    owner_id = models.IntegerField('Идентификатор владельца стены')
    date = models.IntegerField('Дата публикации в unixtime')
    post_type = models.CharField('Тип поста', max_length=10) # post, copy, reply, postpone, suggest
    is_pinned = models.BooleanField('Пост закреплен', default=0)
    marked_as_ads = models.BooleanField('Пост рекламный', default=0)

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['date']

class PostStatistics(models.Model):
    id = models.IntegerField('Идентификатор временной точки', primary_key=True, null=False, unique=True)
    post = models.ForeignKey(Post, verbose_name='пост')
    date = models.DateTimeField('Дата получения временной точки')
    comments = models.PositiveIntegerField('Кол-во комментариев')
    likes = models.PositiveIntegerField('Кол-во лайков')
    reposts = models.PositiveIntegerField('Кол-во репостов')
    views = models.PositiveIntegerField('Кол-во просмотров')

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = 'статистика'
        verbose_name_plural = 'статистики'
        ordering = ['date']