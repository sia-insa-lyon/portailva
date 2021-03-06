# Generated by Django 2.2.2 on 2019-08-17 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('association', '0025_category_latex_color_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accomplishment',
            name='requirement',
            field=models.ForeignKey(limit_choices_to={'type': 'accomplishment'}, on_delete=django.db.models.deletion.CASCADE, to='association.Requirement', verbose_name='Condition'),
        ),
        migrations.AlterField(
            model_name='association',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='association.Category', verbose_name='Catégorie'),
        ),
    ]
