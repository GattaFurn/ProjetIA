# Generated by Django 3.1.1 on 2020-12-01 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_auto_20201201_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='positionPlayer1',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='game',
            name='positionPlayer2',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='qtable',
            name='posP1',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='qtable',
            name='posP2',
            field=models.CharField(max_length=6),
        ),
    ]