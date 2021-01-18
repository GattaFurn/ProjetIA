from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from django.shortcuts import redirect


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
            player_creation(player1,1)
            player2 = request.session['player2'].copy()
            player_creation(player2,2)
            game_state = {
                "board" : [[1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,2]],
                "players" : [player1,player2],
                "current_player" : 0,
                "code" : 0,
                "time": "",
                "maxBoxTaken":1
            }
            return render(request, 'game/new_game.html',{"game_state":game_state})
    return redirect('../connection')

def player_creation(player,position):
    player["position"] = [0,0] if position == 1 else [7,7]
    if(player["type"] == "IA"):
        player["st"] = player["position"]
        player["stp1"] = 0
        player["atp1"] = player["at"] = 0
    player["box_taken"] = 0