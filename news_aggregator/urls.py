from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    
    # Categories
    path('categories/', views.categories, name='categories'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    # Topics
    path('topics/', views.topics, name='topics'),
    path('topics/edit/<int:pk>/', views.edit_topic, name='edit_topic'),
    path('topics/delete/<int:pk>/', views.delete_topic, name='delete_topic'),
    
    # Keywords
    path('keywords/', views.keywords, name='keywords'),
    path('keywords/delete/<int:pk>/', views.delete_keyword, name='delete_keyword'),
    
    # API Settings
    path('api-settings/', views.api_settings, name='api_settings'),
    path('api-settings/edit/<int:pk>/', views.edit_api_setting, name='edit_api_setting'),
    path('api-settings/delete/<int:pk>/', views.delete_api_setting, name='delete_api_setting'),
    
    # RSS Feeds
    path('rss-feeds/', views.rss_feeds, name='rss_feeds'),
    path('rss-feeds/edit/<int:pk>/', views.edit_rss_feed, name='edit_rss_feed'),
    path('rss-feeds/delete/<int:pk>/', views.delete_rss_feed, name='delete_rss_feed'),
    
    # News Search
    path('search/', views.search_news, name='search_news'),
    path('toggle-duplicate/<int:pk>/', views.toggle_duplicate, name='toggle_duplicate'),
    
    # Export
    path('export/csv/', views.export_csv, name='export_csv'),
    path('export/pdf/', views.export_pdf, name='export_pdf'),
]
