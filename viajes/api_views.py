from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import *


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