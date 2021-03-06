from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('deconnection', views.deconnection, name='deconnection'),
    path('statistics', views.statistics, name='statistics'),
]