from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from django.shortcuts import redirect

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

class ConnectionFormPlayer (forms.Form):
    username = forms.CharField(label = "Username", max_length=50)
    password = forms.CharField(label="Password", max_length=20, widget=forms.PasswordInput())

class ConnectionFormNewPlayer(forms.Form):
    username = forms.CharField(label = "Username", max_length=50)
    password = forms.CharField(label="Password", max_length=20, widget=forms.PasswordInput())
    colorchoice = forms.ChoiceField(label="Your color", choices=COLOR_CHOICES)



def index(request):
    if request.method == "GET": # get connection page
        formPlayer = ConnectionFormPlayer() # empty form
        formNewPlayer = ConnectionFormNewPlayer()
        return render(request, "connection/index.html", { "formPlayer": formPlayer , "formNewPlayer": formNewPlayer})

    if request.method == "POST": # post a connection
        formPlayer = ConnectionFormPlayer(request.POST) #auto fill form with info in POST
        
        if formPlayer.is_valid():
            # Check credentials
            return HttpResponseRedirect('/game')
        return HttpResponse("KO")