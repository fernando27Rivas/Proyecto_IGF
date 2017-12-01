# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User, Permission
from django.shortcuts import render
from models import Incidencia,Mantenimiento,Vehiculo,Visita,UnidadOrganizacional,Usuario
from .forms import *
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from datetime import datetime, date, time, timedelta
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout

#Para Crear el Mantenimiento



@login_required
def base(request):
    return render(request, 'base.html',)

@login_required   #Se necesita Iniciar Sesion
#@permission_required('Proyecto_web.add_visita') #Permisos para ejecutar la funcion  Si no tiene el permiso lo manda al login
def Agregar_preventivo(request,vehiculo_id):
    mensaje=""
    if request.method=='GET':
        mantenimiento_form=PreventivoForm(prefix='mantenimiento')
        vehiculo_form=ProximoForm(prefix='proximo')
    #Cuando es POST
    if request.method=='POST':
        mantenimiento_form=PreventivoForm(request.POST or None, prefix='mantenimiento')
        vehiculo_form = ProximoForm(request.POST or None, prefix='proximo')
        if mantenimiento_form.is_valid()& vehiculo_form.is_valid():



            vehi=Vehiculo.objects.get(pk=vehiculo_id)
            tproveedor = mantenimiento_form.cleaned_data['proveedor']
            tfecha=mantenimiento_form.cleaned_data['fecha_actual']
            tdescripcion= mantenimiento_form.cleaned_data['descripcion']
            if (mantenimiento_form.cleaned_data['costo']):
             tcosto = float(mantenimiento_form.cleaned_data['costo'])
            else:
                tcosto=0

            vehi.proximo_mantenimiento=vehiculo_form.cleaned_data['proximo_mantenimiento'] #Actualizar en vehiculo

            vehi.save()
            mante=Mantenimiento.objects.create(
                fecha_actual=tfecha,
                descripcion=tdescripcion,
                tipo=1, #Tipo=1 asumiento que 1 es preventivo
                costo=tcosto,
                id_vehiculo=vehi,
                proveedor=tproveedor,
                )
            #Limpiando campos despues de guardar

            mensaje="Mantenimiento registrado a "+ vehi.placa
            mantenimiento_form=PreventivoForm(prefix='mantenimiento')
            vehiculo_form=ProximoForm(prefix='proximo')


    extra_context = {
    'mantenimiento_form':mantenimiento_form,
    'vehiculo_form':vehiculo_form,
    'mensaje': mensaje,
    'vehiculo_id':vehiculo_id
     }

    return render(request, 'agregar_mantenimiento.html', extra_context)

#PAra Actualizar MAntenimiento
@login_required
def Actualizar_Prevetivo(request,id_mantenimiento):
    mensaje = ""
    mantenimiento=Mantenimiento.objects.get(pk=id_mantenimiento)
    vehiculo=mantenimiento.id_vehiculo
    mantenimiento_form = PreventivoForm(data=request.POST or None, instance=mantenimiento)
    vehiculo_form = ProximoForm(data=request.POST or None, instance=vehiculo)
    if request.method == 'POST':

       if mantenimiento_form.is_valid() & vehiculo_form.is_valid():

            mantenimiento_form.save()
            vehiculo_form.save()
            mensaje="Actualizacion exitosa"
       else:
           mensaje="Error Campos Obligatorios"

    return render(request, 'agregar_mantenimiento.html', {'mantenimiento_form': mantenimiento_form,
                                 'mensaje': mensaje,'vehiculo_form':vehiculo_form })

@login_required
def Agregar_incidencia(request,id_visita):
    mensaje = ""
    mante = None
    try:
        visita = Visita.objects.get(pk=id_visita)
    except Visita.DoesNotExist:
        raise Http404("No existe la vista referenciada.")

    if request.method == 'GET':
        incidencia_form = IncidenciaForm(prefix='incidencia')
        vehiculo_form  =  VehiculoForm(prefix='vehiculo')

    if request.method == 'POST':
        incidencia_form = IncidenciaForm(request.POST or None, prefix='incidencia')
        vehiculo_form = VehiculoForm(request.POST or None,prefix='vehiculo')

        if incidencia_form.is_valid():

            vehiculo = Vehiculo.objects.get(pk=visita.id_vehiculo.id_vehiculo)

            tfecha = incidencia_form.cleaned_data['fecha']
            tcausa = incidencia_form.cleaned_data['causa']
            tconsecuencia = incidencia_form.cleaned_data['consecuencia']


            if (vehiculo_form.is_valid()):
              vehiculo.estado=int (vehiculo_form.cleaned_data['estado'])
              vehiculo.save()

            incidencia = Incidencia.objects.create(
                fecha=tfecha,
                causa=tcausa,
                consecuencia=tconsecuencia,
                id_visita=visita,
                id_vehiculo=vehiculo,
                id_mantenimiento=None
            )

            mensaje = "Registro la Incidencia de la visita " + str(visita.id_visita) + " con placas" + vehiculo.placa

            # Vaciando Formulario

            incidencia_form = IncidenciaForm(prefix='incidencia')  # Vaciando El formulario
            vehiculo_form = VehiculoForm(prefix='vehiculo')

            ## Para redirigir a la siguiente vista
            url = reverse('correctivo', kwargs={'incidencia_id': incidencia.id_incidencia})
            return  HttpResponseRedirect(url)
        else:
            mensaje = "Formulario Vacio o Campos Incompletos"

    extra_context = {
        'incidencia_form': incidencia_form,
        'mensaje': mensaje,
        'vehiculo_form':vehiculo_form
    }

    return render(request, 'agregar_incidencia.html', extra_context,)

@login_required
def Correctivos(request,id_vehiculo):
    if request.user.has_perm('Proyecto_web.change_mantenimiento'):
       try:
        mantenimientos_list = Mantenimiento.objects.filter(id_vehiculo=id_vehiculo).filter(tipo=0)
        placa=Vehiculo.objects.get(pk=id_vehiculo)
        activo=False
        return render(request, 'consultar_mantenimientos.html', {'mantenimientos_list': mantenimientos_list,'placa':placa,'activo':activo })

       except :
        raise Http404("Error en URL")
        return HttpResponseRedirect('/admin')

#Consulta de Mantenimientos Preventivos solamente
@login_required
def Mantenimientos(request,id_vehiculo):
    if request.user.has_perm('Proyecto_web.change_mantenimiento'):
       try:
        mantenimientos_list = Mantenimiento.objects.filter(id_vehiculo=id_vehiculo).filter(tipo=1)
        placa=Vehiculo.objects.get(pk=id_vehiculo)
        activo=True
        return render(request, 'consultar_mantenimientos.html', {'mantenimientos_list': mantenimientos_list,'placa':placa,'activo':activo})

       except :
        raise Http404("Error en URL")
        return HttpResponseRedirect('/admin')

#Consulta las incidencias que no tiene asignado un mantenimiento Correctivo
@login_required
def consultarIncidencias(request,id_vehiculo):

    if request.user.has_perm('Proyecto_web.change_incidencia'):

       try:
        incidencias_list2 = Incidencia.objects.filter(id_vehiculo=id_vehiculo)
        incidencias_list=incidencias_list2.filter(id_mantenimiento__isnull=True)
        placa=Vehiculo.objects.get(pk=id_vehiculo)
        return render(request, 'consultar_incidencia.html',
                      {'incidencias_list': incidencias_list,'placa':placa, })

       except :
        raise Http404("Error en URL")
        return HttpResponseRedirect('/admin')
    else:
        raise Http404("Permisos Insuficientes")
        return HttpResponseRedirect('/admin')

#Vistas de Mantenimiento Correctivo
@login_required
def Agregar_correctivo(request,incidencia_id):
    mensaje=""
    if request.method=='GET':
        mantenimiento_form=PreventivoForm(prefix='mantenimiento')

    #Cuando es POST
    if request.method=='POST':
        mantenimiento_form=PreventivoForm(request.POST or None, prefix='mantenimiento')


        if mantenimiento_form.is_valid():
            inci=Incidencia.objects.get(pk=incidencia_id)
            vehi=Vehiculo.objects.get(pk=inci.id_vehiculo.id_vehiculo)

            tproveedor = mantenimiento_form.cleaned_data['proveedor']
            tfecha=mantenimiento_form.cleaned_data['fecha_actual']
            tdescripcion= mantenimiento_form.cleaned_data['descripcion']
            if (mantenimiento_form.cleaned_data['costo']):
             tcosto = float(mantenimiento_form.cleaned_data['costo'])
            else:
                tcosto=0

            mante = Mantenimiento.objects.create(
                fecha_actual=tfecha,
                descripcion=tdescripcion,
                tipo=0,  # Tipo=1 asumiento que 0 es Correctivo
                costo=tcosto,
                id_vehiculo=vehi,
                proveedor=tproveedor,
            )

            inci.id_mantenimiento=mante
            inci.save()
            # Limpiando campos despues de guardar

            mensaje="Mantenimiento Correctivo registrado a vehiculo placas  "+ vehi.placa
            mantenimiento_form=PreventivoForm(prefix='mantenimiento')



    extra_context = {
    'mantenimiento_form':mantenimiento_form,
    'mensaje': mensaje,

     }

    return render(request, 'agregar_correctivo.html', extra_context)

@login_required
def SolicitarVisita(request):
    mensaje = ""
    usuario =request.user
    user=Usuario.objects.get(id_user=usuario)

    if request.method == 'GET':
        visita_form = SolicitudForm(prefix='solicitud')

    # Cuando es POST
    if request.method == 'POST':
        visita_form = SolicitudForm(request.POST or None,prefix='solicitud')

        if visita_form.is_valid():
            tfecha_inicio = visita_form.cleaned_data['fecha_inicio']
            tdestino = visita_form.cleaned_data['destino']
            tfecha_fin=visita_form.cleaned_data['fecha_fin']

            visita = Visita.objects.create(
                fecha_inicio=tfecha_inicio,
                fecha_fin=tfecha_fin,
                destino=tdestino,
                estado=1, # Solicitada
                id_unidad= user.id_unidad,
                user=usuario
            )


            # Limpiando campos despues de guardar
            mensaje = " Solicitud de visita del Usuario "+ usuario.get_username()
            visita_form = SolicitudForm(prefix='solicitud')
        else:

            mensaje="Error en Formato " + usuario.get_username()

    extra_context = {
        'visita_form': visita_form,
        'mensaje': mensaje,

    }
    return render(request, 'solicitar_visita.html', extra_context)

@login_required
def Lista_solicitud(request):
    usuario = request.user
    user = Usuario.objects.get(id_user=usuario)
    unidad=user.id_unidad
    if request.user.has_perm('Proyecto_web.add_visita'):
       try:
        visitas_list = Visita.objects.filter(id_unidad=unidad.id_unidad_organizacional,estado=1)
        activo=True
        return render(request, 'lista_solicitudes.html', {'visitas_list': visitas_list,'activo':activo})
       except :
        raise Http404("Error en URL")
        return HttpResponseRedirect('/admin')
    else:
        raise Http404("Permisos Insuficientes")


@login_required
def Visitas(request):
    usuario = request.user
    user = Usuario.objects.get(id_user=usuario)
    unidad=user.id_unidad
    if request.user.has_perm('Proyecto_web.add_visita'):
       try:
        visitas_list = Visita.objects.filter(id_unidad=unidad.id_unidad_organizacional,estado=4)
        activo=False
        return render(request, 'lista_solicitudes.html', {'visitas_list': visitas_list,'activo':activo})
       except :
        raise Http404("Error en URL")
        return HttpResponseRedirect('/admin')
    else:
        raise Http404("Permisos Insuficientes")

@login_required
def Resolucion_solicitud(request,id_solicitud):
    mensaje = ""
    user = request.user
    visita=Visita.objects.get(pk=id_solicitud)
    usuario=Usuario.objects.get(id_user=user)
    unidad=usuario.id_unidad
    visita_list = Visita.objects.filter(id_unidad=unidad.id_unidad_organizacional, estado=2)
    if request.method == 'GET':
        resolucion_form = ResolucionForm(prefix='resolucion')
    # Cuando es POST
    if request.method == 'POST':
        resolucion_form = ResolucionForm(request.POST or None, prefix='resolucion')
        if (resolucion_form.is_valid()):
         if(resolucion_form.cleaned_data['id_vehiculo']):
            tvehiculo = resolucion_form.cleaned_data['id_vehiculo']
            #Validamos SI se selecciono Conductor
            if (resolucion_form.cleaned_data['id_conductor']):
             tconductor = resolucion_form.cleaned_data['id_conductor']
            else:
             tconductor=None

            visita.id_conductor = tconductor
            visita.id_vehiculo=tvehiculo
            visita.estado=2
            tvehiculo.estado=2
            tvehiculo.save()
             #Gurdamos el estado de la Solicitud
            visita.save()

            # Limpiando campos despues de guardar
            mensaje = " Solicitud de visita del Usuario " + user.get_username()
            visita_form = SolicitudForm(prefix='solicitud')
         else:

             mensaje = "Error en Formato Espacio vacio " + user.get_username()
        else:

            mensaje = "Error en Formato " + user.get_username()

    extra_context = {
        'resolucion_form': resolucion_form,
        'mensaje': mensaje,
        'visita_list':visita_list,
        'visita2':visita
    }
    return render(request, 'resolucion_visita.html', extra_context)

@login_required
def proximo_mantenimiento(request):
    if (request.user):
      user=request.user
      usuario = Usuario.objects.get(id_user=user)
      unidad = usuario.id_unidad
      if request.user.has_perm('Proyecto_web.change_mantenimiento'):
        try:
         vehiculos_list = Vehiculo.objects.filter(id_unidad=unidad.id_unidad_organizacional,proximo_mantenimiento__range=(date.today(),date.today()+timedelta(days=7)))#provisional
         activo = False
         return render(request, 'vehiculos_list.html', {'vehiculos_list': vehiculos_list,})

        except :
         raise Http404("Error en URL")
         return HttpResponseRedirect('/base')
      else:
        raise Http404("No posee permisos ")
        return HttpResponseRedirect('/base')
    else:
        raise Http404("No posee un Usuario Asignado :V")
        return HttpResponseRedirect('/base')

def minsal_login(request):
    mensaje = ""
    if request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/base')

        else:
            mensaje = "Usuario o Contraseña Incorrecto"
            return render(request, 'login.html', {'mensaje': mensaje, })
    else:
        return render(request, 'login.html', {'mensaje': mensaje, })
@login_required
def minsal_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

@login_required
def Asignar_visita(request,id_visita,id_asignar):
    visita=Visita.objects.get(pk=id_visita)
    visita_asignar=Visita.objects.get(pk=id_asignar)
    visita_asignar.id_vehiculo=visita.id_vehiculo
    visita_asignar.id_conductor=visita.id_conductor
    visita_asignar.estado=visita.estado
    visita_asignar.save()
    url = reverse('lista_solicitudes')
    return HttpResponseRedirect(url)

@login_required
def lista_vehiculos(request):
    if (request.user):
      user=request.user
      usuario = Usuario.objects.get(id_user=user)
      unidad = usuario.id_unidad
      if request.user.has_perm('Proyecto_web.change_mantenimiento'):
        try:
         vehiculos_list = Vehiculo.objects.filter(id_unidad=unidad.id_unidad_organizacional)
         activo=True
         vehiculo=vehiculos_list.first()
         return render(request, 'vehiculos_list.html', {'vehiculos_list': vehiculos_list,'activo':activo,'vehiculo':vehiculo})

        except :
         raise Http404("Error en URL")
         return HttpResponseRedirect('/base')
      else:
        raise Http404("No posee permisos ")
        return HttpResponseRedirect('/base')
    else:
        raise Http404("No posee un Usuario Asignado :V")
        return HttpResponseRedirect('/base')