# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-01-17 22:17
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations
import smartfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=smartfields.fields.ImageField(storage=django.core.files.storage.FileSystemStorage(location=b'D:\\github\\Album\\use_py27\\Album_server\\media\\photo'), upload_to='%Y/%m/%d/orig'),
        ),
    ]
