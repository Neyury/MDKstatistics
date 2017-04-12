from django.contrib import admin
from .models import PostStatistics, Post
# Register your models here.


class PostStatisticsAdmin(admin.TabularInline):
    model = PostStatistics
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'post_type', 'is_pinned','marked_as_ads')
    list_filter = [
        'post_type',
        'is_pinned',
        'marked_as_ads',
    ]

    fields = (
        ('id','date' ),
        'post_type',
        ('is_pinned','marked_as_ads' ),
    )
    inlines = [
        PostStatisticsAdmin,
    ]


admin.site.register(Post, PostAdmin)