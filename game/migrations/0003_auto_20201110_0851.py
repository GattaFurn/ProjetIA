# Generated by Django 3.1.1 on 2020-11-10 07:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20201021_1448'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ia',
            old_name='login',
            new_name='pseudo',
        ),
    ]
