# Generated by Django 2.2.2 on 2020-01-07 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0015_auto_20190817_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='resourcefile',
            name='is_public',
            field=models.BooleanField(blank=True, default=False, verbose_name='Public'),
        ),
    ]
