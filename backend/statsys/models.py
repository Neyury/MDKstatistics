from django.db import models
verbose_name = "Статистика MDK"

class Post(models.Model):
    id = models.IntegerField('Идентификатор поста', primary_key=True, null=False, unique=True) # идентификатор полученый по vk api
    owner_id = models.IntegerField('Идентификатор владельца стены')
    date = models.IntegerField('Дата публикации в unixtime')
    post_type = models.CharField('Тип поста', max_length=10)
    marked_as_ads = models.BooleanField('Пост рекламный', default=0)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['-date']

class PostStatistics(models.Model):
    post = models.ForeignKey(Post, verbose_name='пост', on_delete=models.CASCADE)
    date_unixtime = models.IntegerField('время в unixtime')
    date_datetime = models.DateTimeField('стандартное время')
    likes = models.PositiveIntegerField('Кол-во лайков')
    comments = models.PositiveIntegerField('Кол-во комментариев')
    reposts = models.PositiveIntegerField('Кол-во репостов')
    views = models.PositiveIntegerField('Кол-во просмотров')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'статистика'
        verbose_name_plural = 'статистики'
        ordering = ['-date_unixtime']