# Generated by Django 2.2.2 on 2019-08-20 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0004_auto_20180918_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='directoryentry',
            name='description',
            field=models.TextField(help_text='{}/900 caractère{}', max_length=900, verbose_name="Description de l'association"),
        ),
    ]
