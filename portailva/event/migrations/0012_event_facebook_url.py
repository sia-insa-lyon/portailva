# Generated by Django 2.2.8 on 2019-12-16 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0011_eventtype_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='facebook_url',
            field=models.URLField(blank=True, verbose_name='Evènement Facebook'),
        ),
    ]
