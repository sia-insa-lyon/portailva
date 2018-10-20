# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-10-20 15:55
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0011_file_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='uuid'),
        ),
    ]