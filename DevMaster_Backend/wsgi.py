"""
WSGI config for DevMaster_Backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DevMaster_Backend.settings')

application = get_wsgi_application()
# application = WhiteNoise(application, root='/DevMaster_Backend/static')
# application.add_files('/path/DevMaster_Backend/static')
