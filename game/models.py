from django.db import models
from connection.models import *
from datetime import * 

# Create your models here.
class IA(models.Model):
    pseudo = models.CharField(max_length=50)
    color = models.CharField(max_length=2,choices = COLOR_CHOICES, default = 'BL')
    eps = models.FloatField(default = 0)

    def __str__(self):
        return str(self.id) +" - "+ self.pseudo

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null = True, blank=True)
    ia = models.OneToOneField(IA, on_delete=models.CASCADE,null = True, blank=True)

    def __str__(self):
        if(self.user):
            return str(self.id) + "-" + self.user.pseudo
        else:
            return str(self.id) + "-" + self.ia.pseudo

class AIInfo(models.Model):
    st = models.CharField(max_length=6)
    stp1 = models.CharField(max_length=6)
    at = models.IntegerField(choices = [(0,0),(1,1),(2,2),(3,3)])
    atp1 = models.IntegerField(choices = [(0,0),(1,1),(2,2),(3,3)])
    eps = models.FloatField(default = 0)

    def __str__(self):
        return str(self.id)

class Game(models.Model):
    board = models.TextField(default = "")
    position_player1 = models.CharField(max_length=6)
    position_player2 = models.CharField(max_length=6)
    current_player = models.IntegerField(choices = [(0,0),(1,1)])
    player1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player1')
    player2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player2')
    player1_box_total = models.IntegerField(default = 1)
    player2_box_total = models.IntegerField(default = 1)
    player1_box_turn = models.IntegerField(default = 1)
    player2_box_turn = models.IntegerField(default = 1)
    time = models.TimeField(default = datetime(1997,11,25))
    max_box_taken_with_area = models.IntegerField(default = 1)
    ia_info = models.ForeignKey(AIInfo, on_delete=models.CASCADE, related_name='ia_info')
    code = models.IntegerField(default = 0)


class Qtable(models.Model):
    board = models.TextField(default = "")
    pos_p1 = models.CharField(max_length=6)
    pos_p2 = models.CharField(max_length=6)
    player_turn = models.IntegerField(choices = [(0,0),(1,1)])
    up = models.FloatField(default = 0)
    down = models.FloatField(default = 0)
    left = models.FloatField(default = 0)
    right = models.FloatField(default = 0)

    class Meta:
        unique_together = ("board","pos_p1","pos_p2","player_turn")

    def __str__(self):
        return str(self.id)
