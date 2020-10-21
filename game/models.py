from django.db import models
from connection.models import *

# Create your models here.
class IA(models.Model):
    pseudo = models.CharField(max_length=50)
    color = models.CharField(max_length=2,choices = COLOR_CHOICES,default = 'BL')

class Player(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE,null = True)
    ia = models.ForeignKey(IA, on_delete=models.CASCADE,null = True)

class Game(models.Model):
    board = models.CharField(max_length=145)
    positionPlayer1 = models.CharField(max_length=5)
    positionPlayer2 = models.CharField(max_length=5)
    currentPlayer = models.IntegerField(choices = [(0,0),(1,1)])
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player2')