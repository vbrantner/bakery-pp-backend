# Generated by Django 3.0.8 on 2020-08-06 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0016_auto_20200806_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='temperatursensor',
            name='date_time',
            field=models.DateTimeField(default='2020-08-06 12:00:00'),
            preserve_default=False,
        ),
    ]