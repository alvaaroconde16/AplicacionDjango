from rest_framework import serializers
from .models import *
from datetime import datetime


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
    destino = DestinoSerializer(many=True)
    
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
        
        

#Serializer para Reserva Create
class ReservaSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Reserva
        fields = [
            'codigo_reserva', 'fecha_salida', 'fecha_llegada',
            'numero_personas', 'precio', 'usuario'
        ]

    def validate_codigo_reserva(self, codigo_reserva):
        reserva_existente = Reserva.objects.filter(codigo_reserva=codigo_reserva).first()
        if reserva_existente:
            if self.instance and reserva_existente.id == self.instance.id:
                pass
            else:
                raise serializers.ValidationError('Ya existe una reserva con este código')
        return codigo_reserva

    def validate_fecha_salida(self, fecha_salida):
        if fecha_salida < timezone.now():
            raise serializers.ValidationError('La fecha de salida no puede ser en el pasado')
        return fecha_salida

    
    def validate_fecha_llegada(self, fecha_llegada):
        fecha_salida_str = self.initial_data.get('fecha_salida')

        # Convertir el string a datetime (si viene en formato de fecha)
        try:
            fecha_salida = datetime.strptime(fecha_salida_str, "%Y-%m-%d")  # Asegura que coincida con el formato que estás usando
            fecha_salida = timezone.make_aware(fecha_salida)  # Lo hacemos timezone-aware
        except (ValueError, TypeError):
            raise serializers.ValidationError('Formato de fecha inválido para fecha de salida')

        # Ahora sí podemos comparar
        if fecha_llegada <= fecha_salida:
            raise serializers.ValidationError('La fecha de llegada debe ser después de la fecha de salida')

        return fecha_llegada

    def validate_numero_personas(self, numero_personas):
        if numero_personas < 1:
            raise serializers.ValidationError('Debe haber al menos una persona en la reserva')
        return numero_personas

    def create(self, validated_data):
        reserva = Reserva.objects.create(**validated_data)
        return reserva

    def update(self, instance, validated_data):
        instance.codigo_reserva = validated_data.get('codigo_reserva', instance.codigo_reserva)
        instance.fecha_salida = validated_data.get('fecha_salida', instance.fecha_salida)
        instance.fecha_llegada = validated_data.get('fecha_llegada', instance.fecha_llegada)
        instance.numero_personas = validated_data.get('numero_personas', instance.numero_personas)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.usuario = validated_data.get('usuario', instance.usuario)
        instance.save()
        
        return instance