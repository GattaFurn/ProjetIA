from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import redirect
from .models import Utilisateur
from game.models import Player,IA
from django.core.exceptions import ObjectDoesNotExist
import json


#iterables
COLOR_CHOICES = (
    ('BL', "Blue"),
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
    colorchoice = forms.ChoiceField(label="Your color", choices=COLOR_CHOICES)

class ConnectionFormIA(forms.Form):
    ia_choice = forms.ChoiceField(label="Your_IA",choices = IA_CHOICES)

def index(request):
    if request.method == "GET": # get connection page
        formPlayer = ConnectionFormPlayer() # empty form
        formNewPlayer = ConnectionFormNewPlayer()
        FormIA = ConnectionFormIA()
        if(request.session.get("player1",None) != None and request.session.get("player2",None) != None):
            return redirect('../game')
        if(request.session.get("active",False) == False):
            request.session["active"] = True
            request.session["player1"] = None
            request.session["player2"] = None
        return render(request, "connection/index.html", { "formPlayer": formPlayer , "formNewPlayer": formNewPlayer,"formIA":ConnectionFormIA})

    if request.method == "POST": # post a connection
        username = request.POST.get("username") #auto fill form with info in POST
        password = request.POST.get("password")
        colorchoice = request.POST.get("colorchoice")
        iachoice = request.POST.get("ia_choice")
        if(colorchoice == None):
            try:
                if(password == None):
                    ia = IA.objects.get(pseudo = iachoice)
                    ia_player = Player.objects.get(ia = ia)
                    user = {"id":ia_player.id,"username":ia.pseudo,"color":ia.color,"type":"IA","eps":ia.eps}
                else: 
                    utilisateur = Utilisateur.objects.get(pseudo = username, password = password)
                    utilisateur_player = Player.objects.get(utilisateur = utilisateur)
                    user = {"id":utilisateur_player.id,"username":utilisateur.pseudo,"color":utilisateur.color,"type":"User"}
                if(request.session.get('player1') == None):
                    request.session['player1'] = user
                    return redirect('../game')
                else:
                    if(request.session['player1'].get("id") == user.get("id")):
                        data = "Le joueur a déjà été selectionné"
                        return reconnection_to_the_page(request,data)
                    if(request.session['player1'].get("type") == "IA" and request.session['player1'].get("type") == user["type"]):
                        data = "Une ia a déjà été selectionnée"
                        return reconnection_to_the_page(request,data)
                    request.session['player2'] = user
                return redirect('../game')
            except ObjectDoesNotExist:
                data = "Le joueur n'existe pas"
                return reconnection_to_the_page(request,data)
        else:
            try:
                utilisateur = Utilisateur.objects.get(pseudo = username)
                return HttpResponse("L'utilisateur existe déjà")
            except ObjectDoesNotExist:
               
                data = "Le joueur à bien été crée, veuillez vous connectez maintenant!"
                
                new_utilisateur = Utilisateur.objects.create(pseudo = username, password = password, color = colorchoice)
                Player.objects.create(utilisateur = new_utilisateur)
                return reconnection_to_the_page(request,data)


def deconnection(request):
    request.session["active"] = False
    request.session["player1"] = None
    request.session["player2"] = None
    return redirect('../connection')


def reconnection_to_the_page(request,data):
    formPlayer = ConnectionFormPlayer() # empty form
    formNewPlayer = ConnectionFormNewPlayer()
    return render(request, "connection/index.html", { "data":data,"formPlayer": formPlayer , "formNewPlayer": formNewPlayer,"formIA":ConnectionFormIA})


