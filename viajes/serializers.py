from rest_framework import serializers
from .models import *


# Serializer para Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'



# Serializer para Cliente
class ClienteSerializer(serializers.ModelSerializer):

    fecha_registro = serializers.DateTimeField(format='%d-%m-%Y')

    class Meta:
        model = Cliente
        fields = '__all__'



# Serializer para Proveedor
class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'



# Serializer para Destino
class DestinoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destino
        fields = '__all__'



# Serializer para Reserva
class ReservaSerializer(serializers.ModelSerializer):
    
    fecha_salida = serializers.DateTimeField(format='%d-%m-%Y')
    fecha_llegada = serializers.DateTimeField(format='%d-%m-%Y')
    
    class Meta:
        model = Reserva
        fields = '__all__'



# Serializer para Reserva Mejorada
class ReservaSerializerMejorado(serializers.ModelSerializer):
    usuario = UsuarioSerializer()

    # Si necesitas formatear una fecha (por ejemplo, fecha_salida y fecha_llegada)
    fecha_salida = serializers.DateTimeField(format='%d-%m-%Y')
    fecha_llegada = serializers.DateTimeField(format='%d-%m-%Y')

    # Para mostrar cualquier campo adicional de la reserva
    class Meta:
        model = Reserva
        fields = '__all__'



# Serializer para Comentario
class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'



# Serializer para Alojamiento
class AlojamientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alojamiento
        fields = '__all__'
        
        
        
# Serializer para Alojamiento Mejorado
class AlojamientoMejoradoSerializer(serializers.ModelSerializer):
    destino = DestinoSerializer()
    
    class Meta:
        model = Alojamiento
        fields = '__all__'



# Serializer para Extra
class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = '__all__'



# Serializer para Pasaporte
class PasaporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pasaporte
        fields = '__all__'



# Serializer para Transporte
class TransporteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transporte
        fields = '__all__'
        
        

# Serializer para Transporte Mejorado
class TransporteMejoradoSerializer(serializers.ModelSerializer):
    destino = DestinoSerializer()
    
    class Meta:
        model = Transporte
        fields = '__all__'



# Serializer para Promocion
class PromocionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocion
        fields = '__all__'



# Serializer para Factura
class FacturaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Factura
        fields = '__all__'



# Serializer para ExtraReserva
class ExtraReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraReserva
        fields = '__all__'