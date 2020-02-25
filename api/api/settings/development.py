from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS += (
    'rest_framework_swagger',
    'debug_toolbar',
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True if DEBUG else False,
}
