# Generated by Django 3.0.8 on 2020-08-01 20:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0002_auto_20200728_0743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productioningredients',
            name='production',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production.Production'),
        ),
    ]
