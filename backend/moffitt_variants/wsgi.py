"""
WSGI config for moffitt_variants project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moffitt_variants.settings')

application = get_wsgi_application()

