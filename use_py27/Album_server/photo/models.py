# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from smartfields import fields

from django.conf import settings
from django.core.files.storage import FileSystemStorage


from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Photo(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

class Images(models.Model):
    fs = FileSystemStorage(location=settings.FILES_DIR)

    image = fields.ImageField(upload_to='%Y/%m/%d/orig', storage=fs)
    created = models.DateTimeField(auto_now_add=True)
    photoId = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='imageRelate', default='0')

    class Meta:
        ordering = ('-created', '-pk', )

class Key(models.Model):
    name = models.CharField(max_length=30)
    key = models.CharField(max_length=10)