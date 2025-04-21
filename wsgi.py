"""
WSGI config for expenseTrackerAPI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
from django.contrib.auth.models import User

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expenseTrackerAPI.settings')

application = get_wsgi_application()

users = User.objects.filter(is_superuser=True).filter(email="admin@email.com").first()
if not users:
    User.objects.create_superuser(username="admin", email="admin@email.com", password="admin", is_active=True,
                                  is_staff=True)