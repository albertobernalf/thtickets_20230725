"""Thtickets URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf  import settings
from tickets import  views
from tickets.views import  CreacionTickets, AsignacionTickets, AsignacionTicketsUpdate, Contrasena, GestionCoord, GestionCoordUpdate, GestionCoordMallaUpdate, CrearMalla, THumano, THumanoUpdate
from django.conf.urls.static import  static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('tickets/', views.menuAcceso, name="ticketsAcceso"),
    path('validaAcceso/', views.validaAcceso, name = "validaAccesoA"),
    path('validaAcceso/<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>', views.validaAcceso, name = "validaAccesoB"),
    path('salir/', views.salir),
    # Tickets
    path('validaAcceso/creacionTickets/', CreacionTickets.as_view(),name='creacion_ticketsA'),
    path('validaAcceso/creacionTickets/<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>', CreacionTickets.as_view(),name='creacion_ticketsA'),
    path('creacionTickets/<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>', CreacionTickets.as_view(),name='creacion_ticketsA'),
    #path('asignacionTickets/creacionTickets/<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>', CreacionTickets.as_view(),name='creacion_ticketsA'),
    path('validaAcceso/creacionTickets/<int:pk>/', CreacionTickets.as_view(),name='creacion_ticketsB'),
    path('detail/', views.DetailTicket, name='detail'),
    path('load_dataTickets/<str:data>', views.load_dataTickets, name='loaddataTickets'),
    path('creacionTickets/postConsultaTicket/<str:id>,<str:username>,<str:empleadoId>/edit/', views.PostConsultaTicket,name='Post_editTicket'),
    path('load_asignacionTickets/<str:data>', views.load_asignacionTickets, name='loadasignacionTickets'),

    path('asignacionTickets/', AsignacionTickets.as_view(),name='asignacion_ticketsA'),
    path('asignacionTickets/<str:ticketId>,<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>', AsignacionTickets.as_view(),name='asignacion_ticketsA'),

    path('asignacionTickets1/', AsignacionTickets.as_view(),name='asignacion_ticketsC'),
    path('asignacionTickets1/<str:ticketId>,<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>', AsignacionTickets.as_view(),name='asignacion_ticketsC'),

    #path('asignacionTickets/update/<int:pk>/', AsignacionTicketsUpdate.as_view(),name='asignacionTickets-update'),
    path('asignacionTickets/update/<int:pk>,<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>/', AsignacionTicketsUpdate.as_view(),name='asignacionTickets-update'),

    path('contrasena/', Contrasena.as_view(),name='contrasena'),
    path('contrasena/<int:pk>,<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>', Contrasena.as_view(),name='contrasena'),

    path('gestionCoord/',GestionCoord.as_view(), name='gestionCoord_A'),
    path('gestionCoord/<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>', GestionCoord.as_view(),name='gestionCoord'),
    path('gestionCoord/update/<int:pk>,<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>/', GestionCoordUpdate.as_view(),name='gestionCoord-update'),
    path('load_dataCoordTickets/<str:data>', views.load_dataCoordTickets, name='loaddataCoordTickets'),
    #path('load_dataCoordTickets/', views.load_dataCoordTickets, name='loaddataCoordTickets'),
    path('gestionCoordMalla/update/<int:pk>,<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>/', GestionCoordMallaUpdate.as_view(),name='gestionCoordMalla-update'),

    path('crearMalla/<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>/', CrearMalla.as_view(),name='crearMalla'),

    path('tHumano/', THumano.as_view(), name='tHumano'),
    path('tHumano/<str:ticketId>,<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>',THumano.as_view(), name='tHumano'),
    path('tHumano/update/<int:pk>,<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>/', THumanoUpdate.as_view(),name='tHumano-Update'),

    path('ticketsMalla/<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>', views.TicketsMalla1.as_view(), name = "ticketsMalla_a"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Añadir
admin.site.site_header = 'Administracion Talento Humano Tickets'
admin.site.site_title = "Portal Talento Humano Tickets"
admin.site.index_title = "Bienvenidos al portal de administración Talento Humano Tickets"


