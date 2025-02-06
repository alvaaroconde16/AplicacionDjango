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
    if len(request.query_params) > 0:  # Si hay parámetros en la query
        formulario = BusquedaReservaForm(request.query_params)
        
        if formulario.is_valid():
            # Obtener los datos del formulario
            codigo_reserva = formulario.cleaned_data.get('codigo_reserva')
            fecha = formulario.cleaned_data.get('fecha')
            numero_personas = formulario.cleaned_data.get('numero_personas')

            # Construir la QuerySet inicial
            QSreservas = Reserva.objects.all()

            # Filtros por código de reserva
            if codigo_reserva:
                QSreservas = QSreservas.filter(codigo_reserva__icontains=codigo_reserva)

            # Filtro por fecha
            if fecha:
                QSreservas = QSreservas.filter(fecha=fecha)

            # Filtro por número de personas
            if numero_personas:
                QSreservas = QSreservas.filter(numero_personas=numero_personas)

            # Serializar los resultados
            reservas = QSreservas.all()
            serializer = ReservaSerializerMejorado(reservas, many=True)
            return Response(serializer.data)

        else:
            # Si el formulario no es válido, retornamos los errores
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        # Si no hay parámetros en la query
        return Response({"error": "Debe proporcionar al menos un parámetro de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)