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


# Serializer para Extra Mejorado
class ExtraMejoradoSerializer(serializers.ModelSerializer):
    reserva = ReservaSerializer(many=True)
    
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
    
    

class UsuarioSerializerCreate(serializers.ModelSerializer):

    class Meta:
        model = Usuario
        fields = [
            'nombre', 'correo', 'telefono', 'edad',
            'contraseña', 'fecha_registro', 'imagen'
        ]

    def validate_correo(self, correo):
        # Verifica si ya existe un usuario con el mismo correo
        usuario_existente = Usuario.objects.filter(correo=correo).first()
        if usuario_existente:
            if self.instance and usuario_existente.id == self.instance.id:
                pass
            else:
                raise serializers.ValidationError('Ya existe un usuario con este correo electrónico')
        return correo

    def validate_telefono(self, telefono):
        # Verifica que el teléfono tenga un formato válido (puedes ajustar esta expresión regular)
        if not telefono.isdigit() or len(telefono) < 9:
            raise serializers.ValidationError('El teléfono debe contener al menos 9 dígitos')
        return telefono

    def validate_edad(self, edad):
        if edad < 18:
            raise serializers.ValidationError('Debe ser mayor de 18 años para registrarse')
        return edad

    def validate_fecha_registro(self, fecha_registro):
        if fecha_registro is None:
            raise serializers.ValidationError('La fecha de registro es obligatoria')

        if fecha_registro > timezone.now().date():
            raise serializers.ValidationError('La fecha de registro no puede ser en el futuro')
    
        return fecha_registro

    def validate_contraseña(self, contraseña):
        # Asegura que la contraseña tenga al menos 8 caracteres
        if len(contraseña) < 8:
            raise serializers.ValidationError('La contraseña debe tener al menos 8 caracteres')
        return contraseña

    def update(self, instance, validated_data):
        # Actualizar los datos de un usuario
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.correo = validated_data.get('correo', instance.correo)
        instance.telefono = validated_data.get('telefono', instance.telefono)
        instance.edad = validated_data.get('edad', instance.edad)
        instance.fecha_registro = validated_data.get('fecha_registro', instance.fecha_registro)
        instance.contraseña = validated_data.get('contraseña', instance.contraseña)
        instance.save()

        return instance
    
    
class TransporteSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Transporte
        fields = ['tipo', 'capacidad', 'disponible', 'costo_por_persona', 'destino']

    def validate_tipo(self, tipo):
        if not tipo or len(tipo.strip()) == 0:
            raise serializers.ValidationError("El tipo de transporte es obligatorio")
    
    # Verifica si ya existe un transporte con el mismo tipo
        transporte_existente = Transporte.objects.filter(tipo=tipo).first()
        if transporte_existente:
            if self.instance and transporte_existente.id == self.instance.id:
                pass
            else:
                raise serializers.ValidationError('Ya existe un transporte de ese tipo')
        return tipo


    def validate_capacidad(self, capacidad):
        if capacidad < 1:
            raise serializers.ValidationError("La capacidad debe ser al menos 1")
        return capacidad

    def validate_costo_por_persona(self, costo_por_persona):
        if costo_por_persona < 0:
            raise serializers.ValidationError("El costo por persona no puede ser negativo")
        return costo_por_persona
    
    def validate_destino(self, destino):
        if not destino:
            raise serializers.ValidationError("Debe seleccionar al menos un destino")
        return destino
    

    def update(self, instance, validated_data):
        instance.tipo = validated_data.get('tipo', instance.tipo)
        instance.capacidad = validated_data.get('capacidad', instance.capacidad)
        instance.disponible = validated_data.get('disponible', instance.disponible)
        instance.costo_por_persona = validated_data.get('costo_por_persona', instance.costo_por_persona)

        # Para manejar la relación many-to-many con destinos
        if 'destino' in validated_data:
            instance.destino.set(validated_data['destino'])

        instance.save()
        return instance


class ExtraSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = ['nombre', 'tipo', 'descripcion', 'precio', 'reserva']

    def validate_nombre(self, nombre):
        if not nombre or len(nombre.strip()) == 0:
            raise serializers.ValidationError("El nombre del extra es obligatorio")
        
        # Verifica si ya existe un extra con el mismo nombre
        extra_existente = Extra.objects.filter(nombre=nombre).first()
        if extra_existente:
            if self.instance and extra_existente.id == self.instance.id:
                pass
            else:
                raise serializers.ValidationError('Ya existe un extra con este nombre')

        return nombre

    def validate_tipo(self, tipo):
        if tipo not in dict(Extra.TIPOS_EXTRAS).keys():
            raise serializers.ValidationError("El tipo de extra no es válido")
        return tipo

    def validate_precio(self, precio):
        if precio < 0:
            raise serializers.ValidationError("El precio no puede ser negativo")
        return precio

    def validate_reserva(self, reserva):
        if not reserva:
            raise serializers.ValidationError("Debe seleccionar al menos una reserva")
        return reserva

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.tipo = validated_data.get('tipo', instance.tipo)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.precio = validated_data.get('precio', instance.precio)

        # Para manejar la relación many-to-many con reservas
        if 'reserva' in validated_data:
            instance.reserva.set(validated_data['reserva'])

        instance.save()
        return instance

    

#######################################################################################################################################################################


class ReservaSerializerActualizarCodigo(serializers.ModelSerializer):
    
    class Meta:
        model = Reserva
        fields = [
            'codigo_reserva'
        ]

    def validate_codigo_reserva(self, codigo_reserva):
        reserva_existente = Reserva.objects.filter(codigo_reserva=codigo_reserva).first()
        if reserva_existente:
            if self.instance and reserva_existente.id == self.instance.id:
                pass
            else:
                raise serializers.ValidationError('Ya existe una reserva con este código')
        return codigo_reserva
    

class UsuarioSerializerActualizarNombre(serializers.ModelSerializer):
    
    class Meta:
        model = Usuario
        fields = [
            'nombre'
        ]

    def validate_nombre(self, nombre):
        usuario_existente = Usuario.objects.filter(nombre=nombre).first()
        if usuario_existente:
            if self.instance and usuario_existente.id == self.instance.id:
                pass
            else:
                raise serializers.ValidationError('Ya existe usuario con este nombre')
        return nombre
    

class TransporteSerializerActualizarCapacidad(serializers.ModelSerializer):
    
    class Meta:
        model = Transporte
        fields = [
            'capacidad',
            'tipo'
        ]

    def validate_capacidad(self, capacidad):
        if capacidad < 1:
            raise serializers.ValidationError("La capacidad debe ser al menos 1")
        return capacidad
    

    def validate_nombre(self, tipo):
        transporte_existente = Transporte.objects.filter(tipo=tipo).first()
        if transporte_existente:
            if self.instance and transporte_existente.id == self.instance.id:
                pass
            else:
                raise serializers.ValidationError('Ya existe transporte de ese tipo')
        return tipo
    

class ExtraSerializerActualizarNombre(serializers.ModelSerializer):
    
    class Meta:
        model = Extra
        fields = [
            'nombre'
        ]

    def validate_nombre(self, nombre):
        extra_existente = Extra.objects.filter(nombre=nombre).first()
        if extra_existente:
            if self.instance and extra_existente.id == self.instance.id:
                pass
            else:
                raise serializers.ValidationError('Ya existe extra con este nombre')
        return nombre