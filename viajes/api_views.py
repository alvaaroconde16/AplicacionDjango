from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .forms import *
from django.db.models import Q
from rest_framework import status
from django.contrib.auth.models import Group
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.permissions import AllowAny
from oauth2_provider.models import AccessToken 
from oauth2_provider.contrib.rest_framework import OAuth2Authentication


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
def extraMejorado_list(request):
    
    extras = Extra.objects.all()
    serializer = ExtraMejoradoSerializer(extras, many=True)
    return Response(serializer.data)


#######################################################################################################################################################################


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
    
    
#######################################################################################################################################################################


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


@api_view(['GET'])
def destino_list(request):
    destinos = Destino.objects.all()
    serializer = DestinoSerializer(destinos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def transporte_list(request):
    transportes = Transporte.objects.all()
    serializer = TransporteSerializer(transportes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def extra_list(request):
    extras = Extra.objects.all()
    serializer = ExtraSerializer(extras, many=True)
    return Response(serializer.data)
    

#######################################################################################################################################################################


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


@api_view(['POST'])
def usuario_create(request):
    print(request.data)
    usuarioCreateSerializer = UsuarioSerializerCreate(data=request.data)
    if usuarioCreateSerializer.is_valid():
        try:
            usuarioCreateSerializer.save()
            return Response("Usuario CREADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(usuarioCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
def transporte_create(request):
    print(request.data)
    transporteCreateSerializer = TransporteSerializerCreate(data=request.data)

    if transporteCreateSerializer.is_valid():
        try:
            transporteCreateSerializer.save()
            return Response("Transporte CREADO", status=status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(transporteCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['POST'])
def extra_create(request):
    print(request.data)
    extraCreateSerializer = ExtraSerializerCreate(data=request.data)

    if extraCreateSerializer.is_valid():
        try:
            extraCreateSerializer.save()
            return Response("Extra CREADO", status=status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            print(repr(error))
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(extraCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


#######################################################################################################################################################################

    
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


@api_view(['GET'])
def usuario_obtener(request, usuario_id):
    try:
        # Obtener la reserva por ID
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Serializar la reserva
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)


@api_view(['GET'])
def transporte_obtener(request, transporte_id):
    try:
        # Obtener la reserva por ID
        transporte = Transporte.objects.get(id=transporte_id)
    except Transporte.DoesNotExist:
        return Response({'error': 'Transporte no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Serializar la reserva
    serializer = TransporteSerializer(transporte)
    return Response(serializer.data)


@api_view(['GET'])
def extra_obtener(request, extra_id):
    try:
        # Obtener la reserva por ID
        extra = Extra.objects.get(id=extra_id)
    except Extra.DoesNotExist:
        return Response({'error': 'Extra no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Serializar la reserva
    serializer = ExtraSerializer(extra)
    return Response(serializer.data)


#######################################################################################################################################################################

    
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
    

@api_view(['PUT'])
def usuario_editar(request, usuario_id):
    # Buscar el usuario a actualizar
    usuario = Usuario.objects.get(id=usuario_id)

    # Pasar la instancia al serializer
    usuarioCreateSerializer = UsuarioSerializerCreate(data=request.data, instance=usuario)

    if usuarioCreateSerializer.is_valid():
        try:
            usuarioCreateSerializer.save()
            return Response("Usuario EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(usuarioCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
def transporte_editar(request, transporte_id):
    # Buscar el usuario a actualizar
    transporte = Transporte.objects.get(id=transporte_id)

    # Pasar la instancia al serializer
    transporteCreateSerializer = TransporteSerializerCreate(data=request.data, instance=transporte)

    if transporteCreateSerializer.is_valid():
        try:
            transporteCreateSerializer.save()
            return Response("Transporte EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(transporteCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PUT'])
def extra_editar(request, extra_id):
    # Buscar el usuario a actualizar
    extra = Extra.objects.get(id=extra_id)

    # Pasar la instancia al serializer
    extraCreateSerializer = ExtraSerializerCreate(data=request.data, instance=extra)

    if extraCreateSerializer.is_valid():
        try:
            extraCreateSerializer.save()
            return Response("Extra EDITADO")
        except serializers.ValidationError as error:
            return Response(error.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(extraCreateSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#######################################################################################################################################################################


@api_view(['PATCH'])
def reserva_actualizar_codigo(request, reserva_id):
    try:
        reserva = Reserva.objects.get(id=reserva_id)
    except Reserva.DoesNotExist:
        return Response({"detail": "Reserva no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    # Usamos un serializer para actualizar solo el nombre de la reserva (o lo que necesites)
    serializer = ReservaSerializerActualizarCodigo(data=request.data, instance=reserva)
    
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Reserva actualizada con éxito", status=status.HTTP_200_OK)
        except Exception as error:
            print(repr(error))  # Para depuración
            return Response({"detail": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PATCH'])
def usuario_actualizar_nombre(request, usuario_id):
    try:
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        return Response({"detail": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # Usamos un serializer para actualizar solo el nombre de la reserva (o lo que necesites)
    serializer = UsuarioSerializerActualizarNombre(data=request.data, instance=usuario)
    
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Usuario actualizado con éxito", status=status.HTTP_200_OK)
        except Exception as error:
            print(repr(error))  # Para depuración
            return Response({"detail": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PATCH'])
def transporte_actualizar_capacidad(request, transporte_id):
    try:
        transporte = Transporte.objects.get(id=transporte_id)
    except Transporte.DoesNotExist:
        return Response({"detail": "Transporte no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # Usamos un serializer para actualizar solo el nombre de la reserva (o lo que necesites)
    serializer = TransporteSerializerActualizarCapacidad(data=request.data, instance=transporte)
    
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Transporte actualizado con éxito", status=status.HTTP_200_OK)
        except Exception as error:
            print(repr(error))  # Para depuración
            return Response({"detail": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['PATCH'])
def extra_actualizar_nombre(request, extra_id):
    try:
        extra = Extra.objects.get(id=extra_id)
    except Extra.DoesNotExist:
        return Response({"detail": "Extra no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    # Usamos un serializer para actualizar solo el nombre de la reserva (o lo que necesites)
    serializer = ExtraSerializerActualizarNombre(data=request.data, instance=extra)
    
    if serializer.is_valid():
        try:
            serializer.save()
            return Response("Extra actualizado con éxito", status=status.HTTP_200_OK)
        except Exception as error:
            print(repr(error))  # Para depuración
            return Response({"detail": repr(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

#######################################################################################################################################################################


@api_view(['DELETE'])
def reserva_eliminar(request, reserva_id):
    reserva = Reserva.objects.get(id=reserva_id)
    try:
        reserva.delete()
        return Response("Reserva ELIMINADA")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['DELETE'])
def usuario_eliminar(request, usuario_id):
    usuario = Usuario.objects.get(id=usuario_id)
    try:
        usuario.delete()
        return Response("Usuario ELIMINADO")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['DELETE'])
def transporte_eliminar(request, transporte_id):
    transporte = Transporte.objects.get(id=transporte_id)
    try:
        transporte.delete()
        return Response("Transporte ELIMINADO")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

@api_view(['DELETE'])
def extra_eliminar(request, extra_id):
    extra = Extra.objects.get(id=extra_id)
    try:
        extra.delete()
        return Response("Extra ELIMINADO")
    except Exception as error:
        return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

#######################################################################################################################################################################


# views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny

class registrar_usuario(generics.CreateAPIView):
    serializer_class = UsuarioSerializerRegistro
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializers = UsuarioSerializerRegistro(data=request.data)
        if serializers.is_valid():
            try:
                rol = request.data.get('rol')
                user = Usuario.objects.create_user(
                    nombre = serializers.data.get("nombre"),
                    username = serializers.data.get("username"), 
                    correo = serializers.data.get("correo"), 
                    edad = serializers.data.get("edad"), 
                    telefono = serializers.data.get("telefono"), 
                    password = serializers.data.get("password1"),
                    contraseña = serializers.data.get("password1"),
                    rol = rol,
                )
                if(rol == Usuario.CLIENTE):
                    grupo = Group.objects.get(name='Clientes') 
                    grupo.user_set.add(user)
                    cliente = Cliente.objects.create(usuario = user)
                    cliente.save()
                elif(rol == Usuario.PROVEEDOR):
                    grupo = Group.objects.get(name='Proveedores') 
                    grupo.user_set.add(user)
                    proveedor = Proveedor.objects.create(usuario = user)
                    proveedor.save()
                usuarioSerializado = UsuarioSerializer(user)
                return Response(usuarioSerializado.data)
            except Exception as error:
                print(repr(error))
                return Response(repr(error), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        


from oauth2_provider.models import AccessToken     
@api_view(['GET'])
def obtener_usuario_token(request,token):
    ModeloToken = AccessToken.objects.get(token=token)
    usuario = Usuario.objects.get(id=ModeloToken.user_id)
    serializer = UsuarioSerializer(usuario)
    return Response(serializer.data)