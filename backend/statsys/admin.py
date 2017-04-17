from django.contrib import admin
from .models import PostStatistics, Post


class PostStatisticsAdmin(admin.TabularInline):
    model = PostStatistics
    extra = 1
    readonly_fields = ('post', 'date_unixtime', 'date_datetime', 'likes', 'comments', 'reposts', 'views' )

    def has_add_permission(self, request):
        return False


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner_id', 'date', 'post_type','marked_as_ads')
    readonly_fields = ('id', 'owner_id','date', 'post_type','marked_as_ads')
    list_filter = [
        'post_type',
        'marked_as_ads',
    ]
    fields = (
        'id',
        'owner_id',
        'date',
        'post_type',
        'marked_as_ads'
    )
    inlines = [
        PostStatisticsAdmin,
    ]


admin.site.register(Post, PostAdmin)