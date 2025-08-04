"""
WSGI config for news_aggregator_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for the 'wsgi' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_aggregator_project.settings')

# Initialize Django WSGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
application = get_wsgi_application()

# Optional: Add middleware for production environments
# This can be useful for handling security headers or other WSGI-level concerns
try:
    from whitenoise import WhiteNoise
    application = WhiteNoise(application, root='staticfiles')
    # Enable compression and caching headers
    application.add_files('staticfiles', prefix='')
except ImportError:
    pass
