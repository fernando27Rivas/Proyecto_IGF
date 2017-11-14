from Proyecto_web import views
from django.conf.urls import url,include

urlpatterns=[


    #url(r'^$', views.home, name='home'),
    url(r'^agregar_preventivo/(?P<vehiculo_id>[0-9]+)$', views.Agregar_preventivo, name='preventivo'),
    url(r'^actualizar/(?P<id_mantenimiento>[0-9]+)$', views.Actualizar_Prevetivo, name='actualizar'),
    url(r'^agregar_incidencia/(?P<id_visita>[0-9]+)$', views.Crear_Incidencia, name='incidencia'),
    url(r'^actualizar_incidencia/(?P<id_incidencia>[0-9]+)$', views.actualizar_Incidencia, name='incidencia_actualizada'),
    url(r'^incidencias/(?P<id_vehiculo>[0-9]+)$', views.consultarIncidencias, name='consultarincidencias'),
    url(r'^mantenimientos/(?P<id_vehiculo>[0-9]+)$', views.Mantenimientos, name='mantenimientos'),
    ]