"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

#add yout project directory to the sys.path
project_home = 'home/alvaroconde/AplicacionDjango/mysite'
if project_home not in sys.path:
    sys.path.insert(0, project_home)


#set environment variable to tell django where your settings.py is 
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'


#serve django via WSGI
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
application = get_wsgi_application()
