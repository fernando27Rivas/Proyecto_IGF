from Proyecto_web import views
from django.conf.urls import url,include

urlpatterns=[



    #URL de Preventivos
    #Para Agregar Mantenimiento Preventivo
    url(r'^agregar_preventivo/(?P<vehiculo_id>[0-9]+)/(?P<activo>[0-9]+)$', views.Agregar_preventivo, name='preventivo'),
    #Para actualizar un preventivo
    url(r'^actualizar/(?P<id_mantenimiento>[0-9]+)/(?P<activo>[0-9]+)$', views.Actualizar_Prevetivo, name='actualizar'),

    #Para obtener consulta de preventivos de un vehiculo
    url(r'^lista_preventivos/(?P<id_vehiculo>[0-9]+)$', views.Mantenimientos, name='lista_preventivos'),

    # URL de Incidencias
    # Para agregar incidencia
    url(r'^agregar_incidencia/(?P<id_visita>[0-9]+)$', views.Agregar_incidencia, name='incidencia'),
    #Para cosultar Incidencia
    url(r'^incidencias/(?P<id_vehiculo>[0-9]+)$', views.consultarIncidencias, name='consultarincidencias'),

    #URL de Correctivos
    # Para crear un mantenimiento correctivo
    url(r'^agregar_correctivo/(?P<incidencia_id>[0-9]+)/(?P<activo>[0-9]+)$', views.Agregar_correctivo, name='correctivo'),
    # Lista de mantenimientos correctivos
    url(r'^lista_correctivos/(?P<id_vehiculo>[0-9]+)$', views.Correctivos, name='lista_correctivos'),

    # URLS para la visita
    #Para solicitud de una visita
    url(r'^solicitud_visita/$', views.SolicitarVisita, name='solicitud'),
    # para las visitas que se necesitan aprobar
    url(r'^lista_solicitudes/$', views.Lista_solicitud, name='lista_solicitudes'),
    #para lass visitas que ya esta finalizadas vista de administrador para agregar incidencia
    url(r'^visitas_finalizadas/$', views.Visitas_Unidad, name='visitas_finalizadas'),
    #Para las visitas en estado terminadas de un ususario dterminado
    url(r'^mis_visitas/$', views.Mis_visitas, name='mis_visitas'),
    #Vsita para todos para ver las solicitudes en estado aprobadas
    url(r'^mis_aprobadas/$', views.Mis_aprobadas, name='mis_aprobadas'),
    # Para respondre a una solicitud solicitada
    url(r'^resolucion_solicitud/(?P<id_solicitud>[0-9]+)$', views.Resolucion_solicitud, name='resolucion_solicitud'),
    #Apara asignar datos de una visita a otra
    url(r'^agrupar_visita/(?P<id_visita>[0-9]+)/(?P<id_asignar>[0-9]+)$', views.Asignar_visita, name='asignar'),

    #URL Vehiculos
    #se accede por menu
    url(r'^proximos_mantenimientos/$', views.proximo_mantenimiento, name='proximos'),
    #Alerta de mantenimiento de los vehiculos
    url(r'^vehiculos/$', views.lista_vehiculos, name='vehiculos'),
     #Para crear Un nuevo vehiculo
    url(r'^agregar_vehiculo/$', views.Agregar_vehiculo, name='add_vehiculo'),
    #Para actualizar estado de Vehiculo
    url(r'^actualizar_estado/(?P<id_vehiculo>[0-9]+)/(?P<activo>[0-9]+)$', views.actualizar_estado, name='estado'),

    #URL Login/Logout
    # Metela a patita
    url(r'^login/$', views.minsal_login, name='minsal_login'),
      #se accede por menu
    url(r'^logout/$', views.minsal_logout, name='minsal_logout'),

    #URL Menu
    url(r'^base/$', views.base, name='base'),
    #URL Conductores
    #Para Agregar Conductores
    url(r'^agregar_conductor/(?P<activo>[0-9]+)$', views.Agregar_conductor, name='conductor'),
    #Para lista de conductores
    url(r'^conductores/$', views.lista_conductores, name='coductores'),
    #Para actualizar Conductores
    url(r'^actualizar_conductor/(?P<id_conductor>[0-9]+)/(?P<activo>[0-9]+)$', views.Actualizar_Conductor, name='change_conductor'),


    ]