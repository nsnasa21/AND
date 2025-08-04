from django.contrib import admin
from .models import Category, Topic, Keyword, APISetting, RSSFeed, Article, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')

@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    list_display = ('text', 'topic', 'created_at')
    list_filter = ('topic__category', 'topic')
    search_fields = ('text', 'topic__name')

@admin.register(APISetting)
class APISettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)

@admin.register(RSSFeed)
class RSSFeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'url')

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'source', 'published_at', 'category', 'is_duplicate', 'created_at')
    list_filter = ('source', 'category', 'is_duplicate', 'published_at')
    search_fields = ('title', 'description', 'content')
    date_hierarchy = 'published_at'

admin.site.register(UserProfile)
