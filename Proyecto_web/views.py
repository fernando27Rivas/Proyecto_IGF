# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.detail import DetailView
from django.shortcuts import render
from models import Incidencia,Mantenimiento,Vehiculo,Visita
from .forms import *
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import Http404
#Para Crear el Mantenimiento
def Agregar_preventivo(request,vehiculo_id):
    mensaje=""
    if request.method=='GET':
        mantenimiento_form=PreventivoForm(prefix='mantenimiento')

    #Cuando es POST
    if request.method=='POST':
        mantenimiento_form=PreventivoForm(request.POST or None, prefix='mantenimiento')
        if mantenimiento_form.is_valid():

         if (mantenimiento_form.cleaned_data['fecha_proximo']):

            vehi=Vehiculo.objects.get(pk=vehiculo_id)

            tfecha=mantenimiento_form.cleaned_data['fecha_actual']
            tdescripcion= mantenimiento_form.cleaned_data['descripcion']
            if (mantenimiento_form.cleaned_data['costo']):
             tcosto = float(mantenimiento_form.cleaned_data['costo'])
            else:
                tcosto=0
            tproveedor=mantenimiento_form.cleaned_data['id_proveedor']
            tproximo = mantenimiento_form.cleaned_data['fecha_proximo']
            mante=Mantenimiento.objects.create(
                fecha_actual=tfecha,
                descripcion=tdescripcion,
                tipo=1, #Tipo=1 asumiento que 1 es preventivo
                costo=tcosto,
                id_vehiculo=vehi,
                id_proveedor=tproveedor,
                fecha_proximo=tproximo

                )
            #Limpiando campos despues de guardar

            mensaje="Mantenimiento registrado a "+ vehi.placa
            mantenimiento_form=PreventivoForm(prefix='mantenimiento')
         else:
             mensaje=" Error Programe el proximo Mantenimiento"

    extra_context = {
    'mantenimiento_form':mantenimiento_form,
    'mensaje': mensaje,
    'vehiculo_id':vehiculo_id
     }

    return render(request, 'agregar_mantenimiento.html', extra_context)
#PAra Actualizar MAntenimiento

def Actualizar_Prevetivo(request,id_mantenimiento):
    mensaje = ""
    mantenimiento=Mantenimiento.objects.get(pk=id_mantenimiento)

    mantenimiento_form = PreventivoForm(data=request.POST or None, instance=mantenimiento)

    if request.method == 'POST':

       if mantenimiento_form.is_valid():
           if(mantenimiento_form.cleaned_data['fecha_proximo']):
            mantenimiento_form.save()
            mensaje = "Modifico con exito"
           else:
               mensaje="Error Agregue el Proximo Mantenimiento"
       else:
           mensaje="Error Campos Obligatorios"

    return render(request, 'agregar_mantenimiento.html', {'mantenimiento_form': mantenimiento_form,
                                 'mensaje': mensaje, })

def Crear_Incidencia (request,id_visita):
    mensaje = ""
    mante = None
    if request.method == 'GET':
        incidencia_form = IncidenciaForm(prefix='incidencia')
        mantenimiento_form = MantenimientoForm(prefix='mantenimiento')

    if request.method=='POST':
        incidencia_form=IncidenciaForm(request.POST or None, prefix='incidencia')
        mantenimiento_form=MantenimientoForm(request.POST or None, prefix='mantenimiento')

        if incidencia_form.is_valid():
             visita = Visita.objects.get(pk=id_visita)
             vehiculo = Vehiculo.objects.get(pk=visita.id_visita)

             if mantenimiento_form.is_valid():
                #Registro de Mantenimiento
                tfecha = mantenimiento_form.cleaned_data['fecha_actual']
                tdescripcion = mantenimiento_form.cleaned_data['descripcion']
                if (mantenimiento_form.cleaned_data['costo']):
                    tcosto = float(mantenimiento_form.cleaned_data['costo'])
                else:
                    tcosto = 0
                tproveedor = mantenimiento_form.cleaned_data['id_proveedor']

                mante = Mantenimiento.objects.create(
                   fecha_actual=tfecha,
                   descripcion=tdescripcion,
                   tipo=0,  # Tipo=0 asumiento que  es Correctivo
                   costo=tcosto,
                   id_vehiculo=vehiculo,
                   id_proveedor=tproveedor,

                  )

             else:
                 mantenimiento_form=None


             tfecha= incidencia_form.cleaned_data['fecha_mantenimiento']
             tcausa= incidencia_form.cleaned_data['causa']
             tconsecuencia = incidencia_form.cleaned_data['consecuencia']


             incidencia=Incidencia.objects.create(
                 fecha_mantenimiento=tfecha,
                 causa=tcausa,
                 consecuencia=tconsecuencia,
                 id_visita=visita,
                 id_vehiculo=vehiculo,
                 id_mantenimiento=mante
             )


             mensaje="Registro la Incidencia de la visita"+ str(visita.id_visita)+"con placas"+vehiculo.placa
             #Vaciando Formulario
             incidencia_form=IncidenciaForm(prefix='incidencia') #Vaciando El formulario
             mantenimiento_form=MantenimientoForm(prefix='mantenimiento') #Vaciando El formulario
        else:
            mensaje="Formulario Vacio"
    extra_context = {
    'incidencia_form':incidencia_form,
    'mantenimiento_form': mantenimiento_form,
    'mensaje': mensaje
      }

    return render(request, 'agregar_incidencia.html', extra_context)

def actualizar_Incidencia(request,id_incidencia):
    mensaje = ""
    incidencia=Incidencia.objects.get(pk=id_incidencia)

    incidencia_form = IncidenciaForm(data=request.POST or None, instance=incidencia)

    if request.method == 'POST':

       if incidencia_form.is_valid():
           incidencia_form.save()
           mensaje = "Modifico con exito"
       else:
           mensaje="Error Formulario Vacio"
    else:
        mensaje=""


    return render(request, 'actualizar_incidencia.html', {'incidencia_form': incidencia_form,
                                 'mensaje': mensaje, })



def Mantenimientos(request,id_vehiculo):
   # if request.user.has_perm('donaciones.change_donador') or request.user.has_perm(
    #    'donaciones.delete_donador'):
       try:
        mantenimientos_list = Mantenimiento.objects.filter(id_vehiculo=id_vehiculo)
        placa=Vehiculo.objects.get(pk=id_vehiculo)
        return render(request, 'consultar_mantenimientos.html', {'mantenimientos_list': mantenimientos_list,'placa':placa })

       except :
        raise Http404("Error en URL")
        return HttpResponseRedirect('/admin')

def consultarIncidencias(request,id_vehiculo):
   # if request.user.has_perm('donaciones.change_donador') or request.user.has_perm(
    #    'donaciones.delete_donador'):
       try:
        incidencias_list = Incidencia.objects.filter(id_vehiculo=id_vehiculo)
        placa=Vehiculo.objects.get(pk=id_vehiculo)

        return render(request, 'consultar_incidencia.html',
                      {'incidencias_list': incidencias_list,'placa':placa, })

       except :
        raise Http404("Error en URL")
        return HttpResponseRedirect('/admin')