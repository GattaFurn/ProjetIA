from django.db import models
from connection.models import *

# Create your models here.
class IA(models.Model):
    pseudo = models.CharField(max_length=50)
    color = models.CharField(max_length=2,choices = COLOR_CHOICES, default = 'BL')

    def __str__(self):
        return str(self.id) +" - "+ self.pseudo

class Player(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE,null = True, blank=True)
    ia = models.OneToOneField(IA, on_delete=models.CASCADE,null = True, blank=True)

    def __str__(self):
        if(self.utilisateur):
            return str(self.id) + "-" + self.utilisateur.pseudo
        else:
            return str(self.id) + "-" + self.ia.pseudo

class Game(models.Model):
    board = models.TextField()
    positionPlayer1 = models.CharField(max_length=6)
    positionPlayer2 = models.CharField(max_length=6)
    currentPlayer = models.IntegerField(choices = [(0,0),(1,1)])
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player2')

class Qtable(models.Model):
    board = models.TextField()
    posP1 = models.CharField(max_length=6)
    posP2 = models.CharField(max_length=6)
    playerTurn = models.IntegerField(choices = [(0,0),(1,1)])
    up = models.FloatField(default = 0)
    down = models.FloatField(default = 0)
    left = models.FloatField(default = 0)
    right = models.FloatField(default = 0)

    class Meta:
        unique_together = (("board","posP1","posP2","playerTurn"),)

    def __str__(self):
        return str(self.id)
