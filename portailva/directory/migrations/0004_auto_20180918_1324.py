# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-09-18 13:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0003_unaccent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directoryentry',
            name='phone',
            field=models.CharField(blank=True, default='', max_length=10, verbose_name='Téléphone'),
            preserve_default=False,
        ),
    ]
