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
from tickets.views import  CreacionTickets
from django.conf.urls.static import  static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('chaining/', include('smart_selects.urls')),
    path('tickets/', views.menuAcceso),
    path('validaAcceso/', views.validaAcceso),
    path('salir/', views.salir),
    # Tickets
    path('validaAcceso/creacionTickets/', CreacionTickets.as_view(),name='creacion_ticketsA'),
    path('validaAcceso/creacionTickets/<str:username>,<str:sedeSeleccionada>,<str:nombreUsuario>,<str:nombreSede>,<str:empleadoId>', CreacionTickets.as_view(),name='creacion_ticketsA'),
    path('validaAcceso/creacionTickets/<int:pk>/', CreacionTickets.as_view(),name='creacion_ticketsB'),
    path('detail/', views.DetailTicket, name='detail'),
    path('load_dataTickets/<str:data>', views.load_dataTickets, name='loaddataTickets'),
    path('creacionTickets/postConsultaTicket/<str:id>,<str:username>,<str:empleadoId>/edit/', views.PostConsultaTicket,name='Post_editTicket'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Añadir
admin.site.site_header = 'Administracion Talento Humano Tickets'
admin.site.site_title = "Portal Talento Humano Tickets"
admin.site.index_title = "Bienvenidos al portal de administración Talento Humano Tickets"


