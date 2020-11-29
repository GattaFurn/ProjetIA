from django.db import models
from connection.models import *

# Create your models here.
class IA(models.Model):
    id = models.AutoField(primary_key=True)
    pseudo = models.CharField(max_length=50)
    Q_table = models.TextField(default = '[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]')
    color = models.CharField(max_length=2,choices = COLOR_CHOICES, default = 'BL')

    def __str__(self):
        return str(self.id) +" - "+ self.pseudo

class Player(models.Model):
    id = models.AutoField(primary_key=True)
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE,null = True, blank=True)
    ia = models.OneToOneField(IA, on_delete=models.CASCADE,null = True, blank=True)

    def __str__(self):
        if(self.utilisateur):
            return str(self.utilisateur)
        else:
            return str(self.ia)

class Game(models.Model):
    id = models.AutoField(primary_key=True)
    board = models.TextField()
    positionPlayer1 = models.CharField(max_length=5)
    positionPlayer2 = models.CharField(max_length=5)
    currentPlayer = models.IntegerField(choices = [(0,0),(1,1)])
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player2')