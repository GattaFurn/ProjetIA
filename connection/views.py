from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import redirect
from .models import Utilisateur
from django.core.exceptions import ObjectDoesNotExist

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

class ConnectionFormPlayer(forms.Form):
    username = forms.CharField(label ="Username", max_length=50)
    password = forms.CharField(label="Password", max_length=20, widget=forms.PasswordInput())

class ConnectionFormNewPlayer(forms.Form):
    username = forms.CharField(label = "Username", max_length=50)
    password = forms.CharField(label= "Password", max_length=20, widget=forms.PasswordInput())
    colorchoice = forms.ChoiceField(label="Your color", choices=COLOR_CHOICES)



def index(request):
    if request.method == "GET": # get connection page
        formPlayer = ConnectionFormPlayer() # empty form
        formNewPlayer = ConnectionFormNewPlayer()
        
        request.session["player1"] = None
        request.session["player2"] = None
        return render(request, "connection/index.html", { "formPlayer": formPlayer , "formNewPlayer": formNewPlayer})

    if request.method == "POST": # post a connection
        username = request.POST.get("username") #auto fill form with info in POST
        password = request.POST.get("password")
        colorchoice = request.POST.get("colorchoice")
        if(colorchoice == None):
            try:
                utilisateur = Utilisateur.objects.get(pseudo = username, password = password)
                if(request.session.get('player1') == None):
                    request.session['player1'] = {"username":utilisateur.pseudo,"color":utilisateur.color}
                    return redirect('../game')
                else:
                    request.session['player2'] = {"username":utilisateur.pseudo,"color":utilisateur.color}
                return redirect('../game')
            except ObjectDoesNotExist:
                return HttpResponse("KO")
        else:
            try:
                utilisateur = Utilisateur.objects.get(pseudo = username)
                return HttpResponse("L'utilisateur existe déjà")
            except ObjectDoesNotExist:
                #script = "alert('Le joueur à bien été crée, veuillez vous connectez maintenant');"
                js_data = "Le joueur à bien été crée, veuillez vous connectez maintenant"
                new_utilisateur = Utilisateur.objects.create(pseudo = username, password = password, color = colorchoice)
                
                formPlayer = ConnectionFormPlayer() # empty form
                formNewPlayer = ConnectionFormNewPlayer()
                return render(request, "connection/index.html", { "my_data":js_data, "formPlayer": formPlayer , "formNewPlayer": formNewPlayer})
        

