# Generated by Django 3.1.1 on 2021-04-19 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0033_auto_20210419_1454'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='qtable',
            unique_together={('board', 'posP2'), ('board', 'posP1'), ('board', 'playerTurn')},
        ),
    ]