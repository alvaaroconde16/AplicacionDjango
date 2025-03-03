from django.urls import path

from .api_views import *

urlpatterns = [
    path('usuarios', usuario_list),
    path('reservas', reserva_list),
    path('reservasMejoradas', reservaMejorada_list),
    path('alojamientosMejorados', alojamientoMejorado_list),
    path('transportesMejorados', transporteMejorado_list),
    path('extrasMejorados', extraMejorado_list),
    path('destinos', destino_list),
    path('transportes', transporte_list),
    path('extras', extra_list),
    
    # Rutas para los get    
    path('reservas/busqueda_simple',reserva_buscar),
    path('reservas/busqueda_avanzada',reserva_buscar_avanzado),
    path('usuarios/busqueda_avanzada',usuario_buscar_avanzado),
    path('destinos/busqueda_avanzada',destino_buscar_avanzado),
    path('comentarios/busqueda_avanzada',comentario_buscar_avanzado),
    path('alojamientos/busqueda_avanzada',alojamiento_buscar_avanzado),
    
    # Rutas para los post
    path('reservas/crear',reserva_create),
    path('usuarios/crear',usuario_create),
    path('transportes/crear',transporte_create),
    path('extras/crear',extra_create),
    
    # Rutas para los put
    path('reservas/editar/<int:reserva_id>',reserva_editar),
    path('reservas/<int:reserva_id>',reserva_obtener),
    path('usuarios/editar/<int:usuario_id>',usuario_editar),
    path('usuarios/<int:usuario_id>',usuario_obtener),
    path('transportes/editar/<int:transporte_id>',transporte_editar),
    path('transportes/<int:transporte_id>',transporte_obtener),
    path('extras/editar/<int:extra_id>',extra_editar),
    path('extras/<int:extra_id>',extra_obtener),

    # Rutas para los patch
    path('reservas/actualizar/codigo/<int:reserva_id>', reserva_actualizar_codigo),
    path('usuarios/actualizar/nombre/<int:usuario_id>', usuario_actualizar_nombre),
    path('transportes/actualizar/capacidad/<int:transporte_id>', transporte_actualizar_capacidad),
    path('extras/actualizar/nombre/<int:extra_id>', extra_actualizar_nombre),

    # Rutas para los delete
    path('reservas/eliminar/<int:reserva_id>', reserva_eliminar),
    path('usuarios/eliminar/<int:usuario_id>', usuario_eliminar),
    path('transportes/eliminar/<int:transporte_id>', transporte_eliminar),
    path('extras/eliminar/<int:extra_id>', extra_eliminar),

    path('registrar/usuario',registrar_usuario.as_view()),
    path('usuario/token/<str:token>',obtener_usuario_token)
]