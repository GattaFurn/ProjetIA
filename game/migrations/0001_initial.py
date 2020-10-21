# Generated by Django 3.1.1 on 2020-10-20 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('connection', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pseudo', models.CharField(max_length=50)),
                ('color', models.CharField(choices=[('BL', 'Blue'), ('PK', 'Pink'), ('YW', 'Yellow'), ('GN', 'Green'), ('VT', 'Violet'), ('RD', 'Red'), ('OE', 'Orange'), ('CN', 'Cyan')], default='BL', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='game.ia')),
                ('utilisateur', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='connection.utilisateur')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board', models.CharField(max_length=145)),
                ('positionPlayer1', models.CharField(max_length=5)),
                ('positionPlayer2', models.CharField(max_length=5)),
                ('currentPlayer', models.IntegerField(choices=[(0, 0), (1, 1)])),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player1', to='game.player')),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player2', to='game.player')),
            ],
        ),
    ]