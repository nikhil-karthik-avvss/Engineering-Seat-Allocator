
from django.apps import AppConfig


class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'
    
'''
# apps.py
from django.apps import AppConfig

class PagesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pages'

    def ready(self):
        import pages.signals  # Import signals module
'''
