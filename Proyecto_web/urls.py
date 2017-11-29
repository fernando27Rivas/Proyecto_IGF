from Proyecto_web import views
from django.conf.urls import url,include

urlpatterns=[


    #url(r'^$', views.home, name='home'),
    #URL de Preventivos
    url(r'^agregar_preventivo/(?P<vehiculo_id>[0-9]+)$', views.Agregar_preventivo, name='preventivo'),
    url(r'^actualizar/(?P<id_mantenimiento>[0-9]+)$', views.Actualizar_Prevetivo, name='actualizar'),
    url(r'^mantenimientos/(?P<id_vehiculo>[0-9]+)$', views.Mantenimientos, name='mantenimientos'),
    # URL de Incidencias
    url(r'^agregar_incidencia/(?P<id_visita>[0-9]+)$', views.Agregar_incidencia, name='incidencia'),
    url(r'^incidencias/(?P<id_vehiculo>[0-9]+)$', views.consultarIncidencias, name='consultarincidencias'),
    #URL de Correctivos
    url(r'^agregar_correctivo/(?P<incidencia_id>[0-9]+)$', views.Agregar_correctivo, name='correctivo'),
    ## Los correctivos no se van a actualizar
    # URLS para la visita
    url(r'^solicitud_visita/$', views.SolicitarVisita, name='solicitud'),
    url(r'^lista_solicitudes/$', views.Lista_solicitud, name='lista_solicitudes'),
    url(r'^resolucion_solicitud/(?P<id_solicitud>[0-9]+)$', views.Resolucion_solicitud, name='resolucion_solicitud'),
    url(r'^agrupar_visita/(?P<id_visita>[0-9]+)/(?P<id_asignar>[0-9]+)$', views.Asignar_visita, name='asignar'),
    #URL Vehiculos
    url(r'^vehiculos/$', views.Lista_vehiculos, name='lista_vehiculos'),

    url(r'^login/$', views.minsal_login, name='minsal_login'),
    url(r'^logout/$', views.minsal_logout, name='minsal_logout'),

    ]