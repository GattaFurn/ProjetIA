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
    ("BL", "Blue"),
    ("PK", "Pink"),
    ('YW', 'Yellow'),
    ('GN', 'Green'),
    ('VT', 'Violet'),
    ('RD', 'Red'),
    ('OE', 'Orange'),
    ('CN', 'Cyan'),
)

IA_CHOICES = (("None", "Null"),("Torton", "Torton"))

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
                    user = {"id":ia.id,"username":ia.pseudo,"color":ia.color,"st":[],"atp1": 0, "at": 0,"position":[],"box_taken":0,"Q_table":ia.Q_table}
                else: 
                    utilisateur = Utilisateur.objects.get(pseudo = username, password = password)
                    user = {"id":utilisateur.id,"username":utilisateur.pseudo,"color":utilisateur.color,"st": [],"position":[],"box_taken":0,}
                if(request.session.get('player1') == None):
                    user["st"] = [0,0]
                    user["position"] = [0,0]
                    request.session['player1'] = user
                    return redirect('../game')
                else:
                    user["st"] = [7,7]
                    user["position"] = [7,7]
                    request.session['player2'] = user
                    if(request.session['player1'].get("id") == request.session['player2'].get("id")):
                        data = "Le joueur a déjà été selectionné"
                        formPlayer = ConnectionFormPlayer() # empty form
                        formNewPlayer = ConnectionFormNewPlayer()
                        return render(request, "connection/index.html", { "data":data,"formPlayer": formPlayer , "formNewPlayer": formNewPlayer,"formIA":ConnectionFormIA})
                return redirect('../game')
            except ObjectDoesNotExist:
                return HttpResponse("KO")
        else:
            try:
                utilisateur = Utilisateur.objects.get(pseudo = username)
                return HttpResponse("L'utilisateur existe déjà")
            except ObjectDoesNotExist:
               
                data = "Le joueur à bien été crée, veuillez vous connectez maintenant!"
                
                new_utilisateur = Utilisateur.objects.create(pseudo = username, password = password, color = colorchoice)
                Player.objects.create(utilisateur = new_utilisateur)
                formPlayer = ConnectionFormPlayer() # empty form
                formNewPlayer = ConnectionFormNewPlayer()
                return render(request, "connection/index.html", { "data":data,"formPlayer": formPlayer , "formNewPlayer": formNewPlayer,"formIA":ConnectionFormIA})

def deconnection(request):
    request.session["active"] = False
    request.session["player1"] = None
    request.session["player2"] = None
    return redirect('../connection')

