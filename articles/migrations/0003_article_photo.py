# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-21 05:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos'),
        ),
    ]