import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('RDS_DB_NAME', 'centralbcs')
os.environ.setdefault('RDS_HOSTNAME', 'localhost')
os.environ.setdefault('RDS_PORT', 3306)
os.environ.setdefault('RDS_USERNAME', 'centralbcsdb')
os.environ.setdefault('RDS_PASS', 'c0mpl3x!')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "centralbcs.settings")
application = get_wsgi_application()