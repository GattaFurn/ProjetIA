# Generated by Django 3.1.1 on 2020-12-01 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_auto_20201201_1003'),
    ]

    operations = [
        migrations.RenameField(
            model_name='qtable',
            old_name='Player_Turn',
            new_name='PlayerTurn',
        ),
    ]
