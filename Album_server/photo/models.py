from django.db import models
from smartfields import fields

from django.conf import settings
from django.core.files.storage import FileSystemStorage

class photo(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    path = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

class Images(models.Model):
    fs = FileSystemStorage(location=settings.FILES_DIR)

    image = fields.ImageField(upload_to='%Y/%m/%d/orig', storage=fs)
    created = models.DateTimeField(auto_now_add=True)
    photoId = models.ForeignKey(Posting, related_name='imageRelate', default='0')

    class Meta:
        ordering = ('-created_at', '-pk', )