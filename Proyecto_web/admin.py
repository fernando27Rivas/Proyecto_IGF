# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Para registara los modelos en el Admin de Django

admin.site.register(Vehiculo)
admin.site.register(UnidadOrganizacional)
admin.site.register(Proveedor)
admin.site.register(Visita)
admin.site.register(Mantenimiento)
admin.site.register(Incidencia)
admin.site.register(Licencia)
admin.site.register(Conductor)
admin.site.register(Usuario)


# Register your models here.
