# Generated by Django 3.1.1 on 2021-04-08 14:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0029_auto_20210407_1826'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='iaInfo',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='game',
            name='time',
            field=models.TimeField(default=datetime.datetime(2021, 4, 8, 16, 26, 50, 854820)),
        ),
    ]
