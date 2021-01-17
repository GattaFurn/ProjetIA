# Generated by Django 3.1.1 on 2021-01-17 15:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0024_auto_20210117_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='board',
            field=models.TextField(default='undefined'),
        ),
        migrations.AddField(
            model_name='game',
            name='current_player',
            field=models.IntegerField(choices=[(0, 0), (1, 1)], default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='game',
            name='time',
            field=models.TimeField(default=datetime.datetime(2021, 1, 17, 16, 29, 51, 201428)),
        ),
        migrations.AlterField(
            model_name='qtable',
            name='board',
            field=models.TextField(default='undefined'),
        ),
    ]
