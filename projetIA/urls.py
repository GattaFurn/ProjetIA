from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('connection.urls')),
    path('connection/', include('connection.urls')),
    path('game/', include('game.urls')),
]
