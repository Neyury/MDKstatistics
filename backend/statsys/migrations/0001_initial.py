# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-16 17:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


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
                ('marked_as_ads', models.BooleanField(default=0, verbose_name='Пост рекламный')),
            ],
            options={
                'verbose_name_plural': 'посты',
                'ordering': ['-date'],
                'verbose_name': 'пост',
            },
        ),
        migrations.CreateModel(
            name='PostStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_unixtime', models.IntegerField(verbose_name='время в unixtime')),
                ('date_datetime', models.DateTimeField(verbose_name='стандартное время')),
                ('likes', models.PositiveIntegerField(verbose_name='Кол-во лайков')),
                ('comments', models.PositiveIntegerField(verbose_name='Кол-во комментариев')),
                ('reposts', models.PositiveIntegerField(verbose_name='Кол-во репостов')),
                ('views', models.PositiveIntegerField(verbose_name='Кол-во просмотров')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='statsys.Post', verbose_name='пост')),
            ],
            options={
                'verbose_name_plural': 'статистики',
                'ordering': ['-date_unixtime'],
                'verbose_name': 'статистика',
            },
        ),
    ]
