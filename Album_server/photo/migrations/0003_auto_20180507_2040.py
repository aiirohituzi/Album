# Generated by Django 2.0.4 on 2018-05-07 11:40

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import smartfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('photo', '0002_auto_20180421_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='image',
            field=smartfields.fields.ImageField(storage=django.core.files.storage.FileSystemStorage(location='D:\\github\\Album\\Album_client\\src\\assets\\image'), upload_to='%Y/%m/%d/orig'),
        ),
        migrations.AlterField(
            model_name='images',
            name='photoId',
            field=models.ForeignKey(default='0', on_delete=django.db.models.deletion.CASCADE, related_name='imageRelate', to='photo.Photo'),
        ),
    ]