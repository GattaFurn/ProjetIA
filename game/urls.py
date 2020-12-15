from django.urls import path

from . import views,business,ia,training

urlpatterns = [
    path('', views.index, name='index'), #décide de la page a renvoyer via les views
    path('move', business.index),
    path('training',training.training)
] 