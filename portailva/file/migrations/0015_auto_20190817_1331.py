# Generated by Django 2.2.2 on 2019-08-17 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0014_filefolder_is_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filefolder',
            name='is_public',
            field=models.BooleanField(blank=True, default=False, verbose_name='Public'),
        ),
    ]
