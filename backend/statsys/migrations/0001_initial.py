# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-11 18:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Идентификатор поста')),
                ('owner_id', models.IntegerField(verbose_name='Идентификатор владельца стены')),
                ('date', models.IntegerField(verbose_name='Дата публикации в unixtime')),
                ('post_type', models.CharField(max_length=10, verbose_name='Тип поста')),
                ('is_pinned', models.BooleanField(default=0, verbose_name='Пост закреплен')),
                ('marked_as_ads', models.BooleanField(default=0, verbose_name='Пост рекламный')),
            ],
            options={
                'verbose_name': 'пост',
                'ordering': ['date'],
                'verbose_name_plural': 'посты',
            },
        ),
        migrations.CreateModel(
            name='PostStatistics',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True, verbose_name='Идентификатор временной точки')),
                ('date', models.DateTimeField(verbose_name='Дата получения временной точки')),
                ('comments', models.PositiveIntegerField(verbose_name='Кол-во комментариев')),
                ('likes', models.PositiveIntegerField(verbose_name='Кол-во лайков')),
                ('reposts', models.PositiveIntegerField(verbose_name='Кол-во репостов')),
                ('views', models.PositiveIntegerField(verbose_name='Кол-во просмотров')),
            ],
            options={
                'verbose_name': 'статистика',
                'ordering': ['date'],
                'verbose_name_plural': 'статистики',
            },
        ),
    ]