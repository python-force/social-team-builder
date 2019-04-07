from __future__ import absolute_import, unicode_literals
from .common import * # noga

# DEBUG
# ------------------------------------------------------------------------------
DEBUG = env.bool('DJANGO_DEBUG', default=True)
TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Note: This key only used for development and testing.
SECRET_KEY = env('SECRET_KEY', default='re+.a}t~qS,fR2eG')

# DJANGO DEBUG TOOLBAR
# ------------------------------------------------------------------------------
INSTALLED_APPS  = ['debug_toolbar',] + INSTALLED_APPS
MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware',] + MIDDLEWARE

INTERNAL_IPS = ('127.0.0.1', '68.186.152.97', '71.87.153.54', '66.65.75.74',)
DEBUG_TOOLBAR_CONFIG = {
     'INTERCEPT_REDIRECTS': False,
     }

ADMINS = ('dummy@example.com',)
MANAGERS = ADMINS

# COMPRESS_ENABLED=False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# DEFAULT_FILE_STORAGE = 'config.custom_storages.OverwriteStorage'
MEDIAFILES_LOCATION = 'media'
STATICFILES_LOCATION = 'static'

COMPRESS_ENABLED=False