from django.urls import path

from . import views
from . import business
from . import ia

urlpatterns = [
    path('', views.index, name='index'), #décide de la page a renvoyer via les views
    path('move', business.index),
] 