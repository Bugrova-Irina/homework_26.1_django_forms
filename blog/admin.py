from django.contrib import admin

from blog.models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'is_published', 'view_counter')
    list_filter = ('title', 'is_published')
    search_fields = ('title', 'created_at')
