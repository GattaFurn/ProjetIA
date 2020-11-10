from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

from django import forms
import random
 

class NewGameForm(forms.Form):
    player1 = forms.CharField(label="Player 1")
    player2 = forms.CharField(label="Player 2")


def index(request):
    if request.method == "GET": #quand c'est la premiere fois qu'on vient
        form = NewGameForm()
        if(request.session['player2'] == None):
            return render(request, "game/index.html", { "form": form ,"player1":request.session['player1'],"player2":None})
        else:
            return render(request, "game/index.html", { "form": form ,"player1":request.session['player1'],"player2":request.session['player2']})

    if request.method == "POST": #quand on a les noms des joueurs pour commencer la partie
        form = NewGameForm(request.POST)

        if form.is_valid():
            game_state = {
                "game_id" : 11,
                "board" : [[1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,2]],
                "players" : [{
                        "id" :  request.session['player1'].id,
                        "name" : request.session['player1'].username,
                        "color" : request.session['player1'].color,
                        "position" : [0,0]
                    },{
                        "id" :  request.session['player2'].id,
                        "name" : request.session['player2'].username,
                        "color" : request.session['player2'].color,
                        "position" : [7,7]
                    }],
                "current_player" : 1,
                "code" : 0
            }
            return render(request, 'game/new_game.html', game_state)

        return HttpResponse("KO")

    game_state = {
        "game_id" : 11,
        "board" : [[1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,2]],
        "players" : [{
                "id" :  10,
                "name" : "Alice",
                "color" : "cyan",
                "position" : [0,0]
            },{
                "id" :  20,
                "name" : "Bob",
                "color" : "orange",
                "position" : [7,7]
            }],
        "current_player" : 1,
        "code" : 0
    }

    return HttpResponse(json.dumps(game_state))