# Generated by Django 2.2.8 on 2020-03-21 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0005_place_is_room'),
        ('association', '0029_auto_20191101_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='association',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='association', to='utils.Place', verbose_name='Local'),
        ),
    ]
