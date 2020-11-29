from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json

from django import forms
import random
 

class NewGameForm(forms.Form):
    player1_name = forms.CharField(label="Player name:",widget=forms.HiddenInput())
    player1_color = forms.CharField(label="Player Color:",widget=forms.HiddenInput())
    player2_name = forms.CharField(label="Player name:",widget=forms.HiddenInput())
    player2_color = forms.CharField(label="Player Color:",widget=forms.HiddenInput())

def index(request):
    if request.method == "GET": #quand c'est la premiere fois qu'on vient
        form = NewGameForm()
        form.fields["player1_name"].initial= request.session['player1'].get("username")
        form.fields["player1_color"].initial = request.session['player1'].get("color")
        if(request.session['player2'] == None):
            return render(request, "game/index.html", { "form": form ,"player1":request.session['player1'],"player2":None})
        else:
            form.fields["player2_name"].initial= request.session['player2'].get("username")
            form.fields["player2_color"].initial = request.session['player2'].get("color")
            return render(request, "game/index.html", { "form": form ,"player1":request.session['player1'],"player2":request.session['player2']})

    if request.method == "POST": #quand on a les noms des joueurs pour commencer la partie
        form = NewGameForm(request.POST)
        if form.is_valid():
            game_state = {
                "game_id" : 11,
                "board" : [[1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,2]],
                "players" : [request.session['player1'],request.session['player2']],
                "current_player" : 1,
                "code" : 0
            }
            return render(request, 'game/new_game.html',{"game_state":game_state})

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