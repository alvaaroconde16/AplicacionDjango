from django.urls import path

from .api_views import *

urlpatterns = [
    path('usuarios', usuario_list),
    path('reservas', reserva_list),
    path('reservasMejoradas', reservaMejorada_list),
    path('alojamientosMejorados', alojamientoMejorado_list),
    path('transportesMejorados', transporteMejorado_list),
    
    path('reservas/busqueda_simple',reserva_buscar),
    path('reservas/busqueda_avanzada',reserva_buscar_avanzado),
    path('usuarios/busqueda_avanzada',usuario_buscar_avanzado),
    path('destinos/busqueda_avanzada',destino_buscar_avanzado),
    path('comentarios/busqueda_avanzada',comentario_buscar_avanzado),
    path('alojamientos/busqueda_avanzada',alojamiento_buscar_avanzado),
    
    path('reservas/crear',reserva_create),
    
    path('reservas/editar/<int:reserva_id>',reserva_editar),
    path('reservas/<int:reserva_id>',reserva_obtener),
]