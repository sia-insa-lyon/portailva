# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-10-13 18:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0017_auto_20171011_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='association',
            name='logo_url',
            field=models.URLField(blank=True, help_text="Privilégier les liens en HTTPS, assurez-vous que le lien que vous fournissez pointe directement sur l'image (pas de page d'affichage comme Google Drive ou autres).", verbose_name='URL du logo'),
        ),
    ]
