from django import forms
from material import *
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from models import Mantenimiento,Proveedor,Incidencia,Vehiculo,Visita,Conductor


class ProximoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['proximo_mantenimiento',]

class SolicitudForm(forms.ModelForm):
    class Meta:
      model=Visita
      fields=('fecha_inicio','fecha_fin','destino')

      layout = Layout(Fieldset('Informacion Solicitud:',
                              Row('fecha_inicio'), Row('destino'),Row('fecha_fin')) )

class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ('causa', 'consecuencia', 'fecha')

        layout = Layout(Fieldset('Informacion Incidencia:',
                                Row('causa'), Row('consecuencia'), Row('fecha')
                                 )
                        )

class ResolucionForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ( 'id_vehiculo', 'id_conductor')
        widgets = {

            'id_vehiculo': forms.Select(),
            'id_conductor': forms.Select()
                 }

        layout = Layout(Fieldset('Datos Asignacion:',
                                 Row('id_vehiculo', ), Row('id_conductor', )) )

    def __init__(self, *args, **kwargs):
        super(ResolucionForm, self).__init__(*args, **kwargs)
        self.fields['id_conductor'].widget = forms.Select(
            choices=[('', 'Sin conductor')] + list([(x.id_conductor, x.nombre) for x in Conductor.objects.all()]))
        self.fields['id_vehiculo'].widget = forms.Select(
            choices=[('', 'Escoja Vehiculo')]+list([(x.id_vehiculo, x.placa) for x in Vehiculo.vehiculo.filter(estado=1)]))

class VehiculoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        fields = ['estado',]
        widgets = {

            'estado': forms.Select()
        }

    def __init__(self, *args, **kwargs):
            super(VehiculoForm, self).__init__(*args, **kwargs)
            self.fields['estado'].widget = forms.Select(choices=[(1,'Disponible'),(4,'Inactivo')])

class ConductorForm(forms.ModelForm):
    class Meta:
       model = Conductor
       fields = ('nombre', 'apellido','numero_telefono','fecha_nacimiento','licencia')
       widgets = {
          'licencia': forms.Select(),
                  }

       layout = Layout(Fieldset('Datos Conductor:',
                             Row('nombre', ), Row('apellido','numero_telefono',
                                                  'fecha_nacimiento','licencia' )))
    def __init__(self, *args, **kwargs):
        super(ConductorForm, self).__init__(*args, **kwargs)
        self.fields['licencia'].widget = forms.Select(choices=[('Liviana', 'Liviana'),
         ('Particular', 'Particular'),('Pesada','Pesada'),('Pesada-T','Pesada-T')])


class Add_VehiculosForm(forms.ModelForm):
    class Meta:
       model = Vehiculo
       fields = ['placa','estado','proximo_mantenimiento','color' ]
       widgets = {

           'estado': forms.Select(),
       }
    def __init__(self, *args, **kwargs):
      super(Add_VehiculosForm, self).__init__(*args, **kwargs)
      self.fields['estado'].choices=[(1, 'Disponible'), (3, 'Mantenimiento'),(4, 'Inactivo')]


class MantenimientoForm(forms.ModelForm):
       class Meta:
        model=Mantenimiento
        fields = ('fecha_actual', 'descripcion','proveedor','costo')
        widgets = {

            'proveedor': forms.Select()
        }

       def __init__(self, *args, **kwargs):
            super(MantenimientoForm, self).__init__(*args, **kwargs)
            self.fields['proveedor'].choices = ([('', 'Interno')]+list ([(x.id_proveedor, x.nombre) for x in Proveedor.objects.all()]))

class PreventivoForm(forms.ModelForm):
          class Meta:
              model = Mantenimiento
              fields = ('fecha_actual', 'descripcion', 'proveedor','costo' )
              widgets = {

                  'proveedor': forms.Select()
              }
              layout = Layout(Fieldset('Informacion Mantenimiento:',
                                       Row('fecha_actual', ), Row('descripcion', ), Row('costo', ),
                                       Row('proveedor' )
                                       )
                              )

          def __init__(self, *args, **kwargs):
              super(PreventivoForm, self).__init__(*args, **kwargs)
              self.fields['proveedor'].widget = forms.Select(
                  choices=[('', 'Interno')] + list([(x.id_proveedor, x.nombre) for x in Proveedor.objects.all()]))

class EstadoForm(forms.ModelForm):

    class Meta:
        model = Vehiculo
        fields = ['estado',]
        widgets = {

            'estado': forms.Select()
        }

    def __init__(self, *args, **kwargs):
            super(EstadoForm, self).__init__(*args, **kwargs)
            self.fields['estado'].widget = forms.Select(choices=[(1,'Disponible'),
                     (2,'Asignado'),(3, 'Mantenimiento'),(4,'Inactivo')])