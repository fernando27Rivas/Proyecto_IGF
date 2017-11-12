# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

admin.site.register(Vehiculo)
admin.site.register(UnidadOrganizacional)
admin.site.register(Proveedor)
admin.site.register(Visita)
admin.site.register(Mantenimiento)
# Register your models here.
