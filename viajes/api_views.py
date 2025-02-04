from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *
from django.db.models import Q
from rest_framework import status


@api_view(['GET'])
def usuario_list(request):
    
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def reserva_list(request):
    
    reservas = Reserva.objects.all()
    serializer = ReservaSerializer(reservas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def reservaMejorada_list(request):
    
    reservas = Reserva.objects.all()
    serializer = ReservaSerializerMejorado(reservas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def alojamientoMejorado_list(request):
    
    reservas = Alojamiento.objects.all()
    serializer = AlojamientoMejoradoSerializer(reservas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def transporteMejorado_list(request):
    
    transportes = Transporte.objects.all()
    serializer = TransporteMejoradoSerializer(transportes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def reserva_buscar(request):
    formulario = BusquedaReserva(request.query_params)
    
    if formulario.is_valid():
        texto = formulario.data.get('textoBusqueda')
        
        # Filtrar las reservas basadas en el texto ingresado
        reservas = Reserva.objects.select_related('usuario')  # Usamos select_related si 'usuario' es una relación ForeignKey
        reservas = reservas.filter(
            Q(codigo_reserva__contains=texto) |  # Buscar por código de reserva
            Q(usuario__nombre__contains=texto) |  # Buscar por el nombre del usuario (ajusta según tu modelo)
            Q(fecha_salida__icontains=texto) |   # Buscar por la fecha de salida
            Q(fecha_llegada__icontains=texto)    # Buscar por la fecha de llegada
        ).all()
        
        # Serializar las reservas encontradas
        serializer = ReservaSerializerMejorado(reservas, many=True)
        
        return Response(serializer.data)
    else:
        return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['GET'])
def reserva_buscar_avanzado(request):
    if len(request.query_params) > 0:
        formulario = BusquedaReservaForm(request.query_params)

        if formulario.is_valid():
            # Obtener los valores del formulario con valores por defecto si están vacíos
            codigo_reserva = formulario.cleaned_data.get('codigo_reserva')
            nombre_usuario = formulario.cleaned_data.get('nombre_usuario')
            fecha_salida = formulario.cleaned_data.get('fecha_salida')
            fecha_llegada = formulario.cleaned_data.get('fecha_llegada')
            numero_personas = formulario.cleaned_data.get('numero_personas')
            precio_desde = formulario.cleaned_data.get('precio_desde')
            precio_hasta = formulario.cleaned_data.get('precio_hasta')
            fecha_desde = formulario.cleaned_data.get('fecha_desde')
            fecha_hasta = formulario.cleaned_data.get('fecha_hasta')

            # Crear el queryset inicial
            reservas = Reserva.objects.all()

            # Filtrar por código de reserva si está presente
            if codigo_reserva:
                reservas = reservas.filter(codigo_reserva__contains=codigo_reserva)

            # Filtrar por nombre de usuario si está presente
            if nombre_usuario:
                reservas = reservas.filter(usuario__nombre__icontains=nombre_usuario)

            # Filtrar por fecha de salida si está presente
            if fecha_salida:
                reservas = reservas.filter(fecha_salida__date=fecha_salida)

            # Filtrar por fecha de llegada si está presente
            if fecha_llegada:
                reservas = reservas.filter(fecha_llegada__date=fecha_llegada)

            # Filtrar por número de personas si está presente
            if numero_personas:
                reservas = reservas.filter(numero_personas=numero_personas)

            # Filtrar por rango de precio si está presente
            if precio_desde is not None:
                reservas = reservas.filter(precio__gte=precio_desde)

            if precio_hasta is not None:
                reservas = reservas.filter(precio__lte=precio_hasta)

            # Filtrar por rango de fechas si está presente
            if fecha_desde:
                reservas = reservas.filter(fecha_salida__gte=fecha_desde)

            if fecha_hasta:
                reservas = reservas.filter(fecha_salida__lte=fecha_hasta)

            # Serializar los resultados
            serializer = ReservaSerializerMejorado(reservas, many=True)

            # Retornar los resultados de la búsqueda
            return Response(serializer.data)

        else:
            # Si el formulario no es válido, retornar los errores de validación
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        # Si no se pasan parámetros de búsqueda, retornar un error 400
        return Response({"error": "No se pasaron parámetros de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)