# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 13:37
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0004_auto_20161026_1534'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mandate',
            options={'default_permissions': ('add', 'change', 'delete', 'admin')},
        ),
        migrations.AlterModelOptions(
            name='people',
            options={'default_permissions': ('add', 'change', 'delete', 'admin')},
        ),
        migrations.AlterModelOptions(
            name='peoplerole',
            options={'default_permissions': ('add', 'change', 'delete', 'admin')},
        ),
    ]
