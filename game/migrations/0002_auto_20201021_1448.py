# Generated by Django 3.1.1 on 2020-10-21 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ia',
            old_name='pseudo',
            new_name='login',
        ),
    ]
