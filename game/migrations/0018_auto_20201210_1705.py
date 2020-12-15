# Generated by Django 3.1.1 on 2020-12-10 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_auto_20201201_2101'),
    ]

    operations = [
        migrations.AddField(
            model_name='ia',
            name='eps',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='ia',
            name='color',
            field=models.CharField(choices=[('BL', '#0099ff'), ('PK', '#ff99ff'), ('YW', '#ffcc66'), ('GN', '#80ff80'), ('VT', '#bf80ff'), ('RD', '#b30000'), ('OE', '#ff8c1a'), ('CN', '#80ffff')], default='BL', max_length=2),
        ),
    ]