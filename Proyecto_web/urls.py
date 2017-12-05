from Proyecto_web import views
from django.conf.urls import url,include

urlpatterns=[



    #URL de Preventivos
    #SE accede por la lista de Vehiculos
    url(r'^agregar_preventivo/(?P<vehiculo_id>[0-9]+)$', views.Agregar_preventivo, name='preventivo'),
    #se accede por la lista de Vehiculos
    url(r'^actualizar/(?P<id_mantenimiento>[0-9]+)$', views.Actualizar_Prevetivo, name='actualizar'),
    #Se accede por la vista de vehiculos Lista de mAntenimientos de un vehiculo
    url(r'^lista_preventivos/(?P<id_vehiculo>[0-9]+)$', views.Mantenimientos, name='mantenimientos'),
    # URL de Incidencias
    # se accede por la lista de visitas
    url(r'^agregar_incidencia/(?P<id_visita>[0-9]+)$', views.Agregar_incidencia, name='incidencia'),
    #se Accede por lista de Vehiculos
    url(r'^incidencias/(?P<id_vehiculo>[0-9]+)$', views.consultarIncidencias, name='consultarincidencias'),
    #URL de Correctivos
    # se accede por lista de incidencias
    url(r'^agregar_correctivo/(?P<incidencia_id>[0-9]+)$', views.Agregar_correctivo, name='correctivo'),
    ## Los correctivos no se van a actualizar
    url(r'^lista_correctivos/(?P<id_vehiculo>[0-9]+)$', views.Correctivos, name='mantenimientos'),
    # URLS para la visita
    #Se accede por el menu
    url(r'^solicitud_visita/$', views.SolicitarVisita, name='solicitud'),
    # se Accede por el menu
    url(r'^lista_solicitudes/$', views.Lista_solicitud, name='lista_solicitudes'),
    url(r'^visitas_finalizadas/$', views.Visitas_Unidad, name='visitas_finalizadas'),
    url(r'^mis_visitas/$', views.Mis_visitas, name='mis_visitas'),
    url(r'^mis_aprobadas/$', views.Mis_aprobadas, name='mis_aprobadas'),


    # se Accede por lista de Solicitudes
    url(r'^resolucion_solicitud/(?P<id_solicitud>[0-9]+)$', views.Resolucion_solicitud, name='resolucion_solicitud'),

    #se Accede por lista de Solicitudes
    url(r'^agrupar_visita/(?P<id_visita>[0-9]+)/(?P<id_asignar>[0-9]+)$', views.Asignar_visita, name='asignar'),

    #URL Vehiculos
    #se accede por menu
    url(r'^proximos_mantenimientos/$', views.proximo_mantenimiento, name='proximos'),
    url(r'^vehiculos/$', views.lista_vehiculos, name='vehiculos'),

    #URL LOgin/LOgout
    # Metela a patita
    url(r'^login/$', views.minsal_login, name='minsal_login'),
      #se accede por menu
    url(r'^logout/$', views.minsal_logout, name='minsal_logout'),

    #URL Menu
    #hay que ponerle algo :O
    url(r'^base/$', views.base, name='base'),
    url(r'^agregar_conductor/$', views.Agregar_conductor, name='conductor'),
    url(r'^agregar_vehiculo/$', views.Agregar_vehiculo, name='add_vehiculo'),
    url(r'^actualizar_conductor/(?P<id_conductor>[0-9]+)$', views.Actualizar_Conductor, name='change_conductor'),
    url(r'^conductores/$', views.lista_conductores, name='coductores'),

    url(r'^actualizar_estado/(?P<id_vehiculo>[0-9]+)$', views.actualizar_estado, name='estado'),
    ]