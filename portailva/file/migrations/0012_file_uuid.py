# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2018-10-20 17:04
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


def gen_uuid(apps, schema_editor):
    File = apps.get_model('file', 'file')
    for row in File.objects.all():
        while True:
            row.uuid = uuid.uuid4()
            if not File.objects.filter(uuid=row.uuid).exists():
                break

        row.save()

class Migration(migrations.Migration):

    dependencies = [
        ('file', '0011_file_is_public'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, verbose_name='uuid'),
        ),
        migrations.RunPython(gen_uuid, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='file',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, verbose_name='uuid')
        )
    ]


