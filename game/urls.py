from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'), #décide de la page a renvoyer via les views
    path('move', views.apply_move)
]