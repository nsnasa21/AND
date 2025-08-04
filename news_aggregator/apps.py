from django.apps import AppConfig

class NewsAggregatorConfig(AppConfig):
    """Configuration for the news aggregator application."""
    
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news_aggregator'
    verbose_name = "News Aggregator"
    
    def ready(self):
        """
        This method is called when the application is ready.
        Use this to register signals or perform other initialization tasks.
        """
        # Import signals to ensure they're registered
        try:
            from . import signals
        except ImportError:
            pass
            
        # Optional: Schedule periodic tasks for news aggregation
        # from .services import NewsAggregator
        # NewsAggregator.schedule_daily_updates()
