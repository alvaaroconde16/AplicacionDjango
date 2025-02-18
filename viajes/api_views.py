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
    # Si hay parámetros en la query
    if len(request.query_params) > 0:
        formulario = BusquedaReservaForm(request.query_params)
        
        if formulario.is_valid():
            # Obtener los datos del formulario
            codigo_reserva = formulario.cleaned_data.get('codigo_reserva')
            fecha = formulario.cleaned_data.get('fecha')
            numero_personas = formulario.cleaned_data.get('numero_personas')

            # Si todos los campos están vacíos, devolver un error
            if not codigo_reserva and not fecha and not numero_personas:
                return Response({"error": "Debe proporcionar al menos un parámetro de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)

            # Construir la QuerySet inicial
            QSreservas = Reserva.objects.all()

            # Filtros por código de reserva
            if codigo_reserva:
                QSreservas = QSreservas.filter(codigo_reserva__icontains=codigo_reserva)

            # Filtro por fecha
            if fecha:
                QSreservas = QSreservas.filter(fecha_salida__date=fecha)

            # Filtro por número de personas
            if numero_personas:
                QSreservas = QSreservas.filter(numero_personas=numero_personas)

            # Serializar los resultados
            reservas = QSreservas.all()
            serializer = ReservaSerializerMejorado(reservas, many=True)
            return Response(serializer.data)

        else:
            # Si el formulario no es válido, devolvemos los errores del formulario
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        # Si no hay parámetros en la query
        return Response({"error": "Debe proporcionar al menos un parámetro de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def usuario_buscar_avanzado(request):
    if len(request.query_params) > 0:  # Si hay parámetros en la query
        formulario = BusquedaUsuarioForm(request.query_params)
        
        if formulario.is_valid():
            # Obtener los datos del formulario
            nombre = formulario.cleaned_data.get('nombre')
            correo = formulario.cleaned_data.get('correo')
            edad = formulario.cleaned_data.get('edad')

            # Construir la QuerySet inicial de usuarios
            QSusuarios = Usuario.objects.all()

            # Filtro por nombre
            if nombre:
                QSusuarios = QSusuarios.filter(nombre__icontains=nombre)

            # Filtro por correo
            if correo:
                QSusuarios = QSusuarios.filter(correo__icontains=correo)

            # Filtro por edad
            if edad is not None:
                QSusuarios = QSusuarios.filter(edad=edad)

            # Serializar los resultados
            usuarios = QSusuarios.all()
            serializer = UsuarioSerializer(usuarios, many=True)  # Asumiendo que tienes un serializer para Usuario
            return Response(serializer.data)

        else:
            # Si el formulario no es válido, retornamos los errores
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        # Si no hay parámetros en la query
        return Response({"error": "Debe proporcionar al menos un parámetro de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def destino_buscar_avanzado(request):
    if len(request.query_params) > 0:  # Si hay parámetros en la query
        formulario = BusquedaDestinoForm(request.query_params)
        
        if formulario.is_valid():
            # Obtener los datos del formulario
            nombre = formulario.cleaned_data.get('nombre')
            pais = formulario.cleaned_data.get('pais')
            popularidad = formulario.cleaned_data.get('popularidad')

            # Construir la QuerySet inicial
            QSdestinos = Destino.objects.all()

            # Filtro por nombre del destino
            if nombre:
                QSdestinos = QSdestinos.filter(nombre__icontains=nombre)

            # Filtro por país
            if pais:
                QSdestinos = QSdestinos.filter(pais__icontains=pais)

            # Filtro por popularidad
            if popularidad is not None:
                QSdestinos = QSdestinos.filter(popularidad__gte=popularidad)

            # Serializar los resultados
            destinos = QSdestinos.all()
            serializer = DestinoSerializer(destinos, many=True)
            return Response(serializer.data)

        else:
            # Si el formulario no es válido, retornamos los errores
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        # Si no hay parámetros en la query
        return Response({"error": "Debe proporcionar al menos un parámetro de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def comentario_buscar_avanzado(request):
    if len(request.query_params) > 0:  # Si hay parámetros en la query
        formulario = BusquedaComentarioForm(request.query_params)
        
        if formulario.is_valid():
            # Obtener los datos del formulario
            titulo = formulario.cleaned_data.get('titulo')
            contenido = formulario.cleaned_data.get('contenido')
            calificacion = formulario.cleaned_data.get('calificacion')

            # Construir la QuerySet inicial
            QScomentarios = Comentario.objects.all()

            # Filtros por título
            if titulo:
                QScomentarios = QScomentarios.filter(titulo__icontains=titulo)

            # Filtro por contenido
            if contenido:
                QScomentarios = QScomentarios.filter(contenido__icontains=contenido)

            # Filtro por calificación
            if calificacion is not None:
                QScomentarios = QScomentarios.filter(calificacion__gte=calificacion)


            # Serializar los resultados
            comentarios = QScomentarios.all()
            serializer = ComentarioSerializer(comentarios, many=True)
            return Response(serializer.data)

        else:
            # Si el formulario no es válido, retornamos los errores
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        # Si no hay parámetros en la query
        return Response({"error": "Debe proporcionar al menos un parámetro de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def alojamiento_buscar_avanzado(request):
    if len(request.query_params) > 0:  # Si hay parámetros en la query
        formulario = BusquedaAlojamientoForm(request.query_params)

        if formulario.is_valid():
            # Obtener los datos del formulario
            nombre = formulario.cleaned_data.get('nombre')
            tipo = formulario.cleaned_data.get('tipo')
            capacidad = formulario.cleaned_data.get('capacidad')

            # Construir la QuerySet inicial
            QSalojamientos = Alojamiento.objects.all()

            # Filtros por nombre del alojamiento
            if nombre:
                QSalojamientos = QSalojamientos.filter(nombre__icontains=nombre)

            # Filtros por tipo de alojamiento
            if tipo:
                QSalojamientos = QSalojamientos.filter(tipo__icontains=tipo)

            # Filtros por capacidad mínima
            if capacidad:
                QSalojamientos = QSalojamientos.filter(capacidad__gte=capacidad)

            # Serializar los resultados
            alojamientos = QSalojamientos.all()
            serializer = AlojamientoMejoradoSerializer(alojamientos, many=True)
            return Response(serializer.data)

        else:
            # Si el formulario no es válido, retornamos los errores
            return Response(formulario.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        # Si no hay parámetros en la query
        return Response({"error": "Debe proporcionar al menos un parámetro de búsqueda."}, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def reserva_list(request):
    reservas = Reserva.objects.all()
    serializer = ReservaSerializer(reservas, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def usuario_list(request):
    usuarios = Usuario.objects.all()
    serializer = UsuarioSerializer(usuarios, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def reserva_create(request):
    print(request.data)
    reservaCreateSerializer = ReservaSerializerCreate(data=request.data)
    if reservaCreateSerializer.is_valid():
        try:
            reservaCreateSerializer.save()
            return Response("Reserva CREADA")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(reservaCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['GET'])
def reserva_obtener(request, reserva_id):
    try:
        # Obtener la reserva por ID
        reserva = Reserva.objects.get(id=reserva_id)
    except Reserva.DoesNotExist:
        return Response({'error': 'Reserva no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    # Serializar la reserva
    serializer = ReservaSerializerMejorado(reserva)
    return Response(serializer.data)

    
@api_view(['PUT'])
def reserva_editar(request, reserva_id):
    # Buscar la reserva a actualizar
    reserva = Reserva.objects.get(id=reserva_id)

    # Pasar la instancia al serializer
    reservaCreateSerializer = ReservaSerializerCreate(data=request.data, instance=reserva)

    if reservaCreateSerializer.is_valid():
        try:
            reservaCreateSerializer.save()
            return Response("Reserva EDITADA")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(reservaCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)