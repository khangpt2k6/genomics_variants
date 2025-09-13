"""
ASGI config for moffitt_variants project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moffitt_variants.settings')

application = get_asgi_application()

