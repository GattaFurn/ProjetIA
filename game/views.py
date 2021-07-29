from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import redirect
from game.models import Game,Player,Qtable,AIInfo
from django.core import serializers
from django import forms
import random

row_column = 8
 

class NewGameForm(forms.Form):
    player1_name = forms.CharField(label="Player name:",widget=forms.HiddenInput())
    player1_color = forms.CharField(label="Player Color:",widget=forms.HiddenInput())
    player2_name = forms.CharField(label="Player name:",widget=forms.HiddenInput())
    player2_color = forms.CharField(label="Player Color:",widget=forms.HiddenInput())

def index(request):
    if request.method == "GET": #quand c'est la premiere fois qu'on vient
        form = NewGameForm()
        if(request.session['player1'] == None):
            return redirect('../connection')

        form.fields["player1_name"].initial= request.session['player1'].get("username")
        form.fields["player1_color"].initial = request.session['player1'].get("color")

        if(request.session['player2'] == None):
            return render(request, "game/index.html", { "form": form ,"player1":request.session['player1'],"player2":None})

        form.fields["player2_name"].initial= request.session['player2'].get("username")
        form.fields["player2_color"].initial = request.session['player2'].get("color")
        
        if(request.session['player1']["type"] == "IA"):
            request.session['player1'],request.session['player2'] = request.session['player2'],request.session['player1']
        return render(request, "game/index.html", { "form": form ,"player1":request.session['player1'],"player2":request.session['player2']})

    if request.method == "POST":
        form = NewGameForm(request.POST)
        if form.is_valid():
            player1 = request.session['player1'].copy()
            player_position(player1,1)
            player2 = request.session['player2'].copy()
            player_position(player2,2)
            game_state = create_new_game(player1,player2)
            request.session["idGame"] = game_state["id"]
            return render(request, 'game/new_game.html',{"game_state":game_state})
    return redirect('../connection')

def player_position(player,position):
    player["position"] = [0,0] if position == 1 else [7,7]

def create_new_game(p1,p2):
    player1 = Player.objects.get(id = p1["id"])
    player2 = Player.objects.get(id = p2["id"])
    game_state = Game.objects.create(
        board=create_board(),
        position_player1=p1["position"],
        position_player2=p2["position"],
        current_player=0,
        player1=player1,
        player2=player2,
        ia_info = create_new_ia_info(player2.ia.eps) if p2["type"]=="IA" else None ,
    ).__dict__
    del game_state["_state"]
    del game_state["time"]
    game_state["player1_color"] = player1.user.color
    game_state["player1_username"] =  player1.user.pseudo
    game_state["player2_color"] = player2.user.color if p2["type"]!="IA"  else player2.ia.color
    game_state["player2_username"] = player2.user.pseudo if p2["type"]!="IA" else player2.ia.pseudo
    return game_state

def create_new_ia_info(ia_eps):
    ia_info = AIInfo.objects.create(
        st = [row_column-1,row_column-1],
        stp1 = [row_column-1,row_column-1],
        at = 0,
        atp1 = 0, 
        eps = ia_eps,
    )
    return ia_info

def create_board():
    board = []
    for i in range(row_column):
        row = []
        for j in range(row_column):
            row.append(0)
        board.append(row)
    board[0][0] = 1
    board[row_column-1][row_column-1] = 2
    return board