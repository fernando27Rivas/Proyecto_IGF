# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.detail import DetailView
from django.shortcuts import render
from models import Incidencia,Mantenimiento,Vehiculo,Visita
from .forms import *

#Para Crear el Mantenimiento
def Agregar_preventivo(request,vehiculo_id):
    mensaje=""
    if request.method=='GET':
        mantenimiento_form=MantenimientoForm(prefix='mantenimiento')

    #Cuando es POST
    if request.method=='POST':
        mantenimiento_form=MantenimientoForm(request.POST or None, prefix='mantenimiento')
        if mantenimiento_form.is_valid():
            vehi=Vehiculo.objects.get(pk=vehiculo_id)

            tfecha=mantenimiento_form.cleaned_data['fecha']
            tdescripcion= mantenimiento_form.cleaned_data['descripcion']
            tcosto = float(mantenimiento_form.cleaned_data['costo'])
            tproveedor=mantenimiento_form.cleaned_data['id_proveedor']
            mante=Mantenimiento.objects.create(
                fecha=tfecha,
                descripcion=tdescripcion,
                tipo=1, #Tipo=1 asumiento que 1 es preventivo
                costo=tcosto,
                id_vehiculo=vehi,
                id_proveedor=tproveedor,
                id_incidencia=None


                )
            #Limpiando campos despues de guardar

            mensaje="Mantenimiento registrado a "+ vehi.placa
            mantenimiento_form=MantenimientoForm(prefix='mantenimiento')


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

    mantenimiento_form = MantenimientoForm(data=request.POST or None, instance=mantenimiento)

    if request.method == 'POST':

       if mantenimiento_form.is_valid():
           mantenimiento_form.save()
           mensaje = "Modifico con exito"
       else:
           mensaje="Error"

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

             tfecha= incidencia_form.cleaned_data['fecha_mantenimiento']
             tcausa= incidencia_form.cleaned_data['causa']
             tconsecuencia = incidencia_form.cleaned_data['consecuencia']
             visita=Visita.objects.get(pk=id_visita)
             vehiculo=Vehiculo.objects.get(pk=visita.id_visita)

             incidencia=Incidencia.objects.create(
                 fecha_mantenimiento=tfecha,
                 causa=tcausa,
                 consecuencia=tconsecuencia,
                 id_visita=visita,
                 id_vehiculo=vehiculo,
             )

             if mantenimiento_form.is_valid():
                #Registro de Mantenimiento
                tfecha = mantenimiento_form.cleaned_data['fecha']
                tdescripcion = mantenimiento_form.cleaned_data['descripcion']
                #tcosto = float(mantenimiento_form.cleaned_data['costo'])
                tproveedor = mantenimiento_form.cleaned_data['id_proveedor']

                mante = Mantenimiento.objects.create(
                   fecha=tfecha,
                   descripcion=tdescripcion,
                   tipo=2,  # Tipo=1 asumiento que 2 es Correctivo
                   costo=0,
                   id_vehiculo=vehiculo,
                   id_proveedor=tproveedor,
                   id_incidencia=incidencia
                  )

             else:
                 mantenimiento_form=None
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
           mensaje="Error"
    else:
        mensaje="nada"


    return render(request, 'actualizar_incidencia.html', {'incidencia_form': incidencia_form,
                                 'mensaje': mensaje, })

