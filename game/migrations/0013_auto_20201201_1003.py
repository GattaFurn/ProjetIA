# Generated by Django 3.1.1 on 2020-12-01 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0012_auto_20201201_0955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='q_table',
            name='Down',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='q_table',
            name='Left',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='q_table',
            name='Right',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='q_table',
            name='Up',
            field=models.FloatField(default=0),
        ),
        migrations.AlterUniqueTogether(
            name='q_table',
            unique_together=set(),
        ),
    ]
