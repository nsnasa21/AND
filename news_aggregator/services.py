import requests
import feedparser
from datetime import datetime
from .models import Article, Topic, Keyword

class NewsAggregator:
    def search_by_category(self, category):
        # Get all keywords for topics in this category
        topics = category.topics.all()
        keywords = []
        for topic in topics:
            topic_keywords = topic.keywords.values_list('text', flat=True)
            keywords.extend(topic_keywords)
        
        if not keywords:
            return Article.objects.none()
        
        # Search using all available sources
        articles = self._search_news(keywords)
        
        # Assign category to articles
        for article in articles:
            article.category = category
            article.save()
        
        return articles
    
    def _search_news(self, keywords):
        articles = []
        
        # Example with NewsAPI (you would implement similar for other APIs)
        try:
            from newsapi import NewsApiClient
            newsapi = NewsApiClient(api_key='YOUR_NEWSAPI_KEY')
            for keyword in keywords:
                response = newsapi.get_everything(q=keyword, language='en')
                for article_data in response['articles']:
                    article, created = Article.objects.get_or_create(
                        url=article_data['url'],
                        defaults={
                            'title': article_data['title'],
                            'description': article_data['description'] or '',
                            'content': article_data['content'] or '',
                            'source': article_data['source']['name'],
                            'published_at': datetime.fromisoformat(
                                article_data['publishedAt'].replace('Z', '+00:00')
                            )
                        }
                    )
                    if created:
                        articles.append(article)
        except Exception as e:
            print(f"NewsAPI error: {e}")
        
        # RSS Feed processing
        try:
            from .models import RSSFeed
            rss_feeds = RSSFeed.objects.filter(is_active=True)
            for feed in rss_feeds:
                d = feedparser.parse(feed.url)
                for entry in d.entries:
                    # Check if any keyword is in the title or description
                    if any(kw.lower() in (entry.title + ' ' + getattr(entry, 'summary', '')).lower() 
                           for kw in keywords):
                        article, created = Article.objects.get_or_create(
                            url=entry.link,
                            defaults={
                                'title': entry.title,
                                'description': getattr(entry, 'summary', ''),
                                'source': feed.name,
                                'published_at': datetime.fromtimestamp(
                                    datetime(*entry.published_parsed[:6]).timestamp()
                                ) if hasattr(entry, 'published_parsed') else datetime.now()
                            }
                        )
                        if created:
                            articles.append(article)
        except Exception as e:
            print(f"RSS error: {e}")
        
        return articles
