from django import forms
from material import *
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q
from models import Mantenimiento,Proveedor,Incidencia



class IncidenciaForm(forms.ModelForm):
    class Meta:
        model = Incidencia
        fields = ('causa', 'consecuencia', 'fecha_mantenimiento')

        layout = Layout(Fieldset('Informacion Incidencia:',
                                Row('causa'), Row('consecuencia'), Row('fecha_mantenimiento')
                                 )
                        )



class MantenimientoForm(forms.ModelForm):
      class Meta:
        model=Mantenimiento
        fields = ('fecha', 'descripcion','costo','id_proveedor')
        widgets = {

            'id_proveedor': forms.Select()
        }
        layout = Layout(Fieldset('Informacion Mantenimiento:',
                                 Row('fecha',), Row('descripcion',), Row('costo',), Row('id_proveedor',)
                                 )
                        )


      def __init__(self, *args, **kwargs):
            super(MantenimientoForm, self).__init__(*args, **kwargs)
            self.fields['id_proveedor'].widget = forms.Select(choices=[('', 'Interno')]+list ([(x.id_proveedor, x.nombre) for x in Proveedor.objects.all()]))