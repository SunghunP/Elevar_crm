"""
ASGI config for elevar_crm project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elevar_crm.settings')

application = get_asgi_application()

# Configure Django App for Heroku 
import django_on_heroku
django_on_heroku.settings(locals())
