from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import redirect
from .models import User
from game.models import Player,IA,Game
from django.core.exceptions import ObjectDoesNotExist
import json
from statistics import mean

#iterables
COLOR_CHOICES = ( 
    ('PK', "Pink"),
    ('YW', 'Yellow'),
    ('GN', 'Green'),
    ('VT', 'Violet'),
    ('RD', 'Red'),
    ('OE', 'Orange'),
    ('CN', 'Cyan'),
)

IA_CHOICES = (("Nitron", "Nitron - Easy"),("Torton","Torton - Medium"),("Vatron", "Vatron - Difficult"))

class ConnectionFormPlayer(forms.Form):
    username = forms.CharField(label ="Username", max_length=50)
    password = forms.CharField(label="Password", max_length=20, widget=forms.PasswordInput())

class ConnectionFormNewPlayer(forms.Form):
    username = forms.CharField(label = "Username", max_length=50)
    password = forms.CharField(label= "Password", max_length=20, widget=forms.PasswordInput())
    color_choice = forms.ChoiceField(label="Your color", choices=COLOR_CHOICES)

class ConnectionFormIA(forms.Form):
    ia_choice = forms.ChoiceField(label="Your_IA",choices = IA_CHOICES)

def index(request):
    if request.method == "GET": # get connection page
        form_player = ConnectionFormPlayer() # empty form
        form_new_player = ConnectionFormNewPlayer()
        form_IA = ConnectionFormIA()
        if(request.session.get("player1",None) != None and request.session.get("player2",None) != None):
            return redirect('../game')
        if(request.session.get("active",False) == False):
            request.session["active"] = True
            request.session["player1"] = None
            request.session["player2"] = None
        return render(request, "connection/index.html", { "form_player": form_player , "form_new_player": form_new_player,"form_IA":form_IA})

    if request.method == "POST": # post a connection
        username = request.POST.get("username") #auto fill form with info in POST
        password = request.POST.get("password")
        color_choice = request.POST.get("color_choice")
        ia_choice = request.POST.get("ia_choice")
        if(color_choice == None):
            try:
                if(password == None):
                    ia = IA.objects.get(pseudo = ia_choice)
                    ia_player = Player.objects.get(ia = ia)
                    user = {"id":ia_player.id,"username":ia.pseudo,"color":ia.color,"type":"IA","eps":ia.eps}
                else: 
                    user = User.objects.get(pseudo = username, password = password)
                    player = Player.objects.get(user = user)
                    user = {"id":player.id,"username":user.pseudo,"color":user.color,"type":"User"}
                    
                if(request.session.get('player1') == None):
                    request.session['player1'] = user
                    return redirect('../game')
                else:
                    if(request.session['player1'].get("id") == user.get("id")):
                        data = "The player has already been selected"
                        return reconnection(request,data)
                    if(request.session['player1'].get("type") == "IA" and request.session['player1'].get("type") == user["type"]):
                        data = "One AI has already been selected"
                        return reconnection(request,data)
                    request.session['player2'] = user
                return redirect('../game')
            except ObjectDoesNotExist:
                data = "The player does not exist or the username/password is incorrect."
                return reconnection(request,data)
        else:
            try:
                user = User.objects.get(pseudo = username)
                data = "The user already exists"
                return reconnection(request,data)
            except ObjectDoesNotExist:
               
                data = "The player has been created, please log in now!"
                
                new_user = User.objects.create(pseudo = username, password = password, color = color_choice)
                Player.objects.create(user = new_user)
                return reconnection(request,data)


def deconnection(request):
    request.session["active"] = False
    request.session["player1"] = None
    request.session["player2"] = None
    return redirect('../connection')

def statistics(request):
    ia = Player.objects.filter(user__isnull = True)
    player = Player.objects.filter(ia__isnull = True)
    nb_game_played = Game.objects.count()
    nb_Ia_Game = Game.objects.filter(player2__in=ia).count()
    nb_player_game = Game.objects.filter(player2__in=player).count()

    time_in_minute = Game.objects.values('time')
    time_in_minute = [(entry["time"].hour*3600 + entry["time"].minute*60 + entry["time"].second) for entry in time_in_minute]
    average_time = mean(time_in_minute)
    max_time = max(time_in_minute)
    min_time = min(time_in_minute)

    box_taken = Game.objects.values('player1_box_total','player2_box_total')
    box_taken_area = [entry["max_box_taken_with_area"] for entry in Game.objects.values('max_box_taken_with_area')]
    box_taken = [entry["player1_box_total"] for entry in box_taken]+[entry["player2_box_total"] for entry in box_taken]
    total_box_taken = sum(box_taken)
    max_box_taken = max(box_taken_area)
    average_box_taken = mean(box_taken)
    return render(request,"connection/statistics.html",{ "nb_game_played":nb_game_played,"nb_Ia_Game": nb_Ia_Game , "nb_player_game": nb_player_game,"average_time":average_time,"max_time":max_time,"min_time":min_time,"total_box_taken":total_box_taken,"max_box_taken":max_box_taken,"average_box_taken":average_box_taken})

def reconnection(request,data):
    return render(request, "connection/index.html", { "data":data,"form_player": ConnectionFormPlayer() , "form_new_player": ConnectionFormNewPlayer(),"form_IA":ConnectionFormIA()})


