# Generated by Django 3.0.8 on 2020-08-06 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0013_auto_20200806_1631'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperatursensor',
            name='humidity',
            field=models.FloatField(null=True),
        ),
    ]
