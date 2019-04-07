from django.conf import settings
from storages.backends.s3boto import S3BotoStorage
from django.core.files.storage import get_storage_class

import os
from django.core.files.storage import FileSystemStorage

class OverwriteStorage(FileSystemStorage):
    location = settings.MEDIAFILES_LOCATION
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class StaticStorage(S3BotoStorage):
    location = settings.STATICFILES_LOCATION
    file_overwrite = True


class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION
    file_overwrite = True


class CachedS3BotoStaticStorage(S3BotoStorage):

    # S3 storage backend that saves the files locally, too.

    location = 'static'

    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStaticStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(CachedS3BotoStaticStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name
