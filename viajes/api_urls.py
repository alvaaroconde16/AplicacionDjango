from django.urls import path

from .api_views import *

urlpatterns = [
    path('usuarios', usuario_list),
    path('reservas', reserva_list),
    path('reservasMejoradas', reservaMejorada_list),
]