from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.template.loader import get_template
from django.conf import settings
import csv
import io
from datetime import datetime
from weasyprint import HTML
import pandas as pd

from .models import Category, Topic, Keyword, APISetting, RSSFeed, Article
from .forms import CategoryForm, TopicForm, KeywordForm, APISettingForm, RSSFeedForm
from .services import NewsAggregator

def dashboard(request):
    categories = Category.objects.all()
    articles = Article.objects.filter(is_duplicate=False).order_by('-published_at')[:10]
    context = {
        'categories': categories,
        'articles': articles
    }
    return render(request, 'dashboard.html', context)

def categories(request):
    categories = Category.objects.all()
    form = CategoryForm()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('categories')
    
    context = {
        'categories': categories,
        'form': form
    }
    return render(request, 'categories.html', context)

def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    form = CategoryForm(instance=category)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('categories')
    
    context = {
        'form': form,
        'category': category
    }
    return render(request, 'edit_category.html', context)

def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('categories')
    return render(request, 'confirm_delete.html', {'object': category})

def topics(request):
    topics = Topic.objects.select_related('category').all()
    form = TopicForm()
    
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Topic created successfully!')
            return redirect('topics')
    
    context = {
        'topics': topics,
        'form': form
    }
    return render(request, 'topics.html', context)

def edit_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    form = TopicForm(instance=topic)
    
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, 'Topic updated successfully!')
            return redirect('topics')
    
    context = {
        'form': form,
        'topic': topic
    }
    return render(request, 'edit_topic.html', context)

def delete_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        topic.delete()
        messages.success(request, 'Topic deleted successfully!')
        return redirect('topics')
    return render(request, 'confirm_delete.html', {'object': topic})

def keywords(request):
    keywords = Keyword.objects.select_related('topic', 'topic__category').all()
    form = KeywordForm()
    
    if request.method == 'POST':
        form = KeywordForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            keywords_text = form.cleaned_data['keywords']
            keyword_list = [kw.strip() for kw in keywords_text.split(',') if kw.strip()]
            
            for keyword_text in keyword_list:
                Keyword.objects.get_or_create(text=keyword_text, topic=topic)
            
            messages.success(request, f'{len(keyword_list)} keywords added successfully!')
            return redirect('keywords')
    
    context = {
        'keywords': keywords,
        'form': form
    }
    return render(request, 'keywords.html', context)

def delete_keyword(request, pk):
    keyword = get_object_or_404(Keyword, pk=pk)
    if request.method == 'POST':
        keyword.delete()
        messages.success(request, 'Keyword deleted successfully!')
        return redirect('keywords')
    return render(request, 'confirm_delete.html', {'object': keyword})

def api_settings(request):
    apis = APISetting.objects.all()
    form = APISettingForm()
    
    if request.method == 'POST':
        form = APISettingForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'API setting saved successfully!')
            return redirect('api_settings')
    
    context = {
        'apis': apis,
        'form': form
    }
    return render(request, 'api_settings.html', context)

def edit_api_setting(request, pk):
    api_setting = get_object_or_404(APISetting, pk=pk)
    form = APISettingForm(instance=api_setting)
    
    if request.method == 'POST':
        form = APISettingForm(request.POST, instance=api_setting)
        if form.is_valid():
            form.save()
            messages.success(request, 'API setting updated successfully!')
            return redirect('api_settings')
    
    context = {
        'form': form,
        'api_setting': api_setting
    }
    return render(request, 'edit_api_setting.html', context)

def delete_api_setting(request, pk):
    api_setting = get_object_or_404(APISetting, pk=pk)
    if request.method == 'POST':
        api_setting.delete()
        messages.success(request, 'API setting deleted successfully!')
        return redirect('api_settings')
    return render(request, 'confirm_delete.html', {'object': api_setting})

def rss_feeds(request):
    feeds = RSSFeed.objects.select_related('category').all()
    form = RSSFeedForm()
    
    if request.method == 'POST':
        form = RSSFeedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'RSS feed added successfully!')
            return redirect('rss_feeds')
    
    context = {
        'feeds': feeds,
        'form': form
    }
    return render(request, 'rss_feeds.html', context)

def edit_rss_feed(request, pk):
    feed = get_object_or_404(RSSFeed, pk=pk)
    form = RSSFeedForm(instance=feed)
    
    if request.method == 'POST':
        form = RSSFeedForm(request.POST, instance=feed)
        if form.is_valid():
            form.save()
            messages.success(request, 'RSS feed updated successfully!')
            return redirect('rss_feeds')
    
    context = {
        'form': form,
        'feed': feed
    }
    return render(request, 'edit_rss_feed.html', context)

def delete_rss_feed(request, pk):
    feed = get_object_or_404(RSSFeed, pk=pk)
    if request.method == 'POST':
        feed.delete()
        messages.success(request, 'RSS feed deleted successfully!')
        return redirect('rss_feeds')
    return render(request, 'confirm_delete.html', {'object': feed})

def search_news(request):
    categories = Category.objects.all()
    articles = Article.objects.none()
    selected_category = None
    search_performed = False
    
    if request.method == 'POST':
        category_id = request.POST.get('category')
        if category_id:
            selected_category = get_object_or_404(Category, pk=category_id)
            aggregator = NewsAggregator()
            articles = aggregator.search_by_category(selected_category)
            search_performed = True
    
    # Apply filters
    source = request.GET.get('source')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    show_duplicates = request.GET.get('show_duplicates')
    
    if source:
        articles = articles.filter(source__icontains=source)
    
    if date_from:
        articles = articles.filter(published_at__gte=date_from)
    
    if date_to:
        articles = articles.filter(published_at__lte=date_to)
    
    if not show_duplicates:
        articles = articles.filter(is_duplicate=False)
    
    paginator = Paginator(articles, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'categories': categories,
        'selected_category': selected_category,
        'page_obj': page_obj,
        'search_performed': search_performed,
        'source': source,
        'date_from': date_from,
        'date_to': date_to,
        'show_duplicates': show_duplicates
    }
    return render(request, 'search_news.html', context)

def toggle_duplicate(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.is_duplicate = not article.is_duplicate
    article.save()
    return JsonResponse({'success': True, 'is_duplicate': article.is_duplicate})

def export_csv(request):
    selected_ids = request.POST.getlist('selected_articles')
    articles = Article.objects.filter(id__in=selected_ids)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="news_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Title', 'Description', 'Source', 'Published At', 'URL'])
    
    for article in articles:
        writer.writerow([
            article.title,
            article.description,
            article.source,
            article.published_at.strftime('%Y-%m-%d %H:%M:%S'),
            article.url
        ])
    
    return response

def export_pdf(request):
    selected_ids = request.POST.getlist('selected_articles')
    articles = Article.objects.filter(id__in=selected_ids)
    
    template = get_template('pdf_template.html')
    context = {
        'articles': articles,
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    html = template.render(context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="news_bulletin.pdf"'
    
    HTML(string=html).write_pdf(response)
    return response
