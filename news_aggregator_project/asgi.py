"""
ASGI config for news_aggregator_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default Django settings module for the 'asgi' app.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_aggregator_project.settings')

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

# You can add middleware or other ASGI components here if needed
# For example, for Django Channels:
# import channels.routing
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter

# application = ProtocolTypeRouter({
#     "http": django_asgi_app,
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             channels_routing.websocket_urlpatterns
#         )
#     ),
# })

# For a standard Django application without Channels, use this:
application = django_asgi_app
