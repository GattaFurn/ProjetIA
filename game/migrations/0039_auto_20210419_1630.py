# Generated by Django 3.1.1 on 2021-04-19 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0038_auto_20210419_1607'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='qtable',
            unique_together={('board', 'posP1', 'posP2', 'playerTurn')},
        ),
    ]
