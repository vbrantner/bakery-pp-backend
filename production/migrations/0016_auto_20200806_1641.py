# Generated by Django 3.0.8 on 2020-08-06 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0015_auto_20200806_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temperatursensor',
            name='humidity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='temperatursensor',
            name='temperature',
            field=models.IntegerField(),
        ),
    ]
