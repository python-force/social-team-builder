from __future__ import absolute_import, unicode_literals
from django.utils import six
from boto.s3.connection import OrdinaryCallingFormat # need to change that to boto3

from .common import * # noga

# SSL PROCESSING
# ------------------------------------------------------------------------------
SECURE_SSL_REDIRECT = False

# SECRET CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
# Raises ImproperlyConfigured exception if DJANGO_SECRET_KEY not in os.environ
SECRET_KEY = env('SECRET_KEY', default='re+.a}t~qS,fR2eG')

# This ensures that Django will be able to detect a secure connection
# properly on Heroku.
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# SITE CONFIGURATION
# ------------------------------------------------------------------------------
# Hosts/domain names that are valid for this site
# See https://docs.djangoproject.com/en/2.1/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']
# STB SITE CONFIGURATION

# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_FILE_STORAGE = 'config.custom_storages.MediaStorage'
THUMBNAIL_DEFAULT_STORAGE = 'config.custom_storages.MediaStorage'


AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('REGION_NAME')  # e.g. us-east-2
AWS_S3_CUSTOM_DOMAIN = '{}.s3.amazonaws.com'.format(AWS_STORAGE_BUCKET_NAME)
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_CALLING_FORMAT = OrdinaryCallingFormat()
AWS_DEFAULT_ACL = "public-read"

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
AWS_HEADERS = {
    'Cache-Control': six.b('max-age=%d, s-maxage=%d, must-revalidate' % (
        AWS_EXPIRY, AWS_EXPIRY))
}

# URL that handles the media served from MEDIA_ROOT, used for managing
# stored files.
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)


# Static Assests
# ------------------------
STATICFILES_STORAGE = 'config.custom_storages.CachedS3BotoStaticStorage'
COMPRESS_STORAGE = 'config.custom_storages.CachedS3BotoStaticStorage'

AWS_S3_SECURE_URLS = True

STATICFILES_LOCATION = 'static'
STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)


# See: https://github.com/antonagestam/collectfast
# For Django 1.7+, 'collectfast' should come before
# 'django.contrib.staticfiles'
AWS_PRELOAD_METADATA = True
INSTALLED_APPS = ['collectfast',] + INSTALLED_APPS

# MIDDLEWARE_CLASSES = ['hide_herokuapp.middleware.HideHerokuappFromRobotsMiddleware',] + MIDDLEWARE_CLASSES

# MINIFY HTML
# ------------------------
# HTML_MINIFY = True