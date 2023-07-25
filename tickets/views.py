from django.shortcuts import render
from django.http import FileResponse
import psycopg2
import json
from django.views.generic import View
from django.views.generic import TemplateView
from tickets.models import Empleados, Tickets, MallaTurnos, TicketsMalla
from django.views.generic import FormView, CreateView, UpdateView, ListView
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.http import urlencode
# Create your views here.
from django.http import JsonResponse
from django.contrib import messages
from tickets.forms import ticketsForm, ticketsForm2, mallaTurnosForm, ticketsForm3, ticketsAsignacionForm
from datetime import date
from datetime import datetime
from calendar import monthrange

def menuAcceso(request):
    print ("Ingreso al Menu TH")
    context = {}

    # Sedes
    miConexion  = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432" , user="postgres", password="BD_m3d1c4l")
    cur = miConexion.cursor()
    comando = 'SELECT ltrim(codreg_sede), nom_sede FROM public.tickets_sedes'
    cur.execute(comando)
    print(comando)

    sedes = []

    for codreg_sede, nom_sede in cur.fetchall():
        sedes.append({'codreg_sede':codreg_sede, 'nom_sede' : nom_sede})
    miConexion.close()

    context['Sedes'] = sedes

    return render(request, "tickets/accesoPrincipal.html", context)


def validaAcceso(request):

    print ("Entre Acceso TH")
    context = {}

    # Sedes
    miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")


    comando = 'SELECT id, codreg_sede, nom_sede FROM public.tickets_sedes'
    cur.execute(comando)
    print(comando)

    sedes = []

    for id,codreg_sede, nom_sede in cur.fetchall():
        sedes.append({'id' : id, 'codreg_sede': codreg_sede, 'nom_sede': nom_sede})
    miConexion.close()

    context['Sedes'] = sedes
    print ("Aqui estan las sedes")
    print (context['Sedes'])

    username = request.POST["username"]
    contrasena = request.POST["password"]
    sedeSeleccionada   = request.POST["seleccion2"]
    print ("sedeSeleccionada = " , sedeSeleccionada)
    print("username = ", username)
    print ("contrasena = ", contrasena)
    context['Username'] = username
    context['SedeSeleccionada'] = sedeSeleccionada


    # Consigo Nombre de la sede

    miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres",
                              password="BD_m3d1c4l")
    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")

    comando = "SELECT id,codreg_sede, nom_sede FROM public.tickets_sedes WHERE codreg_sede = '" + sedeSeleccionada + "'"

    cur.execute(comando)
    print(comando)

    nombreSede = []

    for id,codreg_sede, nom_sede in cur.fetchall():
        nombreSede.append({'id' : id,'codreg_sede': codreg_sede, 'nom_sede': nom_sede})

    miConexion.close()

    context['NombreSede'] = nombreSede[0]['nom_sede']

    # Validacion Usuario existente

    miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres",   password="BD_m3d1c4l")

    #comando = 'SELECT empleado empleado, nombre nombre, sede sede FROM public.tickets_empleados WHERE "estadoReg" = ' + "'A'" + " and empleado = '" + username + "'"
    comando = 'SELECT id empleadoId,cedula cedula,nombre,sede_id sede, contrasena clave_usuario FROM public.tickets_empleados WHERE "estadoReg"  = ' + "'A'" + ' and cedula = ' + "'"+  str(username) + "'"

    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")
    print(comando)
    cur.execute(comando)

    nombreUsuario = []

    for empleadoId,cedula, nombre, sede  , clave_usuario in cur.fetchall():
        nombreUsuario.append({'empleadoId':empleadoId ,'cedula': cedula, 'nombre': nombre, 'sede':sede, 'clave_usuario':clave_usuario})

    print ("PASE 0")

    context['NombreUsuario'] = nombreUsuario[0]['nombre']
    context['EmpleadoId'] = nombreUsuario[0]['empleadoId']

    print ("PASE 1")

    print ("Asi quedo el nombre del usuario",  context['NombreUsuario'])
    miConexion.close()

    if nombreUsuario == []:

        context['Error'] = "Personal invalido y/o No Activo ! "
        print("Entre por personal No encontrado")

        return render(request, "tickets/accesoPrincipal.html", context)

        print("pase0")

    else:
        # Valido contraseña
        if nombreUsuario[0]['clave_usuario'] != contrasena:
            context['Error'] = "Contraseña invalida ! "
            return render(request, "tickets/accesoPrincipal.html", context)

        else:
            pass

            # Valido la Sede seleccinada

            miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres",
                                          password="BD_m3d1c4l")

            miConexion.set_client_encoding('LATIN1')
            cur = miConexion.cursor()
            cur.execute("set client_encoding='LATIN1';")

            comando = 'SELECT cedula cedula,nom_sede nom_sede , perf.nombre perfil FROM public.tickets_empleados usu, public.tickets_sedes sedes, public.tickets_tiposempleadosperfil perf WHERE usu.sede_id = sedes.id and usu."estadoReg" = ' + "'A" + "'" + " and  usu.cedula = '" + username + "' and sedes.codreg_sede =  '" + sedeSeleccionada + "'" + ' AND usu."tiposEmpleadoPerfil_id"=perf.id '
            print(comando)
            cur.execute(comando)

            permitido = []

            for cedula, nom_sede, perfil in cur.fetchall():
                permitido.append({'cedula': cedula, 'nom_sede': nom_sede, 'perfil':perfil})

            miConexion.close()



            if permitido == []:

                context['Error'] = "Usuario no tiene autorizacion para la sede seleccionada y/o Reportes no asignados ! "
                return render(request, "tickets/accesoPrincipal.html", context)

            else:
                pass
                print("Paso Autenticacion")
                context['Perfil'] = permitido[0]['perfil']

    print("Asi quedo el nombre del usuario", context['NombreUsuario'])
    return render(request, "tickets/cabeza.html", context)


def salir(request):
    print("Voy a salir TH")

    context = {}

    # Sedes
    miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres",
                                  password="BD_m3d1c4l")
    cur = miConexion.cursor()
    comando = 'SELECT ltrim(codreg_sede), nom_sede FROM public.tickets_sedes'
    cur.execute(comando)
    print(comando)

    sedes = []

    for codreg_sede, nom_sede in cur.fetchall():
        sedes.append({'codreg_sede': codreg_sede, 'nom_sede': nom_sede})
    miConexion.close()

    context['Sedes'] = sedes


    print("Aqui estan las sedes")
    print(context['Sedes'])

    return render(request, "tickets/accesoPrincipal.html", context)


class CreacionTickets(  CreateView ):
    print("Entre Creae View")
    form_class = ticketsForm
    model = Tickets
    #fields = ['sede','tiposTicket', 'fecha','empleado','sedeInicial','tiposTurnoInicial','desdeInicial','hastaInicial','sedeFinal','tiposTurnoFinal','desdeFinal','hastaFinal','adjunto']
    #fields = ['tiposTicket', 'fecha', 'empleado','sedeInicial','tiposTurnoInicial','desdeInicial','hastaInicial','adjunto','sedeFinal' ,'tiposTurnoFinal', 'desdeFinal','hastaFinal' ,'sedeReemplazo', 'reemplazo']

    template_name = 'tickets/tickets.html'

    #success_url = "/tickets/list"


    def get_initial(self):
        print ("initial = ", self.kwargs)
        initial = super(CreacionTickets, self).get_initial()
        initial['empleado'] = self.kwargs['empleadoId']

        return initial


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(" kwargs =", self.kwargs)
        print(" kwargs de get_context_data =", self.kwargs['username'])
        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']

        print ("context en el get_context_data = ", context)
        print(context["Username"])
        print(context["NombreUsuario"])
        print(context["NombreSede"])
        print(context["EmpleadoId"])
        print(context["SedeSeleccionada"])
        print(context["Perfil"])

        return context

    def form_valid(self, form):

        print ("FormaValida Clean = ",form.cleaned_data)

        #form.cleaned_data['empleado'] = self.kwargs['username']
        print("form.cleaned_data['empleado ya actualizada = ", form.cleaned_data['empleado'])
        instance = form.save()
        context={}
        #return HttpResponseRedirect(reverse_lazy('ticket:detail', args=[instance.id]))
        #redirect_url = reverse('CreacionTickets', args=(backend,))
        #ruta = reverse("creacion_ticketsA")
        #print ("ruta = ", ruta)
        #ruta2 = reverse_lazy("creacion_ticketsA")
        #print("ruta2 = ", ruta2)
        redirect_url = reverse('creacion_ticketsA')
        print ("redirect_url = ",redirect_url )
        #parameters = urlencode(form.cleaned_data)
        # return redirect(f'{redirect_url}?{parameters}')

        #parameters = urlencode(self.kwargs)
        envio=self.kwargs['username']+','+ self.kwargs['sedeSeleccionada']  + ',' + self.kwargs['nombreUsuario'] + ',' + self.kwargs['nombreSede'] + ','  + self.kwargs['empleadoId']
        #print ("parameters = " , parameters)
        #return redirect(f'{redirect_url}?{parameters}')
        #return redirect(f'{redirect_url}52888300,%20SJ,%20FERNANDEZ%20GARZON%20MARIA%20JIMENA%20,%20SEDE%20SANTA%20JULIANA,6')
        #return redirect(f'{redirect_url}52888300,SJ,FERNANDEZGARZONMARIAJIMENA,SEDESANTAJULIANA,6')
        print ("Envio = ", envio)

        return redirect(f'{redirect_url}{envio}')


        #return redirect('CreacionTickets', pk=0)
        #return render(self.request,'tickets/tickets.html' , context)
        #return HttpResponse(f"contact saved: {instance}")
        #form.instance.created_by = self.request.user
        #return super().form_valid(form)
        #form.instance.ticket = Ticket.objects.get(id=self.kwargs.get('pk'))

    #def form_invalid(self, form):
    #    print ("form is invalid")
    #    return HttpResponse("form is invalid.. this is just an HttpResponse object")

    def form_invalid(self, form):
        print("Entre form_invalid")
        response = super().form_invalid(form)
        print("pase1")
        print ("responde = ", response)
        if self.request.accepts('text/html'):
            print("pase2")

            return response
        else:
            print("pase3")
            return JsonResponse(form.errors, status=400)


def DetailTicket(request):
    print ("Entre DetailTicket")
    pass

# Create your views here.
def load_dataTickets(request, data):
    print ("Entre load_data Tickets")

    context = {}
    d = json.loads(data)

    sedeSeleccionada = d['sedeSeleccionada']
    username = d['username']
    nombreUsuario = d['nombreUsuario']

    nombreSede = d['nombreSede']
    empleadoId = d['empleadoId']

    #print("data = ", request.GET('data'))

    # Abro Conexion

    miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres", password="BD_m3d1c4l")
    # cur = miConexion.cursor()

    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")

    comando = 'SELECT ticket.id,ticket."tiposTicket_id",  tiposticket.nombre nombreTiposTicket , sede.nom_sede nom_sede,  emp.nombre nombre_empleado, to_char(ticket.fecha,' + "'" + "YYYY-MM-DD HH:MM.SS" + "')" + ',empleado_id,"sedeInicial_id","tiposTurnoInicial_id",tiposturno.nombre nombreTiposTurnoInicial,  to_char(ticket."desdeInicial",' + "'" + "YYYY-MM-DD HH:MM.SS" + "')" + ',to_char(ticket."hastaInicial",' + "'" + "YYYY-MM-DD HH:MM.SS" + "')"'   FROM tickets_tickets  ticket LEFT JOIN tickets_sedes sede on (sede.id = ticket."sedeInicial_id") INNER JOIN tickets_empleados emp  ON (emp.id = ticket.empleado_id) INNER JOIN tickets_tiposticket tiposticket ON (tiposticket.id = ticket."tiposTicket_id") LEFT JOIN tickets_tiposturno tiposturno   ON (tiposturno.id = ticket."tiposTurnoInicial_id" ) WHERE ticket.empleado_id = ' + "'" +  empleadoId + "'"
    print(comando)
    cur.execute(comando)

    tickets = []

    for id, tiposTicket_id, nombreTiposTicket, nom_sede, nombre_empleado, fecha, empleado, sedeInicial_id,tiposTurnoInicial_id,  nombreTiposTurnoInicial,desdeInicial, hastaInicial in cur.fetchall():
        tickets.append(
            {"model":"tickets.tickets","pk":id,"fields":
            {"id": id,
             "tiposTicket_id": tiposTicket_id,
             "nombreTiposTicket":nombreTiposTicket, "nom_sede" : nom_sede ,"nombre_empleado":nombre_empleado,
             "fecha": fecha, "empleado": empleado,
             "sedeInicial_id": sedeInicial_id,"tiposTurnoInicial_id": tiposTurnoInicial_id,
             "nombreTiposTurnoInicial":nombreTiposTurnoInicial,
             "desdeInicial": desdeInicial, "hastaInicial": hastaInicial}})

    miConexion.close()
    print("tickets")
    print(tickets)

    # Cierro Conexion

    context['Tickets'] = tickets

    ## Voy a enviar tickets

    serialized1 = json.dumps(tickets)

    print ("Envio = ", json)

    return HttpResponse(serialized1, content_type='application/json')


def PostConsultaTicket(request, id, username,empleadoId):
    print ("Entre POST edit Ticket")

    print ("username = ", username)
    print("id = ", id)
    print ("empleadoId = ", empleadoId)

    context = {}


    if request.method == 'GET':

        # Abro Conexion

        miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres",password="BD_m3d1c4l")
        # cur = miConexion.cursor()

        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        cur.execute("set client_encoding='LATIN1';")

        comando = 'SELECT ticket.id,ticket."tiposTicket_id",  tiposticket.nombre nombreTiposTicket ,to_char(ticket.fecha,' + "'" + "YYYY-MM-DD HH:MM.SS" + "')" + ',empleado_id empleado,"sedeInicial_id","tiposTurnoInicial_id",tiposturno.nombre nombreTiposTurnoInicial,  to_char(ticket."desdeInicial",' + "'" + "YYYY-MM-DD HH:MM.SS" + "')" + ',to_char(ticket."hastaInicial",' + "'" + "YYYY-MM-DD HH:MM.SS" + "')" + ',"sedeReemplazo_id" sedeReemplazo, reemplazo_id reemplazo, "respuestaEmpleadoCoordinador_id" respuestaEmpleadoCoordinador,coord.nombre nombreCoordinador,  "textoRespuestaCoordinador" textoRespuestaCoordinador, "estadoRespuestaCoordinador" estadoRespuestaCoordinador,"respuestaEmpleadoThumano_id" respuestaEmpleadoThumano, thumano.nombre nombreTHumano, "textoRespuestaThumano" textoRespuestaThumano,"estadoRespuestaThumano" estadoRespuestaThumano, "visibleTicketEmpleado" visibleTicketEmpleado  , emp.nombre nombreEmpleado, sedesi.nom_sede nomSedeinicial, sedesf.nom_sede nomSedeFinal, tiposturnof.nombre nombreTiposTurnoFinal,sedesr.nom_sede nomSedeReemplazo,empr.nombre nombreEmpleadoReemplazo    FROM tickets_tickets  ticket INNER JOIN tickets_tiposticket tiposticket ON (tiposticket.id = ticket."tiposTicket_id") LEFT JOIN tickets_tiposturno tiposturno   ON (tiposturno.id = ticket."tiposTurnoInicial_id" ) INNER JOIN tickets_empleados emp on (emp.id = ticket.empleado_id ) LEFT JOIN tickets_sedes sedesi on (sedesi.id = ticket."sedeInicial_id") LEFT JOIN tickets_sedes sedesf on (sedesf.id = ticket."sedeFinal_id") LEFT JOIN tickets_tiposturno tiposturnof on (tiposturnof.id = ticket."tiposTurnoFinal_id" ) LEFT JOIN tickets_sedes sedesr on (sedesr.id = ticket."sedeReemplazo_id") LEFT JOIN tickets_empleados empr on (empR.id = ticket.reemplazo_id ) LEFT JOIN tickets_empleados coord on (coord.id = ticket."respuestaEmpleadoCoordinador_id" ) LEFT JOIN tickets_empleados thumano on (thumano.id = ticket."respuestaEmpleadoThumano_id" )  WHERE  ticket.id = ' + "'" + id + "'"
        print(comando)
        cur.execute(comando)

        tickets = []

        for id, tiposTicket_id, nombreTiposTicket, fecha, empleado, sedeInicial_id, tiposTurnoInicial_id, nombreTiposTurnoInicial, desdeInicial, hastaInicial, sedeReemplazo,reemplazo, respuestaEmpleadoCoordinador, nombreCoordinador, textoRespuestaCoordinador, estadoRespuestaCoordinador, respuestaEmpleadoThumano ,nombreTHumano,textoRespuestaThumano, estadoRespuestaThumano,  visibleTicketEmpleado , nombreEmpleado, nomSedeinicial,  nomSedeFinal, nombreTiposTurnoFinal,  nomSedeReemplazo,  nombreEmpleadoReemplazo in cur.fetchall():
            tickets.append( {"id": id,
                     "tiposTicket_id": tiposTicket_id,
                     "nombreTiposTicket": nombreTiposTicket,
                     "fecha": fecha, "empleado": empleado,
                     "sedeInicial_id": sedeInicial_id, "tiposTurnoInicial_id": tiposTurnoInicial_id,
                     "nombreTiposTurnoInicial": nombreTiposTurnoInicial,
                     "desdeInicial": desdeInicial, "hastaInicial": hastaInicial,
                     "sedeReemplazo":sedeReemplazo,"reemplazo":reemplazo,"respuestaEmpleadoCoordinador":respuestaEmpleadoCoordinador,
                      "nombreCoordinador":nombreCoordinador,
                     "textoRespuestaCoordinador":textoRespuestaCoordinador,"estadoRespuestaCoordinador":estadoRespuestaCoordinador,
                     "respuestaEmpleadoThumano":respuestaEmpleadoThumano,
                      "nombreTHumano":nombreTHumano,  "textoRespuestaThumano":textoRespuestaThumano,
                    "estadoRespuestaThumano":estadoRespuestaThumano,"visibleTicketEmpleado":visibleTicketEmpleado ,
                     "nombreEmpleado":nombreEmpleado, "nomSedeinicial": nomSedeinicial,"nomSedeFinal":nomSedeFinal,
                     "nombreTiposTurnoFinal":nombreTiposTurnoFinal, "nomSedeReemplazo":nomSedeReemplazo,
                     "nombreEmpleadoReemplazo":nombreEmpleadoReemplazo

                             })

        miConexion.close()
        print("tickets")
        print(tickets)

        # Cierro Conexion
        print ("Me devuelvo a la MODAL")

        return JsonResponse({'pk':tickets[0]['id'],'tiposTicket_id':tickets[0]['tiposTicket_id'],'nombreTiposTicket':tickets[0]['nombreTiposTicket'],
                             'empleado':tickets[0]['empleado'],  'sedeInicial_id': tickets[0]['sedeInicial_id'],
                             'tiposTurnoInicial_id': tickets[0]['tiposTurnoInicial_id'], 'nombreTiposTurnoInicial':tickets[0]['nombreTiposTurnoInicial'],
                             'desdeInicial':tickets[0]['desdeInicial'],'hastaInicial':tickets[0]['hastaInicial'],
                             'sedeReemplazo': tickets[0]['sedeReemplazo'],  'reemplazo': tickets[0]['reemplazo'],
                             'respuestaEmpleadoCoordinador': tickets[0]['respuestaEmpleadoCoordinador'],
                             'nombreCoordinador': tickets[0]['nombreCoordinador'],

                             'textoRespuestaCoordinador': tickets[0]['textoRespuestaCoordinador'],
                             'estadoRespuestaCoordinador': tickets[0]['estadoRespuestaCoordinador'],
                             'respuestaEmpleadoThumano': tickets[0]['respuestaEmpleadoThumano'],
                             'nombreTHumano': tickets[0]['nombreTHumano'],

                             'textoRespuestaThumano': tickets[0]['textoRespuestaThumano'],'estadoRespuestaThumano': tickets[0]['estadoRespuestaThumano'],
                             'visibleTicketEmpleado': tickets[0]['visibleTicketEmpleado'],

                             'nombreEmpleado': tickets[0]['nombreEmpleado'],
                             'nomSedeinicial': tickets[0]['nomSedeinicial'],
                             'nomSedeFinal': tickets[0]['nomSedeFinal'],
                             'nombreTiposTurnoFinal': tickets[0]['nombreTiposTurnoFinal'],
                             'nomSedeReemplazo': tickets[0]['nomSedeReemplazo'],
                             'nombreEmpleadoReemplazo': tickets[0]['nombreEmpleadoReemplazo']

                              })
    else:
        return JsonResponse({'errors':'Something went wrong!'})


def load_asignacionTickets(request, data):
    print ("Entre load_asignacionTickets")

    context = {}
    d = json.loads(data)

    sedeSeleccionada = d['sedeSeleccionada']
    username = d['username']
    nombreUsuario = d['nombreUsuario']

    nombreSede = d['nombreSede']
    empleadoId = d['empleadoId']

    #print("data = ", request.GET('data'))

    # Abro Conexion

    miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres", password="BD_m3d1c4l")
    # cur = miConexion.cursor()

    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")

    comando = 'SELECT ticket.id,ticket."tiposTicket_id",  tiposticket.nombre nombreTiposTicket ,to_char(ticket.fecha,' + "'" + "YYYY-MM-DD HH:MM.SS" + "')" + ',empleado_id,"sedeInicial_id","tiposTurnoInicial_id",tiposturno.nombre nombreTiposTurnoInicial,  to_char(ticket."desdeInicial",' + "'" + "YYYY-MM-DD HH:MM.SS" + "')" + ',to_char(ticket."hastaInicial",' + "'" + "YYYY-MM-DD HH:MM.SS" + "')"'   FROM tickets_tickets  ticket INNER JOIN tickets_tiposticket tiposticket ON (tiposticket.id = ticket."tiposTicket_id") LEFT JOIN tickets_tiposturno tiposturno   ON (tiposturno.id = ticket."tiposTurnoInicial_id" ) WHERE ticket.asignado_id = ' + "''"
    print(comando)
    cur.execute(comando)

    asignacionTickets = []

    for id, tiposTicket_id, nombreTiposTicket, fecha, empleado, sedeInicial_id,tiposTurnoInicial_id,  nombreTiposTurnoInicial,desdeInicial, hastaInicial in cur.fetchall():
        asignacionTickets.append(
            {"model":"tickets.tickets","pk":id,"fields":
            {"id": id,
             "tiposTicket_id": tiposTicket_id,
             "nombreTiposTicket":nombreTiposTicket,
             "fecha": fecha, "empleado": empleado,
             "sedeInicial_id": sedeInicial_id,"tiposTurnoInicial_id": tiposTurnoInicial_id,
             "nombreTiposTurnoInicial":nombreTiposTurnoInicial,
             "desdeInicial": desdeInicial, "hastaInicial": hastaInicial}})

    miConexion.close()
    print("tickets")
    print(tickets)

    # Cierro Conexion

    context['AsignacionTickets'] = asignacionTickets

    ## Voy a enviar tickets

    serialized1 = json.dumps(tickets)

    print ("Envio = ", json)

    return HttpResponse(serialized1, content_type='application/json')

class AsignacionTickets(ListView):
    print ("Entre List View de AsignacionTickets : ")

    #model = Tickets
    #queryset = Tickets.objects.filter(asignado_id__isnull=True).order_by('id')

    #query = 'select t.id id,t."desdeInicial"  desdeInicial, t."hastaInicial" hastaInicial,t."empleado_id" empleado_id ,t."tiposTicket_id" tiposTicket_id,tip.nombre nombreTipo, emp.nombre nombreEmpleado from tickets_tickets t inner join tickets_tiposticket tip on (tip.id =  t."tiposTicket_id") inner join tickets_empleados emp on (emp.id =  t."empleado_id") WHERE asignado_id IS NULL order by t.id '
    #queryset =  Tickets.objects.raw(query)

    context_object_name = 'AsignacionTickets'
    paginate_by = 7
    template_name = 'tickets/asignacionTickets1.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        print ("Context asi viene del get_context del ListVoew = ", context)
        user = self.request.user

        print(" SELF de asignacion ticets = ", self.kwargs)
        print(" kwargs de ASIGNACION TICKETS = ", self.kwargs)

        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']

        print(context["Username"])
        print(context["NombreUsuario"])
        print(context["NombreSede"])
        print(context["EmpleadoId"])
        print(context["SedeSeleccionada"])
        print('Perfilll = ', context["Perfil"])

        return context

    def get_queryset(self):

        ticketId = self.kwargs['ticketId']
        empleadoNom = self.kwargs['nombre']
        perfil = self.kwargs['perfil']
        print ("perfil=", perfil)

        print ("empleadoNom =", empleadoNom)
        print ("kwargs de queryset",  self.kwargs)

        print ("CONCLUSION ticketId = ", ticketId)

        nombreSede = self.kwargs['nombreSede']
        print("nombreSede",nombreSede )

        try:

            if (perfil != 'TALENTO HUMANO'):
                return Tickets.objects.none()

            if (ticketId == '0' and empleadoNom == 'null'):
                # busqueda general
                print ("Entre todos los ticket= ",ticketId )
                #queryset = Tickets.objects.filter(asignado_id__isnull=True).order_by('id')
                queryset = Tickets.objects.filter(asignado_id__isnull=True).select_related('tiposTicket', 'empleado').order_by('-fecha','empleado_id')


            if (ticketId != '0' and empleadoNom == 'null'):
                # busqueda por ticket

                print("Entre por ticket = ", ticketId)
                queryset = Tickets.objects.filter(asignado_id__isnull=True, id=ticketId).order_by('-fecha','empleado_id')
                print("queryset = ", queryset)

            if (ticketId == '0' and empleadoNom != 'null'):
                ## busqueda por nombre
                print("Entre  por nombre = ", empleadoNom)
                #queryset = Tickets.objects.filter(asignado_id__isnull=True, empleado_id__contains=empleadoNom).select_related('empleado').order_by('id')
                queryset = Tickets.objects.select_related('empleado').filter(asignado_id__isnull=True,empleado_id__nombre__icontains=empleadoNom).order_by('-fecha','empleado_id')
                print("queryset = ", queryset)

            if (ticketId != '0' and empleadoNom != 'null'):
                ## busqueda por ticket, nombre
                print("Entre por ticket y por nombre = ", empleadoNom)
                queryset = Tickets.objects.select_related('empleado').filter(asignado_id__isnull=True, id=ticketId, empleado_id__nombre__icontains=empleadoNom).order_by('-fecha','empleado_id')
                print("queryset = ", queryset)


            return queryset.all()

        except Tickets.DoesNotExist:
            print ("sali posr exception")
            return Tickets.objects.none()


class AsignacionTicketsUpdate(UpdateView):
    print ("Entre AsignacionTicketsUpdate ")
    form_class = ticketsAsignacionForm
    model = Tickets

    #fields = ['id', 'tiposTicket', 'empleado','sedeInicial','desdeInicial','sedeFinal','hastaFinal', 'asignado']
    #fields = ['asignado']
    #context_object_name = 'AsignacionTicketsUpdate'
    template_name = 'tickets/asignacionTicketsUpdated.html'
    #success_url = reverse_lazy('asignacion_ticketsA')

    #def get_initial(self):
    #    print ("initial = ", self.kwargs)
    #    initial = super(CreacionTickets, self).get_initial()
    #    initial['empleado'] = self.kwargs['empleadoId']

    #    return initial

    def form_valid(self, form):
        print ("Entre Forma VALIDA")

        print ("forma valida sef.kwargs =" , self.kwargs)

        context = {}

        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']
        #self.get_context_data(   context=context )

        messages.success(self.request, "La asignacion fue satisfactoria.")
        return super(AsignacionTicketsUpdate, self).form_valid(form)


    def get_context_data(self, **kwargs):

        print ("Entre Contexto de Updated View")
        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(" kwargs de update = ", self.kwargs)

        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']

        print("context en el get_context_data AsignacionUpdated = ", context)
        print(context["Username"])
        print(context["NombreUsuario"])
        print(context["NombreSede"])
        print(context["EmpleadoId"])
        print(context["SedeSeleccionada"])

        print('Perfil = ', context["Perfil"])

        return context

    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        print ("Entre sucess url con kwargs = ", self.kwargs)


        username = self.kwargs['username']
        nombreUsuario = self.kwargs['nombreUsuario']
        nombreSede = self.kwargs['nombreSede']
        empleadoId = self.kwargs['empleadoId']
        sedeSeleccionada = self.kwargs['sedeSeleccionada']
        perfil = self.kwargs['perfil']

        return reverse_lazy('asignacion_ticketsA', kwargs={'ticketId':0,'nombre':'null', 'username':username,'nombreUsuario':nombreUsuario,'nombreSede': nombreSede,'empleadoId':empleadoId ,'sedeSeleccionada':sedeSeleccionada, 'perfil':perfil})

class Contrasena(UpdateView):
    print ("Entre Contrasena")
    model = Empleados
    fields = ['contrasena']
    template_name = 'tickets/contrasena.html'

    def get_context_data(self, **kwargs):

        print ("Entre Contexto de Updated View")
        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(" kwargs de update = ", self.kwargs)

        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']

        print("context en el get_context_data AsignacionUpdated = ", context)
        print(context["Username"])
        print(context["NombreUsuario"])
        print(context["NombreSede"])
        print(context["EmpleadoId"])
        print(context["SedeSeleccionada"])

        return context


    def form_valid(self, form):
        print ("Entre Forma VALIDA Contraseña")

        print ("forma valida sef.kwargs =" , self.kwargs)

        context = {}

        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']
        #self.get_context_data(   context=context )

        messages.success(self.request, "La asignacion fue satisfactoria.")
        return super(Contrasena, self).form_valid(form)


    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        print ("Entre sucess url con kwargs = ", self.kwargs)

        username = self.kwargs['username']
        nombreUsuario = self.kwargs['nombreUsuario']
        nombreSede = self.kwargs['nombreSede']
        empleadoId = self.kwargs['empleadoId']
        sedeSeleccionada = self.kwargs['sedeSeleccionada']

        #return reverse_lazy('tickets/', kwargs={'username':username,'nombreUsuario':nombreUsuario,'nombreSede': nombreSede,'empleadoId':empleadoId ,'sedeSeleccionada':sedeSeleccionada})

        return reverse_lazy('ticketsAcceso')


class GestionCoord(ListView):
    print ("Entre List View Gestion Coord")

    #model = Tickets
    #query = 'select t.id id,t."desdeInicial"  desdeInicial, t."hastaInicial" hastaInicial,t."empleado_id" empleado_id ,t."tiposTicket_id" tiposTicket_id,tip.nombre nombreTipo, emp.nombre nombreEmpleado from tickets_tickets t inner join tickets_tiposticket tip on (tip.id =  t."tiposTicket_id") inner join tickets_empleados emp on (emp.id =  t."empleado_id") WHERE asignado_id IS NULL order by t.id '
    #queryset =  Tickets.objects.raw(query)
    #queryset = Tickets.objects.filter( estadoRespuestaCoordinador='P').order_by('id')
    context_object_name = 'GestionCoord'
    paginate_by = 10
    template_name = 'tickets/gestionCoord2.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = self.request.user

        print(" SELF de asignacion ticets = ", self.kwargs)
        print(" kwargs de ASIGNACION TICKETS = ", self.kwargs)

        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']

        sedeMalla = self.kwargs['sedeMalla']
        areaMalla = self.kwargs['areaMalla']
        nombreMalla = self.kwargs['nombreMalla']


        sedeSeleccionada = self.kwargs['sedeSeleccionada']
        empleadoId = self.kwargs['empleadoId']
        sedeSeleccionada=sedeSeleccionada.replace(' ','')
        print ("sedeSeleccionada=",sedeSeleccionada )


        print(context["Username"])
        print(context["NombreUsuario"])
        print(context["NombreSede"])
        print(context["EmpleadoId"])
        print(context["SedeSeleccionada"])

        ## Consigo el id del Area del empleado

        ## Fin area del Coordinador

        miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres",               password="BD_m3d1c4l")
        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        cur.execute("set client_encoding='LATIN1';")

        comando = "SELECT emp.area_id empArea FROM public.tickets_empleados emp  WHERE id = " + str(empleadoId)

        cur.execute(comando)
        print(comando)

        empAreas = []


        for empArea in cur.fetchall():
            empAreas.append({'empArea': empArea})

        miConexion.close()

        context['EmpArea'] = empAreas

        # Consigo las areas

        miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres", password="BD_m3d1c4l")
        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        cur.execute("set client_encoding='LATIN1';")

        comando = "SELECT area.id id, area.nombre nombre FROM public.tickets_areas area, public.tickets_sedes sedes  WHERE area.sedes_id = area.sedes_id AND sedes.codreg_sede = '" + sedeSeleccionada + "'"

        cur.execute(comando)
        print(comando)

        areas = []
        areas.append({'id': '' , 'nombre': ' '})


        for id, nombre in cur.fetchall():
            areas.append({'id': id, 'nombre': nombre})

        miConexion.close()

        context['Areas'] = areas

        if (areaMalla == "99"):
            context['AreaMalla'] = areas[0]['id']
        else:
            context['AreaMalla'] = areaMalla
        print("sede malla de arranque = ", context['AreaMalla'])


        # Consigo Sedes

        miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        cur.execute("set client_encoding='LATIN1';")

        comando = 'SELECT sedes.id id, sedes.nom_sede nombre FROM public.tickets_sedes sedes WHERE "estadoReg" = ' + "'A'"

        cur.execute(comando)
        print(comando)

        sedes = []
        #sedes.append({'id': '', 'nombre': ' '})

        for id, nombre in cur.fetchall():
            sedes.append({'id': id, 'nombre': nombre})

        miConexion.close()

        context['Sedes'] = sedes

        # Fin consigo sede
        if (sedeMalla == "99"):
            context['SedeMalla'] = sedes[0]['id']
        else:
            context['SedeMalla'] = sedeMalla
        print ("sede malla de arranque = " ,context['SedeMalla'] )





        # Día actual
        today = date.today()

        # Fecha actual
        now = datetime.now()

        print(today.year)
        print(today.month)
        AnoActual = today.year
        MesActual = today.month

        #context['Ano'] = today.year
        #context['Mes'] = today.month

        print ("estos son los kwargs")

        print ("ano =", self.kwargs['ano'])
        print ("mes =", self.kwargs['mes'])

        print("FIN estos son los kwargs")


        if (self.kwargs['ano'] == "99"):
            context['Ano'] = today.year
        else:
            context['Ano'] = self.kwargs['ano']

        if (self.kwargs['mes'] == "99"):
            context['Mes'] = today.month
        else:
            if (self.kwargs['mes'] == "0"):
                context['Mes'] = ''
            else:
                context['Mes'] = self.kwargs['mes']




        context['Nombremalla'] = nombreMalla


        ## Aqui conformo el calendario

        miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        cur.execute("set client_encoding='LATIN1';")

        comando = "SELECT dia dia, nombre nombre FROM public.tickets_calendario WHERE ano =" + str(AnoActual) + ' AND mes = ' + str(MesActual) + ' ORDER BY dia  '

        cur.execute(comando)
        print(comando)

        calendario = []


        for dia, nombre in cur.fetchall():
            calendario.append({'dia': dia, 'nombre': nombre})

        miConexion.close()

        for x in range(0, len(calendario)):
            print(calendario[x])
            campo = calendario[x]
            #print ("campo1 = ", campo1)
            #campo = json.loads(campo1)
            print("campo = ", campo)
            print(campo['dia'])
            print(campo['nombre'])
            if (x==0):
                context['uno'] = campo['nombre']
            if (x==1):
                context['dos'] = campo['nombre']
            if (x == 2):
                context['tres'] = campo['nombre']
            if (x==3):
                context['cuatro'] = campo['nombre']
            if (x==4):
                context['cinco'] = campo['nombre']
            if (x==5):
                context['seis'] = campo['nombre']
            if (x==6):
                context['siete'] = campo['nombre']
            if (x==7):
                context['ocho'] = campo['nombre']
            if (x==8):
                context['nueve'] = campo['nombre']
            if (x==9):
                context['diez'] = campo['nombre']
            if (x==10):
                context['once'] = campo['nombre']
            if (x==11):
                context['doce'] = campo['nombre']
            if (x==12):
                context['trece'] = campo['nombre']

            if (x==13):
                context['catorce'] = campo['nombre']

            if (x==14):
                context['quince'] = campo['nombre']
            if (x==15):
                context['diezyseis'] = campo['nombre']
            if (x==16):
                context['diezysiete'] = campo['nombre']
            if (x==17):
                context['diezyocho'] = campo['nombre']
            if (x==18):
                context['diezynueve'] = campo['nombre']
            if (x==19):
                context['veinte'] = campo['nombre']
            if (x==20):
                context['veintiuno'] = campo['nombre']
            if (x==21):
                context['veintidos'] = campo['nombre']
            if (x==22):
                context['veintitres'] = campo['nombre']
            if (x==23):
                context['veinticuatro'] = campo['nombre']
            if (x==24):
                context['veinticinco'] = campo['nombre']
            if (x==25):
                context['veintiseis'] = campo['nombre']
            if (x==26):
                context['veintisiete'] = campo['nombre']
            if (x==27):
                context['veintiocho'] = campo['nombre']
            if (x == 28):
                    context['veintinueve'] = campo['nombre']
            if (x==29):
                context['treinta'] = campo['nombre']
            if (x==30):
                context['treintayuno'] = campo['nombre']
            if (x==31):
                context['treintaydos'] = campo['nombre']

        ## Fin conformo em calendario




        return context

    def get_queryset(self):
        empleadoId = self.kwargs['empleadoId']
        perfil = self.kwargs['perfil']
        print ("Entre querySet de GestionCoord  ")
        print ("empleadoId", empleadoId)
        print("perfil DEL COORINADOR ES : ", perfil)
        try:

            if (perfil == 'COLABORADOR'):
                print ("Entre NO ENTREGO PAGINA A COLABORADOR")
                return Tickets.objects.none()

            print("ANTES DE OJOOO queryset = ")
            #queryset = Tickets.objects.filter(asignado_id=empleadoId, estadoRespuestaCoordinador='Pendiente', tickets__empleados_set__id=empleado).order_by('id')

            queryset =Tickets.objects.filter(asignado_id=empleadoId, estadoRespuestaCoordinador='Pendiente').select_related('tiposTicket', 'empleado').order_by('-fecha','empleado_id')

            print ("OJOOO queryset = ",queryset )
            return queryset.all()
        except Tickets.DoesNotExist:
            return Empleados.objects.none()

def GestionCoordDelete(request, pk,username,sedeSeleccionada,nombreUsuario, nombreSede, empleadoId,perfil,ano,mes,sedeMalla,areaMalla,nombreMalla):
    print ("Entre a BORRAR la malla")
    mallaturnos = MallaTurnos.objects.get(id=pk)
    try:
        mallaturnos.delete()

    except Exception as X:
        print("ESTA ES LA EXCEPCION", X)

        #envio = username + ',' + sedeSeleccionada + ',' + nombreUsuario + ',' + nombreSede + ',' + empleadoId + ',' + perfil + ',' + ano + ',' + mes + ',' + sedeMalla + ',' + areaMalla + ',' + nombreMalla
        #redirect_url = reverse('gestionCoord' + '/' + envio + '/')

        #return reverse_lazy('gestionCoord', kwargs={'username': username, 'nombreUsuario': nombreUsuario, 'nombreSede': nombreSede,                                    'empleadoId': empleadoId, 'sedeSeleccionada': sedeSeleccionada, 'perfil': perfil,                                    'ano': ano, 'mes': mes, 'sedeMalla': sedeMalla, 'areaMalla': areaMalla,                                    'nombreMalla': nombreMalla})

        #return redirect(f'{redirect_url}{envio}')

        #return render (request,   )

        #return HttpResponse(X)
        return HttpResponseRedirect(reverse('gestionCoord', kwargs={'username': username, 'nombreUsuario': nombreUsuario, 'nombreSede': nombreSede, 'empleadoId': empleadoId, 'sedeSeleccionada': sedeSeleccionada, 'perfil': perfil, 'ano': ano, 'mes': mes, 'sedeMalla': sedeMalla,  'areaMalla': areaMalla, 'nombreMalla': nombreMalla}), X)

    # Ademas de que aquip hay que ingresar la auditoria de ticketsmalla diciendo quien borro la malla
    return HttpResponseRedirect(reverse('gestionCoord', kwargs={'username': username, 'nombreUsuario': nombreUsuario, 'nombreSede': nombreSede,'empleadoId': empleadoId, 'sedeSeleccionada': sedeSeleccionada, 'perfil': perfil, 'ano': ano, 'mes': mes, 'sedeMalla': sedeMalla, 'areaMalla': areaMalla,'nombreMalla': nombreMalla}))


class GestionCoordUpdate(UpdateView):
    print ("Entre GestionCoordUpdate ")
    form_class = ticketsForm2
    model = Tickets
    #fields = ['id', 'tiposTicket', 'empleado','sedeInicial','desdeInicial','sedeFinal','hastaFinal', 'asignado']
    #fields = ['asignado']
    context_object_name = 'gestionCoordUpdate'
    template_name = 'tickets/gestionCoordUpdated.html'
    success_url = reverse_lazy('gestionCoord')

    #def get_initial(self):
    #    print ("initial = ", self.kwargs)
    #    initial = super(CreacionTickets, self).get_initial()
    #    initial['empleado'] = self.kwargs['empleadoId']

    #    return initial

    def form_valid(self, form):
        print ("Entre Forma VALIDA GestionCoordUpdate ")

        print ("forma valida sef.kwargs =" , self.kwargs)
        #form.cleaned_data['respuestaEmpleadoCoordinador'] = self.kwargs['empleadoId']

        #print ("La forma cleaned_data quedo = ",  form.cleaned_data['respuestaEmpleadoCoordinador'])
        form.instance.save()

        print ("acabe de grabar la actualziacion de GETIONUPDATE")

        context = {}

        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']

        context["Ano"] = self.kwargs['ano']
        context["Mes"] = self.kwargs['mes']
        context["SedeMalla"] = self.kwargs['sedeMalla']
        context["AreaMalla"] = self.kwargs['areaMalla']
        context["NombreMalla"] = self.kwargs['nombreMalla']




        #self.get_context_data(   context=context )

        messages.success(self.request, "La asignacion fue satisfactoria.")
        return super(GestionCoordUpdate, self).form_valid(form)



    def get_context_data(self, **kwargs):

        print ("Entre Contexto de Updated View GestionCoordUpdate")
        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(" kwargs de update = ", self.kwargs)

        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']

        context["SedeMalla"] = self.kwargs['sedeMalla']
        context["AreaMalla"] = self.kwargs['areaMalla']
        context["NombreMalla"] = self.kwargs['nombreMalla']
        context["Ano"] = self.kwargs['ano']
        context["Mes"] = self.kwargs['mes']

        print("context en el get_context_data AsignacionUpdated = ", context)
        print(context["Username"])
        print(context["NombreUsuario"])
        print(context["NombreSede"])
        print(context["EmpleadoId"])
        print(context["SedeSeleccionada"])

        return context

    def get_initial(self):
        print("initial = ", self.kwargs)
        initial = super(GestionCoordUpdate, self).get_initial()
        initial['respuestaEmpleadoCoordinador'] = self.kwargs['empleadoId']

        return initial


    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        print ("Entre sucess url con kwargs  GestionCoordUpdate = ", self.kwargs)


        username = self.kwargs['username']
        nombreUsuario = self.kwargs['nombreUsuario']
        nombreSede = self.kwargs['nombreSede']
        empleadoId = self.kwargs['empleadoId']
        sedeSeleccionada = self.kwargs['sedeSeleccionada']
        perfil = self.kwargs['perfil']

        sedeMalla = self.kwargs['sedeMalla']
        areaMalla = self.kwargs['areaMalla']
        nombreMalla = self.kwargs['nombreMalla']
        ano = self.kwargs['ano']
        mes = self.kwargs['mes']


        return reverse_lazy('gestionCoord', kwargs={'username':username,'nombreUsuario':nombreUsuario,'nombreSede': nombreSede,'empleadoId':empleadoId ,'sedeSeleccionada':sedeSeleccionada, 'perfil':perfil, 'ano':ano, 'mes':mes, 'sedeMalla':sedeMalla, 'areaMalla': areaMalla, 'nombreMalla':nombreMalla})


# Create your views here.
def load_dataCoordTickets(request, data):

    print ("Entre load_data Tickets de Gestion Coordinador")

    print ("request =", request)
    print("dataCompleta =", data)

    context = {}
    d = json.loads(data)

    sedeSeleccionada = d['sedeSeleccionada']
    username = d['username']
    nombreUsuario = d['nombreUsuario']

    nombreSede = d['nombreSede']
    empleadoId = d['empleadoId']
    nombreEmp  = d['nombreEmp']

    areaMalla = d['areaMalla']
    sedeMalla = d['sedeMalla']
    nombreMalla = d['nombreMalla']

    sede = d['sede']

    area = d['area']
    ano = d['ano']
    mes = d['mes']
    perfil = d['perfil']
    print("sede        =", sede)
    print("sedeMalla   =", sedeMalla)
    print("llega nombreEmp ORIGINA =", nombreEmp)

    nombreEmp1=''


    if (nombreEmp == "" or nombreEmp=="0"):
        print ("Entre a cambiar nombreEmp1")
        nombreEmp1 = '0'

    if (sede == ''):
        sede = 0

    if (area==''):
        area=0

    if (mes==''):
        mes=0

    if (ano==''):
        ano=0

    print("llega sede=", sede)
    print("llega area=", area)
    print("llega ano=", ano)
    print("llega mes=", mes)
    print("llega nombreEmp1=", nombreEmp1   )

    #print("data = ", request.GET('data'))

    # Abro Conexion

    miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres", password="BD_m3d1c4l")
    # cur = miConexion.cursor()

    miConexion.set_client_encoding('LATIN1')
    cur = miConexion.cursor()
    cur.execute("set client_encoding='LATIN1';")

    #comando = 'select malla.id  id, empleado_id  empleado_id,emp.nombre nombreEmpleado,  malla.area_id  area_id, area.nombre nombreArea, ano, mes ,   tur1.abrev dia1,  tur2.abrev dia2 ,   tur3.abrev dia3 , tur4.abrev dia4 ,  tur5.abrev dia5  ,  tur6.abrev dia6  , tur7.abrev dia7  ,  tur8.abrev  dia8,  tur9.abrev dia9 , tur10.abrev dia10 ,  tur11.abrev dia11,  tur12.abrev dia12,  tur13.abrev dia13,tur14.abrev dia14 ,  tur15.abrev dia15,  tur16.abrev dia16,  tur17.abrev dia17 ,  tur18.abrev dia18 ,  tur19.abrev dia19,  tur20.abrev dia20 ,  tur21.abrev dia21 ,  tur22.abrev dia22 ,  tur23.abrev dia23,  tur24.abrev dia24,  tur25.abrev dia25 ,  tur26.abrev dia26 ,  tur27.abrev dia27 ,  tur28.abrev dia28 ,  tur29.abrev dia29 ,   tur30.abrev dia30 , tur31.abrev dia31 FROM tickets_mallaturnos  malla INNER JOIN tickets_empleados emp on (emp.id = malla.empleado_id) INNER JOIN tickets_areas area on (area.id = malla.area_id) LEFT JOIN tickets_tiposturno tur1   ON (tur1.id = malla.dia1_id) LEFT JOIN tickets_tiposturno tur2   ON (tur2.id = malla.dia2_id) LEFT JOIN tickets_tiposturno tur3   ON (tur3.id = malla.dia3_id) LEFT JOIN tickets_tiposturno tur4   ON (tur4.id = malla.dia4_id) LEFT JOIN tickets_tiposturno tur5   ON (tur5.id = malla.dia5_id) LEFT JOIN tickets_tiposturno tur6   ON (tur6.id = malla.dia6_id) LEFT JOIN tickets_tiposturno tur7   ON (tur7.id = malla.dia7_id) LEFT JOIN tickets_tiposturno tur8   ON (tur8.id = malla.dia8_id) LEFT JOIN tickets_tiposturno tur9   ON (tur9.id = malla.dia9_id) LEFT JOIN tickets_tiposturno tur10   ON (tur10.id = malla.dia10_id) LEFT JOIN tickets_tiposturno tur11   ON (tur11.id = malla.dia11_id) LEFT JOIN tickets_tiposturno tur12   ON (tur12.id = malla.dia12_id) LEFT JOIN tickets_tiposturno tur13   ON (tur13.id = malla.dia13_id) LEFT JOIN tickets_tiposturno tur14   ON (tur14.id = malla.dia14_id) LEFT JOIN tickets_tiposturno tur15   ON (tur15.id = malla.dia15_id) LEFT JOIN tickets_tiposturno tur16   ON (tur16.id = malla.dia16_id) LEFT JOIN tickets_tiposturno tur17   ON (tur17.id = malla.dia17_id) LEFT JOIN tickets_tiposturno tur18   ON (tur18.id = malla.dia18_id) LEFT JOIN tickets_tiposturno tur19   ON (tur19.id = malla.dia19_id) LEFT JOIN tickets_tiposturno tur20   ON (tur20.id = malla.dia20_id) LEFT JOIN tickets_tiposturno tur21   ON (tur21.id = malla.dia21_id) LEFT JOIN tickets_tiposturno tur22   ON (tur22.id = malla.dia22_id) LEFT JOIN tickets_tiposturno tur23   ON (tur23.id = malla.dia23_id) LEFT JOIN tickets_tiposturno tur24   ON (tur24.id = malla.dia24_id) LEFT JOIN tickets_tiposturno tur25   ON (tur25.id = malla.dia25_id) LEFT JOIN tickets_tiposturno tur26   ON (tur26.id = malla.dia26_id) LEFT JOIN tickets_tiposturno tur27   ON (tur27.id = malla.dia27_id) LEFT JOIN tickets_tiposturno tur28   ON (tur28.id = malla.dia28_id) LEFT JOIN tickets_tiposturno tur29   ON (tur29.id = malla.dia29_id) LEFT JOIN tickets_tiposturno tur30   ON (tur30.id = malla.dia30_id) LEFT JOIN tickets_tiposturno tur31   ON (tur31.id = malla.dia31_id) where malla.ano = 2023'

    if (nombreEmp1 != "0"):
        print ("Entre POR nombre1 <> 0 =", nombreEmp1)
        comando = 'select  malla.id  id,sedes.nom_sede nom_sede,  empleado_id  empleado_id,emp.nombre nombreEmpleado  ,  malla.area_id  area_id, area.nombre nombreArea, ano, mes ,   tur1.abrev dia1,  tur2.abrev dia2 ,   tur3.abrev dia3 , tur4.abrev dia4 ,  tur5.abrev dia5  ,  tur6.abrev dia6  , tur7.abrev dia7  ,  tur8.abrev  dia8,  tur9.abrev dia9 , tur10.abrev dia10 ,  tur11.abrev dia11,  tur12.abrev dia12,  tur13.abrev dia13,tur14.abrev dia14 ,  tur15.abrev dia15,  tur16.abrev dia16,  tur17.abrev dia17 ,  tur18.abrev dia18 ,  tur19.abrev dia19,  tur20.abrev dia20 ,  tur21.abrev dia21 ,  tur22.abrev dia22 ,  tur23.abrev dia23,  tur24.abrev dia24,  tur25.abrev dia25 ,  tur26.abrev dia26 ,  tur27.abrev dia27 ,  tur28.abrev dia28 ,  tur29.abrev dia29 ,   tur30.abrev dia30 , tur31.abrev dia31 FROM tickets_mallaturnos  malla   INNER JOIN tickets_empleados emp on (emp.id = malla.empleado_id) INNER JOIN tickets_sedes sedes on (1=1) INNER JOIN tickets_areas area on (area.sedes_id = sedes.id AND area.id = malla.area_id)  LEFT JOIN tickets_tiposturno tur1   ON (tur1.id = malla.dia1_id) LEFT JOIN tickets_tiposturno tur2   ON (tur2.id = malla.dia2_id) LEFT JOIN tickets_tiposturno tur3   ON (tur3.id = malla.dia3_id) LEFT JOIN tickets_tiposturno tur4   ON (tur4.id = malla.dia4_id) LEFT JOIN tickets_tiposturno tur5   ON (tur5.id = malla.dia5_id) LEFT JOIN tickets_tiposturno tur6   ON (tur6.id = malla.dia6_id) LEFT JOIN tickets_tiposturno tur7   ON (tur7.id = malla.dia7_id) LEFT JOIN tickets_tiposturno tur8   ON (tur8.id = malla.dia8_id) LEFT JOIN tickets_tiposturno tur9   ON (tur9.id = malla.dia9_id) LEFT JOIN tickets_tiposturno tur10   ON (tur10.id = malla.dia10_id) LEFT JOIN tickets_tiposturno tur11   ON (tur11.id = malla.dia11_id) LEFT JOIN tickets_tiposturno tur12   ON (tur12.id = malla.dia12_id) LEFT JOIN tickets_tiposturno tur13   ON (tur13.id = malla.dia13_id) LEFT JOIN tickets_tiposturno tur14   ON (tur14.id = malla.dia14_id) LEFT JOIN tickets_tiposturno tur15   ON (tur15.id = malla.dia15_id) LEFT JOIN tickets_tiposturno tur16   ON (tur16.id = malla.dia16_id) LEFT JOIN tickets_tiposturno tur17   ON (tur17.id = malla.dia17_id) LEFT JOIN tickets_tiposturno tur18   ON (tur18.id = malla.dia18_id) LEFT JOIN tickets_tiposturno tur19   ON (tur19.id = malla.dia19_id) LEFT JOIN tickets_tiposturno tur20   ON (tur20.id = malla.dia20_id) LEFT JOIN tickets_tiposturno tur21   ON (tur21.id = malla.dia21_id) LEFT JOIN tickets_tiposturno tur22   ON (tur22.id = malla.dia22_id) LEFT JOIN tickets_tiposturno tur23   ON (tur23.id = malla.dia23_id) LEFT JOIN tickets_tiposturno tur24   ON (tur24.id = malla.dia24_id) LEFT JOIN tickets_tiposturno tur25   ON (tur25.id = malla.dia25_id) LEFT JOIN tickets_tiposturno tur26   ON (tur26.id = malla.dia26_id) LEFT JOIN tickets_tiposturno tur27   ON (tur27.id = malla.dia27_id) LEFT JOIN tickets_tiposturno tur28   ON (tur28.id = malla.dia28_id) LEFT JOIN tickets_tiposturno tur29   ON (tur29.id = malla.dia29_id) LEFT JOIN tickets_tiposturno tur30   ON (tur30.id = malla.dia30_id) LEFT JOIN tickets_tiposturno tur31   ON (tur31.id = malla.dia31_id) where  sedes.id = ' + str(sede) + " AND emp.nombre like ('%" + str(nombreEmp) + "%')" + ' ORDER BY  malla.ano, malla.mes, malla.area_id '

    if (nombreEmp1=="0"):
        print("Entre POR nombre1 IGUAL A 0 = ", nombreEmp1)
        if (sede != 0):

            if (area==0):
                comando = 'select  malla.id  id,sedes.nom_sede nom_sede,  empleado_id  empleado_id,emp.nombre nombreEmpleado  ,  malla.area_id  area_id, area.nombre nombreArea, ano, mes ,   tur1.abrev dia1,  tur2.abrev dia2 ,   tur3.abrev dia3 , tur4.abrev dia4 ,  tur5.abrev dia5  ,  tur6.abrev dia6  , tur7.abrev dia7  ,  tur8.abrev  dia8,  tur9.abrev dia9 , tur10.abrev dia10 ,  tur11.abrev dia11,  tur12.abrev dia12,  tur13.abrev dia13,tur14.abrev dia14 ,  tur15.abrev dia15,  tur16.abrev dia16,  tur17.abrev dia17 ,  tur18.abrev dia18 ,  tur19.abrev dia19,  tur20.abrev dia20 ,  tur21.abrev dia21 ,  tur22.abrev dia22 ,  tur23.abrev dia23,  tur24.abrev dia24,  tur25.abrev dia25 ,  tur26.abrev dia26 ,  tur27.abrev dia27 ,  tur28.abrev dia28 ,  tur29.abrev dia29 ,   tur30.abrev dia30 , tur31.abrev dia31 FROM tickets_mallaturnos  malla   INNER JOIN tickets_empleados emp on (emp.id = malla.empleado_id)  INNER JOIN tickets_sedes sedes on (1=1) INNER JOIN tickets_areas area on (area.sedes_id = sedes.id AND area.id = malla.area_id)  LEFT JOIN tickets_tiposturno tur1   ON (tur1.id = malla.dia1_id) LEFT JOIN tickets_tiposturno tur2   ON (tur2.id = malla.dia2_id) LEFT JOIN tickets_tiposturno tur3   ON (tur3.id = malla.dia3_id) LEFT JOIN tickets_tiposturno tur4   ON (tur4.id = malla.dia4_id) LEFT JOIN tickets_tiposturno tur5   ON (tur5.id = malla.dia5_id) LEFT JOIN tickets_tiposturno tur6   ON (tur6.id = malla.dia6_id) LEFT JOIN tickets_tiposturno tur7   ON (tur7.id = malla.dia7_id) LEFT JOIN tickets_tiposturno tur8   ON (tur8.id = malla.dia8_id) LEFT JOIN tickets_tiposturno tur9   ON (tur9.id = malla.dia9_id) LEFT JOIN tickets_tiposturno tur10   ON (tur10.id = malla.dia10_id) LEFT JOIN tickets_tiposturno tur11   ON (tur11.id = malla.dia11_id) LEFT JOIN tickets_tiposturno tur12   ON (tur12.id = malla.dia12_id) LEFT JOIN tickets_tiposturno tur13   ON (tur13.id = malla.dia13_id) LEFT JOIN tickets_tiposturno tur14   ON (tur14.id = malla.dia14_id) LEFT JOIN tickets_tiposturno tur15   ON (tur15.id = malla.dia15_id) LEFT JOIN tickets_tiposturno tur16   ON (tur16.id = malla.dia16_id) LEFT JOIN tickets_tiposturno tur17   ON (tur17.id = malla.dia17_id) LEFT JOIN tickets_tiposturno tur18   ON (tur18.id = malla.dia18_id) LEFT JOIN tickets_tiposturno tur19   ON (tur19.id = malla.dia19_id) LEFT JOIN tickets_tiposturno tur20   ON (tur20.id = malla.dia20_id) LEFT JOIN tickets_tiposturno tur21   ON (tur21.id = malla.dia21_id) LEFT JOIN tickets_tiposturno tur22   ON (tur22.id = malla.dia22_id) LEFT JOIN tickets_tiposturno tur23   ON (tur23.id = malla.dia23_id) LEFT JOIN tickets_tiposturno tur24   ON (tur24.id = malla.dia24_id) LEFT JOIN tickets_tiposturno tur25   ON (tur25.id = malla.dia25_id) LEFT JOIN tickets_tiposturno tur26   ON (tur26.id = malla.dia26_id) LEFT JOIN tickets_tiposturno tur27   ON (tur27.id = malla.dia27_id) LEFT JOIN tickets_tiposturno tur28   ON (tur28.id = malla.dia28_id) LEFT JOIN tickets_tiposturno tur29   ON (tur29.id = malla.dia29_id) LEFT JOIN tickets_tiposturno tur30   ON (tur30.id = malla.dia30_id) LEFT JOIN tickets_tiposturno tur31   ON (tur31.id = malla.dia31_id) where  sedes.id = ' + str(sede) + ' AND malla.ano = ' + str(ano)  + ' AND malla.mes = ' + str(mes) + ' ORDER BY  malla.ano, malla.mes, malla.area_id '
                if (ano == 0):
                    comando = 'select malla.id  id,sedes.nom_sede nom_sede, empleado_id  empleado_id,emp.nombre nombreEmpleado,  malla.area_id  area_id, area.nombre nombreArea, ano, mes ,   tur1.abrev dia1,  tur2.abrev dia2 ,   tur3.abrev dia3 , tur4.abrev dia4 ,  tur5.abrev dia5  ,  tur6.abrev dia6  , tur7.abrev dia7  ,  tur8.abrev  dia8,  tur9.abrev dia9 , tur10.abrev dia10 ,  tur11.abrev dia11,  tur12.abrev dia12,  tur13.abrev dia13,tur14.abrev dia14 ,  tur15.abrev dia15,  tur16.abrev dia16,  tur17.abrev dia17 ,  tur18.abrev dia18 ,  tur19.abrev dia19,  tur20.abrev dia20 ,  tur21.abrev dia21 ,  tur22.abrev dia22 ,  tur23.abrev dia23,  tur24.abrev dia24,  tur25.abrev dia25 ,  tur26.abrev dia26 ,  tur27.abrev dia27 ,  tur28.abrev dia28 ,  tur29.abrev dia29 ,   tur30.abrev dia30 , tur31.abrev dia31 FROM tickets_mallaturnos  malla INNER JOIN tickets_empleados emp on (emp.id = malla.empleado_id)  INNER JOIN tickets_sedes sedes on (1=1)   INNER JOIN tickets_areas area on (area.sedes_id = sedes.id AND area.id = malla.area_id) LEFT JOIN tickets_tiposturno tur1   ON (tur1.id = malla.dia1_id) LEFT JOIN tickets_tiposturno tur2   ON (tur2.id = malla.dia2_id) LEFT JOIN tickets_tiposturno tur3   ON (tur3.id = malla.dia3_id) LEFT JOIN tickets_tiposturno tur4   ON (tur4.id = malla.dia4_id) LEFT JOIN tickets_tiposturno tur5   ON (tur5.id = malla.dia5_id) LEFT JOIN tickets_tiposturno tur6   ON (tur6.id = malla.dia6_id) LEFT JOIN tickets_tiposturno tur7   ON (tur7.id = malla.dia7_id) LEFT JOIN tickets_tiposturno tur8   ON (tur8.id = malla.dia8_id) LEFT JOIN tickets_tiposturno tur9   ON (tur9.id = malla.dia9_id) LEFT JOIN tickets_tiposturno tur10   ON (tur10.id = malla.dia10_id) LEFT JOIN tickets_tiposturno tur11   ON (tur11.id = malla.dia11_id) LEFT JOIN tickets_tiposturno tur12   ON (tur12.id = malla.dia12_id) LEFT JOIN tickets_tiposturno tur13   ON (tur13.id = malla.dia13_id) LEFT JOIN tickets_tiposturno tur14   ON (tur14.id = malla.dia14_id) LEFT JOIN tickets_tiposturno tur15   ON (tur15.id = malla.dia15_id) LEFT JOIN tickets_tiposturno tur16   ON (tur16.id = malla.dia16_id) LEFT JOIN tickets_tiposturno tur17   ON (tur17.id = malla.dia17_id) LEFT JOIN tickets_tiposturno tur18   ON (tur18.id = malla.dia18_id) LEFT JOIN tickets_tiposturno tur19   ON (tur19.id = malla.dia19_id) LEFT JOIN tickets_tiposturno tur20   ON (tur20.id = malla.dia20_id) LEFT JOIN tickets_tiposturno tur21   ON (tur21.id = malla.dia21_id) LEFT JOIN tickets_tiposturno tur22   ON (tur22.id = malla.dia22_id) LEFT JOIN tickets_tiposturno tur23   ON (tur23.id = malla.dia23_id) LEFT JOIN tickets_tiposturno tur24   ON (tur24.id = malla.dia24_id) LEFT JOIN tickets_tiposturno tur25   ON (tur25.id = malla.dia25_id) LEFT JOIN tickets_tiposturno tur26   ON (tur26.id = malla.dia26_id) LEFT JOIN tickets_tiposturno tur27   ON (tur27.id = malla.dia27_id) LEFT JOIN tickets_tiposturno tur28   ON (tur28.id = malla.dia28_id) LEFT JOIN tickets_tiposturno tur29   ON (tur29.id = malla.dia29_id) LEFT JOIN tickets_tiposturno tur30   ON (tur30.id = malla.dia30_id) LEFT JOIN tickets_tiposturno tur31   ON (tur31.id = malla.dia31_id) where sedes.id = ' + str(sede) + ' ORDER BY  malla.ano, malla.mes, malla.area_id '
                    if (mes == 0):
                        comando = 'select malla.id  id,sedes.nom_sede nom_sede, empleado_id  empleado_id,emp.nombre nombreEmpleado,  malla.area_id  area_id, area.nombre nombreArea, ano, mes ,   tur1.abrev dia1,  tur2.abrev dia2 ,   tur3.abrev dia3 , tur4.abrev dia4 ,  tur5.abrev dia5  ,  tur6.abrev dia6  , tur7.abrev dia7  ,  tur8.abrev  dia8,  tur9.abrev dia9 , tur10.abrev dia10 ,  tur11.abrev dia11,  tur12.abrev dia12,  tur13.abrev dia13,tur14.abrev dia14 ,  tur15.abrev dia15,  tur16.abrev dia16,  tur17.abrev dia17 ,  tur18.abrev dia18 ,  tur19.abrev dia19,  tur20.abrev dia20 ,  tur21.abrev dia21 ,  tur22.abrev dia22 ,  tur23.abrev dia23,  tur24.abrev dia24,  tur25.abrev dia25 ,  tur26.abrev dia26 ,  tur27.abrev dia27 ,  tur28.abrev dia28 ,  tur29.abrev dia29 ,   tur30.abrev dia30 , tur31.abrev dia31 FROM tickets_mallaturnos  malla INNER JOIN tickets_empleados emp on (emp.id = malla.empleado_id)  INNER JOIN tickets_sedes sedes on (1=1) INNER JOIN tickets_areas area on (area.sedes_id = sedes.id AND area.id = malla.area_id)   LEFT JOIN tickets_tiposturno tur1   ON (tur1.id = malla.dia1_id) LEFT JOIN tickets_tiposturno tur2   ON (tur2.id = malla.dia2_id) LEFT JOIN tickets_tiposturno tur3   ON (tur3.id = malla.dia3_id) LEFT JOIN tickets_tiposturno tur4   ON (tur4.id = malla.dia4_id) LEFT JOIN tickets_tiposturno tur5   ON (tur5.id = malla.dia5_id) LEFT JOIN tickets_tiposturno tur6   ON (tur6.id = malla.dia6_id) LEFT JOIN tickets_tiposturno tur7   ON (tur7.id = malla.dia7_id) LEFT JOIN tickets_tiposturno tur8   ON (tur8.id = malla.dia8_id) LEFT JOIN tickets_tiposturno tur9   ON (tur9.id = malla.dia9_id) LEFT JOIN tickets_tiposturno tur10   ON (tur10.id = malla.dia10_id) LEFT JOIN tickets_tiposturno tur11   ON (tur11.id = malla.dia11_id) LEFT JOIN tickets_tiposturno tur12   ON (tur12.id = malla.dia12_id) LEFT JOIN tickets_tiposturno tur13   ON (tur13.id = malla.dia13_id) LEFT JOIN tickets_tiposturno tur14   ON (tur14.id = malla.dia14_id) LEFT JOIN tickets_tiposturno tur15   ON (tur15.id = malla.dia15_id) LEFT JOIN tickets_tiposturno tur16   ON (tur16.id = malla.dia16_id) LEFT JOIN tickets_tiposturno tur17   ON (tur17.id = malla.dia17_id) LEFT JOIN tickets_tiposturno tur18   ON (tur18.id = malla.dia18_id) LEFT JOIN tickets_tiposturno tur19   ON (tur19.id = malla.dia19_id) LEFT JOIN tickets_tiposturno tur20   ON (tur20.id = malla.dia20_id) LEFT JOIN tickets_tiposturno tur21   ON (tur21.id = malla.dia21_id) LEFT JOIN tickets_tiposturno tur22   ON (tur22.id = malla.dia22_id) LEFT JOIN tickets_tiposturno tur23   ON (tur23.id = malla.dia23_id) LEFT JOIN tickets_tiposturno tur24   ON (tur24.id = malla.dia24_id) LEFT JOIN tickets_tiposturno tur25   ON (tur25.id = malla.dia25_id) LEFT JOIN tickets_tiposturno tur26   ON (tur26.id = malla.dia26_id) LEFT JOIN tickets_tiposturno tur27   ON (tur27.id = malla.dia27_id) LEFT JOIN tickets_tiposturno tur28   ON (tur28.id = malla.dia28_id) LEFT JOIN tickets_tiposturno tur29   ON (tur29.id = malla.dia29_id) LEFT JOIN tickets_tiposturno tur30   ON (tur30.id = malla.dia30_id) LEFT JOIN tickets_tiposturno tur31   ON (tur31.id = malla.dia31_id) where sedes.id = ' + str(sede) + ' ORDER BY  malla.ano, malla.mes, malla.area_id '
                else:
                    if (mes == 0):
                        comando = 'select malla.id  id,sedes.nom_sede nom_sede, empleado_id  empleado_id,emp.nombre nombreEmpleado,  malla.area_id  area_id, area.nombre nombreArea, ano, mes ,   tur1.abrev dia1,  tur2.abrev dia2 ,   tur3.abrev dia3 , tur4.abrev dia4 ,  tur5.abrev dia5  ,  tur6.abrev dia6  , tur7.abrev dia7  ,  tur8.abrev  dia8,  tur9.abrev dia9 , tur10.abrev dia10 ,  tur11.abrev dia11,  tur12.abrev dia12,  tur13.abrev dia13,tur14.abrev dia14 ,  tur15.abrev dia15,  tur16.abrev dia16,  tur17.abrev dia17 ,  tur18.abrev dia18 ,  tur19.abrev dia19,  tur20.abrev dia20 ,  tur21.abrev dia21 ,  tur22.abrev dia22 ,  tur23.abrev dia23,  tur24.abrev dia24,  tur25.abrev dia25 ,  tur26.abrev dia26 ,  tur27.abrev dia27 ,  tur28.abrev dia28 ,  tur29.abrev dia29 ,   tur30.abrev dia30 , tur31.abrev dia31 FROM tickets_mallaturnos  malla INNER JOIN tickets_empleados emp on (emp.id = malla.empleado_id)  INNER JOIN tickets_sedes sedes on (1=1)  INNER JOIN tickets_areas area on (area.sedes_id = sedes.id AND area.id = malla.area_id)  LEFT JOIN tickets_tiposturno tur1   ON (tur1.id = malla.dia1_id) LEFT JOIN tickets_tiposturno tur2   ON (tur2.id = malla.dia2_id) LEFT JOIN tickets_tiposturno tur3   ON (tur3.id = malla.dia3_id) LEFT JOIN tickets_tiposturno tur4   ON (tur4.id = malla.dia4_id) LEFT JOIN tickets_tiposturno tur5   ON (tur5.id = malla.dia5_id) LEFT JOIN tickets_tiposturno tur6   ON (tur6.id = malla.dia6_id) LEFT JOIN tickets_tiposturno tur7   ON (tur7.id = malla.dia7_id) LEFT JOIN tickets_tiposturno tur8   ON (tur8.id = malla.dia8_id) LEFT JOIN tickets_tiposturno tur9   ON (tur9.id = malla.dia9_id) LEFT JOIN tickets_tiposturno tur10   ON (tur10.id = malla.dia10_id) LEFT JOIN tickets_tiposturno tur11   ON (tur11.id = malla.dia11_id) LEFT JOIN tickets_tiposturno tur12   ON (tur12.id = malla.dia12_id) LEFT JOIN tickets_tiposturno tur13   ON (tur13.id = malla.dia13_id) LEFT JOIN tickets_tiposturno tur14   ON (tur14.id = malla.dia14_id) LEFT JOIN tickets_tiposturno tur15   ON (tur15.id = malla.dia15_id) LEFT JOIN tickets_tiposturno tur16   ON (tur16.id = malla.dia16_id) LEFT JOIN tickets_tiposturno tur17   ON (tur17.id = malla.dia17_id) LEFT JOIN tickets_tiposturno tur18   ON (tur18.id = malla.dia18_id) LEFT JOIN tickets_tiposturno tur19   ON (tur19.id = malla.dia19_id) LEFT JOIN tickets_tiposturno tur20   ON (tur20.id = malla.dia20_id) LEFT JOIN tickets_tiposturno tur21   ON (tur21.id = malla.dia21_id) LEFT JOIN tickets_tiposturno tur22   ON (tur22.id = malla.dia22_id) LEFT JOIN tickets_tiposturno tur23   ON (tur23.id = malla.dia23_id) LEFT JOIN tickets_tiposturno tur24   ON (tur24.id = malla.dia24_id) LEFT JOIN tickets_tiposturno tur25   ON (tur25.id = malla.dia25_id) LEFT JOIN tickets_tiposturno tur26   ON (tur26.id = malla.dia26_id) LEFT JOIN tickets_tiposturno tur27   ON (tur27.id = malla.dia27_id) LEFT JOIN tickets_tiposturno tur28   ON (tur28.id = malla.dia28_id) LEFT JOIN tickets_tiposturno tur29   ON (tur29.id = malla.dia29_id) LEFT JOIN tickets_tiposturno tur30   ON (tur30.id = malla.dia30_id) LEFT JOIN tickets_tiposturno tur31   ON (tur31.id = malla.dia31_id) where sedes.id = ' + str(sede) + ' AND malla.ano = ' + str(ano)  + ' ORDER BY  malla.ano, malla.mes, malla.area_id '

                    if (mes != 0):
                        comando = 'select malla.id  id,sedes.nom_sede nom_sede, empleado_id  empleado_id,emp.nombre nombreEmpleado,  malla.area_id  area_id, area.nombre nombreArea, ano, mes ,   tur1.abrev dia1,  tur2.abrev dia2 ,   tur3.abrev dia3 , tur4.abrev dia4 ,  tur5.abrev dia5  ,  tur6.abrev dia6  , tur7.abrev dia7  ,  tur8.abrev  dia8,  tur9.abrev dia9 , tur10.abrev dia10 ,  tur11.abrev dia11,  tur12.abrev dia12,  tur13.abrev dia13,tur14.abrev dia14 ,  tur15.abrev dia15,  tur16.abrev dia16,  tur17.abrev dia17 ,  tur18.abrev dia18 ,  tur19.abrev dia19,  tur20.abrev dia20 ,  tur21.abrev dia21 ,  tur22.abrev dia22 ,  tur23.abrev dia23,  tur24.abrev dia24,  tur25.abrev dia25 ,  tur26.abrev dia26 ,  tur27.abrev dia27 ,  tur28.abrev dia28 ,  tur29.abrev dia29 ,   tur30.abrev dia30 , tur31.abrev dia31 FROM tickets_mallaturnos  malla INNER JOIN tickets_empleados emp on (emp.id = malla.empleado_id) INNER JOIN tickets_sedes sedes on (1=1)  INNER JOIN tickets_areas area on (area.sedes_id = sedes.id AND area.id = malla.area_id)  LEFT JOIN tickets_tiposturno tur1   ON (tur1.id = malla.dia1_id) LEFT JOIN tickets_tiposturno tur2   ON (tur2.id = malla.dia2_id) LEFT JOIN tickets_tiposturno tur3   ON (tur3.id = malla.dia3_id) LEFT JOIN tickets_tiposturno tur4   ON (tur4.id = malla.dia4_id) LEFT JOIN tickets_tiposturno tur5   ON (tur5.id = malla.dia5_id) LEFT JOIN tickets_tiposturno tur6   ON (tur6.id = malla.dia6_id) LEFT JOIN tickets_tiposturno tur7   ON (tur7.id = malla.dia7_id) LEFT JOIN tickets_tiposturno tur8   ON (tur8.id = malla.dia8_id) LEFT JOIN tickets_tiposturno tur9   ON (tur9.id = malla.dia9_id) LEFT JOIN tickets_tiposturno tur10   ON (tur10.id = malla.dia10_id) LEFT JOIN tickets_tiposturno tur11   ON (tur11.id = malla.dia11_id) LEFT JOIN tickets_tiposturno tur12   ON (tur12.id = malla.dia12_id) LEFT JOIN tickets_tiposturno tur13   ON (tur13.id = malla.dia13_id) LEFT JOIN tickets_tiposturno tur14   ON (tur14.id = malla.dia14_id) LEFT JOIN tickets_tiposturno tur15   ON (tur15.id = malla.dia15_id) LEFT JOIN tickets_tiposturno tur16   ON (tur16.id = malla.dia16_id) LEFT JOIN tickets_tiposturno tur17   ON (tur17.id = malla.dia17_id) LEFT JOIN tickets_tiposturno tur18   ON (tur18.id = malla.dia18_id) LEFT JOIN tickets_tiposturno tur19   ON (tur19.id = malla.dia19_id) LEFT JOIN tickets_tiposturno tur20   ON (tur20.id = malla.dia20_id) LEFT JOIN tickets_tiposturno tur21   ON (tur21.id = malla.dia21_id) LEFT JOIN tickets_tiposturno tur22   ON (tur22.id = malla.dia22_id) LEFT JOIN tickets_tiposturno tur23   ON (tur23.id = malla.dia23_id) LEFT JOIN tickets_tiposturno tur24   ON (tur24.id = malla.dia24_id) LEFT JOIN tickets_tiposturno tur25   ON (tur25.id = malla.dia25_id) LEFT JOIN tickets_tiposturno tur26   ON (tur26.id = malla.dia26_id) LEFT JOIN tickets_tiposturno tur27   ON (tur27.id = malla.dia27_id) LEFT JOIN tickets_tiposturno tur28   ON (tur28.id = malla.dia28_id) LEFT JOIN tickets_tiposturno tur29   ON (tur29.id = malla.dia29_id) LEFT JOIN tickets_tiposturno tur30   ON (tur30.id = malla.dia30_id) LEFT JOIN tickets_tiposturno tur31   ON (tur31.id = malla.dia31_id) where sedes.id = ' + str(sede) + ' AND malla.ano = ' + str(ano) + ' AND malla.mes = ' + str(mes) + ' ORDER BY  malla.ano, malla.mes, malla.area_id '




            if (area!=0):
                comando =          'select malla.id  id,sedes.nom_sede nom_sede,  empleado_id  empleado_id,emp.nombre nombreEmpleado,   malla.area_id  area_id, area.nombre nombreArea, ano, mes ,   tur1.abrev dia1,  tur2.abrev dia2 ,   tur3.abrev dia3 , tur4.abrev dia4 ,  tur5.abrev dia5  ,  tur6.abrev dia6  , tur7.abrev dia7  ,  tur8.abrev  dia8,  tur9.abrev dia9 , tur10.abrev dia10 ,  tur11.abrev dia11,  tur12.abrev dia12,  tur13.abrev dia13,tur14.abrev dia14 ,  tur15.abrev dia15,  tur16.abrev dia16,  tur17.abrev dia17 ,  tur18.abrev dia18 ,  tur19.abrev dia19,  tur20.abrev dia20 ,  tur21.abrev dia21 ,  tur22.abrev dia22 ,  tur23.abrev dia23,  tur24.abrev dia24,  tur25.abrev dia25 ,  tur26.abrev dia26 ,  tur27.abrev dia27 ,  tur28.abrev dia28 ,  tur29.abrev dia29 ,   tur30.abrev dia30 , tur31.abrev dia31 FROM tickets_mallaturnos  malla INNER JOIN tickets_empleados emp on (emp.id = malla.empleado_id)  INNER JOIN tickets_sedes sedes on (1=1)  INNER JOIN tickets_areas area on (area.sedes_id = sedes.id AND area.id = malla.area_id)  LEFT JOIN tickets_tiposturno tur1   ON (tur1.id = malla.dia1_id) LEFT JOIN tickets_tiposturno tur2   ON (tur2.id = malla.dia2_id) LEFT JOIN tickets_tiposturno tur3   ON (tur3.id = malla.dia3_id) LEFT JOIN tickets_tiposturno tur4     ON (tur4.id = malla.dia4_id) LEFT JOIN tickets_tiposturno tur5   ON (tur5.id = malla.dia5_id) LEFT JOIN tickets_tiposturno tur6   ON (tur6.id = malla.dia6_id) LEFT JOIN tickets_tiposturno tur7   ON (tur7.id = malla.dia7_id) LEFT JOIN tickets_tiposturno tur8   ON (tur8.id = malla.dia8_id) LEFT JOIN tickets_tiposturno tur9   ON (tur9.id = malla.dia9_id) LEFT JOIN tickets_tiposturno tur10   ON (tur10.id = malla.dia10_id) LEFT JOIN tickets_tiposturno tur11   ON (tur11.id = malla.dia11_id) LEFT JOIN tickets_tiposturno tur12   ON (tur12.id = malla.dia12_id) LEFT JOIN tickets_tiposturno tur13   ON (tur13.id = malla.dia13_id) LEFT JOIN tickets_tiposturno tur14   ON (tur14.id = malla.dia14_id) LEFT JOIN tickets_tiposturno tur15   ON (tur15.id = malla.dia15_id) LEFT JOIN tickets_tiposturno tur16   ON (tur16.id = malla.dia16_id) LEFT JOIN tickets_tiposturno tur17   ON (tur17.id = malla.dia17_id) LEFT JOIN tickets_tiposturno tur18   ON (tur18.id = malla.dia18_id) LEFT JOIN tickets_tiposturno tur19   ON (tur19.id = malla.dia19_id) LEFT JOIN tickets_tiposturno tur20   ON (tur20.id = malla.dia20_id) LEFT JOIN tickets_tiposturno tur21   ON (tur21.id = malla.dia21_id) LEFT JOIN tickets_tiposturno tur22   ON (tur22.id = malla.dia22_id) LEFT JOIN tickets_tiposturno tur23   ON (tur23.id = malla.dia23_id) LEFT JOIN tickets_tiposturno tur24   ON (tur24.id = malla.dia24_id) LEFT JOIN tickets_tiposturno tur25   ON (tur25.id = malla.dia25_id) LEFT JOIN tickets_tiposturno tur26   ON (tur26.id = malla.dia26_id) LEFT JOIN tickets_tiposturno tur27   ON (tur27.id = malla.dia27_id) LEFT JOIN tickets_tiposturno tur28   ON (tur28.id = malla.dia28_id) LEFT JOIN tickets_tiposturno tur29   ON (tur29.id = malla.dia29_id) LEFT JOIN tickets_tiposturno tur30   ON (tur30.id = malla.dia30_id) LEFT JOIN tickets_tiposturno tur31   ON (tur31.id = malla.dia31_id) where sedes.id = ' + str(sede) + ' AND malla.ano = ' + str(ano)  + ' AND malla.mes = ' + str(mes) + ' AND malla.area_id = ' + str(area) + ' ORDER BY  malla.ano, malla.mes, malla.area_id '
                if (ano == 0):
                    comando =      'select malla.id  id,sedes.nom_sede nom_sede,  empleado_id  empleado_id,emp.nombre nombreEmpleado,   malla.area_id  area_id, area.nombre nombreArea, ano, mes ,   tur1.abrev dia1,  tur2.abrev dia2 ,   tur3.abrev dia3 , tur4.abrev dia4 ,  tur5.abrev dia5  ,  tur6.abrev dia6  , tur7.abrev dia7  ,  tur8.abrev  dia8,  tur9.abrev dia9 , tur10.abrev dia10 ,  tur11.abrev dia11,  tur12.abrev dia12,  tur13.abrev dia13,tur14.abrev dia14 ,  tur15.abrev dia15,  tur16.abrev dia16,  tur17.abrev dia17 ,  tur18.abrev dia18 ,  tur19.abrev dia19,  tur20.abrev dia20 ,  tur21.abrev dia21 ,  tur22.abrev dia22 ,  tur23.abrev dia23,  tur24.abrev dia24,  tur25.abrev dia25 ,  tur26.abrev dia26 ,  tur27.abrev dia27 ,  tur28.abrev dia28 ,  tur29.abrev dia29 ,   tur30.abrev dia30 , tur31.abrev dia31 FROM tickets_mallaturnos  malla INNER JOIN tickets_empleados emp on (emp.id = malla.empleado_id)  INNER JOIN tickets_sedes sedes on (1=1)  INNER JOIN tickets_areas area on (area.sedes_id = sedes.id AND area.id = malla.area_id)  LEFT JOIN tickets_tiposturno tur1   ON (tur1.id = malla.dia1_id) LEFT JOIN tickets_tiposturno tur2   ON (tur2.id = malla.dia2_id) LEFT JOIN tickets_tiposturno tur3   ON (tur3.id = malla.dia3_id) LEFT JOIN tickets_tiposturno tur4   ON (tur4.id = malla.dia4_id) LEFT JOIN tickets_tiposturno tur5   ON (tur5.id = malla.dia5_id) LEFT JOIN tickets_tiposturno tur6   ON (tur6.id = malla.dia6_id) LEFT JOIN tickets_tiposturno tur7   ON (tur7.id = malla.dia7_id) LEFT JOIN tickets_tiposturno tur8   ON (tur8.id = malla.dia8_id) LEFT JOIN tickets_tiposturno tur9   ON (tur9.id = malla.dia9_id) LEFT JOIN tickets_tiposturno tur10   ON (tur10.id = malla.dia10_id) LEFT JOIN tickets_tiposturno tur11   ON (tur11.id = malla.dia11_id) LEFT JOIN tickets_tiposturno tur12   ON (tur12.id = malla.dia12_id) LEFT JOIN tickets_tiposturno tur13   ON (tur13.id = malla.dia13_id) LEFT JOIN tickets_tiposturno tur14   ON (tur14.id = malla.dia14_id) LEFT JOIN tickets_tiposturno tur15   ON (tur15.id = malla.dia15_id) LEFT JOIN tickets_tiposturno tur16   ON (tur16.id = malla.dia16_id) LEFT JOIN tickets_tiposturno tur17   ON (tur17.id = malla.dia17_id) LEFT JOIN tickets_tiposturno tur18   ON (tur18.id = malla.dia18_id) LEFT JOIN tickets_tiposturno tur19   ON (tur19.id = malla.dia19_id) LEFT JOIN tickets_tiposturno tur20   ON (tur20.id = malla.dia20_id) LEFT JOIN tickets_tiposturno tur21   ON (tur21.id = malla.dia21_id) LEFT JOIN tickets_tiposturno tur22   ON (tur22.id = malla.dia22_id) LEFT JOIN tickets_tiposturno tur23   ON (tur23.id = malla.dia23_id) LEFT JOIN tickets_tiposturno tur24   ON (tur24.id = malla.dia24_id) LEFT JOIN tickets_tiposturno tur25   ON (tur25.id = malla.dia25_id) LEFT JOIN tickets_tiposturno tur26   ON (tur26.id = malla.dia26_id) LEFT JOIN tickets_tiposturno tur27   ON (tur27.id = malla.dia27_id) LEFT JOIN tickets_tiposturno tur28   ON (tur28.id = malla.dia28_id) LEFT JOIN tickets_tiposturno tur29   ON (tur29.id = malla.dia29_id) LEFT JOIN tickets_tiposturno tur30   ON (tur30.id = malla.dia30_id) LEFT JOIN tickets_tiposturno tur31   ON (tur31.id = malla.dia31_id)   where sedes.id = ' + str(sede) + ' AND malla.mes = ' + str(mes) + ' AND malla.area_id = ' + str(area) + ' ORDER BY  malla.ano, malla.mes, malla.area_id '
                    if (mes == 0):
                        comando = 'select malla.id  id, sedes.nom_sede nom_sede, empleado_id  empleado_id,emp.nombre nombreEmpleado,  malla.area_id  area_id, area.nombre nombreArea, ano, mes ,   tur1.abrev dia1,  tur2.abrev dia2 ,   tur3.abrev dia3 , tur4.abrev dia4 ,  tur5.abrev dia5  ,  tur6.abrev dia6  , tur7.abrev dia7  ,  tur8.abrev  dia8,  tur9.abrev dia9 , tur10.abrev dia10 ,  tur11.abrev dia11,  tur12.abrev dia12,  tur13.abrev dia13,tur14.abrev dia14 ,  tur15.abrev dia15,  tur16.abrev dia16,  tur17.abrev dia17 ,  tur18.abrev dia18 ,  tur19.abrev dia19,  tur20.abrev dia20 ,  tur21.abrev dia21 ,  tur22.abrev dia22 ,  tur23.abrev dia23,  tur24.abrev dia24,  tur25.abrev dia25 ,  tur26.abrev dia26 ,  tur27.abrev dia27 ,  tur28.abrev dia28 ,  tur29.abrev dia29 ,   tur30.abrev dia30 , tur31.abrev dia31 FROM tickets_mallaturnos  malla INNER JOIN tickets_empleados emp on (emp.id = malla.empleado_id)  INNER JOIN tickets_sedes sedes on (1=1)   INNER JOIN tickets_areas area on (area.sedes_id = sedes.id AND area.id = malla.area_id) LEFT JOIN tickets_tiposturno tur1   ON (tur1.id = malla.dia1_id) LEFT JOIN tickets_tiposturno tur2   ON (tur2.id = malla.dia2_id) LEFT JOIN tickets_tiposturno tur3   ON (tur3.id = malla.dia3_id) LEFT JOIN tickets_tiposturno tur4   ON (tur4.id = malla.dia4_id) LEFT JOIN tickets_tiposturno tur5   ON (tur5.id = malla.dia5_id) LEFT JOIN tickets_tiposturno tur6   ON (tur6.id = malla.dia6_id) LEFT JOIN tickets_tiposturno tur7   ON (tur7.id = malla.dia7_id) LEFT JOIN tickets_tiposturno tur8   ON (tur8.id = malla.dia8_id) LEFT JOIN tickets_tiposturno tur9   ON (tur9.id = malla.dia9_id) LEFT JOIN tickets_tiposturno tur10   ON (tur10.id = malla.dia10_id) LEFT JOIN tickets_tiposturno tur11   ON (tur11.id = malla.dia11_id) LEFT JOIN tickets_tiposturno tur12   ON (tur12.id = malla.dia12_id) LEFT JOIN tickets_tiposturno tur13   ON (tur13.id = malla.dia13_id) LEFT JOIN tickets_tiposturno tur14   ON (tur14.id = malla.dia14_id) LEFT JOIN tickets_tiposturno tur15   ON (tur15.id = malla.dia15_id) LEFT JOIN tickets_tiposturno tur16   ON (tur16.id = malla.dia16_id) LEFT JOIN tickets_tiposturno tur17   ON (tur17.id = malla.dia17_id) LEFT JOIN tickets_tiposturno tur18   ON (tur18.id = malla.dia18_id) LEFT JOIN tickets_tiposturno tur19   ON (tur19.id = malla.dia19_id) LEFT JOIN tickets_tiposturno tur20   ON (tur20.id = malla.dia20_id) LEFT JOIN tickets_tiposturno tur21   ON (tur21.id = malla.dia21_id) LEFT JOIN tickets_tiposturno tur22   ON (tur22.id = malla.dia22_id) LEFT JOIN tickets_tiposturno tur23   ON (tur23.id = malla.dia23_id) LEFT JOIN tickets_tiposturno tur24   ON (tur24.id = malla.dia24_id) LEFT JOIN tickets_tiposturno tur25   ON (tur25.id = malla.dia25_id) LEFT JOIN tickets_tiposturno tur26   ON (tur26.id = malla.dia26_id) LEFT JOIN tickets_tiposturno tur27   ON (tur27.id = malla.dia27_id) LEFT JOIN tickets_tiposturno tur28   ON (tur28.id = malla.dia28_id) LEFT JOIN tickets_tiposturno tur29   ON (tur29.id = malla.dia29_id) LEFT JOIN tickets_tiposturno tur30   ON (tur30.id = malla.dia30_id) LEFT JOIN tickets_tiposturno tur31   ON (tur31.id = malla.dia31_id)   where sedes.id = ' + str(sede) + ' AND malla.area_id = ' + str(area) + ' ORDER BY  malla.ano, malla.mes, malla.area_id '
                else:
                    if (mes != 0):
                        comando =  'select malla.id  id, sedes.nom_sede nom_sede, empleado_id  empleado_id,emp.nombre nombreEmpleado,  malla.area_id  area_id, area.nombre nombreArea, ano, mes ,   tur1.abrev dia1,  tur2.abrev dia2 ,   tur3.abrev dia3 , tur4.abrev dia4 ,  tur5.abrev dia5  ,  tur6.abrev dia6  , tur7.abrev dia7  ,  tur8.abrev  dia8,  tur9.abrev dia9 , tur10.abrev dia10 ,  tur11.abrev dia11,  tur12.abrev dia12,  tur13.abrev dia13,tur14.abrev dia14 ,  tur15.abrev dia15,  tur16.abrev dia16,  tur17.abrev dia17 ,  tur18.abrev dia18 ,  tur19.abrev dia19,  tur20.abrev dia20 ,  tur21.abrev dia21 ,  tur22.abrev dia22 ,  tur23.abrev dia23,  tur24.abrev dia24,  tur25.abrev dia25 ,  tur26.abrev dia26 ,  tur27.abrev dia27 ,  tur28.abrev dia28 ,  tur29.abrev dia29 ,   tur30.abrev dia30 , tur31.abrev dia31 FROM tickets_mallaturnos  malla INNER JOIN tickets_empleados emp on (emp.id = malla.empleado_id)  INNER JOIN tickets_sedes sedes on (1=1)  INNER JOIN tickets_areas area on (area.sedes_id = sedes.id AND area.id = malla.area_id)  LEFT JOIN tickets_tiposturno tur1   ON (tur1.id = malla.dia1_id) LEFT JOIN tickets_tiposturno tur2   ON (tur2.id = malla.dia2_id) LEFT JOIN tickets_tiposturno tur3   ON (tur3.id = malla.dia3_id) LEFT JOIN tickets_tiposturno tur4   ON (tur4.id = malla.dia4_id) LEFT JOIN tickets_tiposturno tur5   ON (tur5.id = malla.dia5_id) LEFT JOIN tickets_tiposturno tur6   ON (tur6.id = malla.dia6_id) LEFT JOIN tickets_tiposturno tur7   ON (tur7.id = malla.dia7_id) LEFT JOIN tickets_tiposturno tur8   ON (tur8.id = malla.dia8_id) LEFT JOIN tickets_tiposturno tur9   ON (tur9.id = malla.dia9_id) LEFT JOIN tickets_tiposturno tur10   ON (tur10.id = malla.dia10_id) LEFT JOIN tickets_tiposturno tur11   ON (tur11.id = malla.dia11_id) LEFT JOIN tickets_tiposturno tur12   ON (tur12.id = malla.dia12_id) LEFT JOIN tickets_tiposturno tur13   ON (tur13.id = malla.dia13_id) LEFT JOIN tickets_tiposturno tur14   ON (tur14.id = malla.dia14_id) LEFT JOIN tickets_tiposturno tur15   ON (tur15.id = malla.dia15_id) LEFT JOIN tickets_tiposturno tur16   ON (tur16.id = malla.dia16_id) LEFT JOIN tickets_tiposturno tur17   ON (tur17.id = malla.dia17_id) LEFT JOIN tickets_tiposturno tur18   ON (tur18.id = malla.dia18_id) LEFT JOIN tickets_tiposturno tur19   ON (tur19.id = malla.dia19_id) LEFT JOIN tickets_tiposturno tur20   ON (tur20.id = malla.dia20_id) LEFT JOIN tickets_tiposturno tur21   ON (tur21.id = malla.dia21_id) LEFT JOIN tickets_tiposturno tur22   ON (tur22.id = malla.dia22_id) LEFT JOIN tickets_tiposturno tur23   ON (tur23.id = malla.dia23_id) LEFT JOIN tickets_tiposturno tur24   ON (tur24.id = malla.dia24_id) LEFT JOIN tickets_tiposturno tur25   ON (tur25.id = malla.dia25_id) LEFT JOIN tickets_tiposturno tur26   ON (tur26.id = malla.dia26_id) LEFT JOIN tickets_tiposturno tur27   ON (tur27.id = malla.dia27_id) LEFT JOIN tickets_tiposturno tur28   ON (tur28.id = malla.dia28_id) LEFT JOIN tickets_tiposturno tur29   ON (tur29.id = malla.dia29_id) LEFT JOIN tickets_tiposturno tur30   ON (tur30.id = malla.dia30_id) LEFT JOIN tickets_tiposturno tur31   ON (tur31.id = malla.dia31_id)   where sedes.id = ' + str(sede) + ' AND malla.ano = ' + str(ano) + ' AND malla.mes = ' + str(mes) + ' AND malla.area_id = ' + str(area) + ' ORDER BY  malla.ano, malla.mes, malla.area_id '

                    if (mes == 0):
                         comando = 'select malla.id  id, sedes.nom_sede nom_sede, empleado_id  empleado_id,emp.nombre nombreEmpleado,  malla.area_id  area_id, area.nombre nombreArea, ano, mes ,   tur1.abrev dia1,  tur2.abrev dia2 ,   tur3.abrev dia3 , tur4.abrev dia4 ,  tur5.abrev dia5  ,  tur6.abrev dia6  , tur7.abrev dia7  ,  tur8.abrev  dia8,  tur9.abrev dia9 , tur10.abrev dia10 ,  tur11.abrev dia11,  tur12.abrev dia12,  tur13.abrev dia13,tur14.abrev dia14 ,  tur15.abrev dia15,  tur16.abrev dia16,  tur17.abrev dia17 ,  tur18.abrev dia18 ,  tur19.abrev dia19,  tur20.abrev dia20 ,  tur21.abrev dia21 ,  tur22.abrev dia22 ,  tur23.abrev dia23,  tur24.abrev dia24,  tur25.abrev dia25 ,  tur26.abrev dia26 ,  tur27.abrev dia27 ,  tur28.abrev dia28 ,  tur29.abrev dia29 ,   tur30.abrev dia30 , tur31.abrev dia31 FROM tickets_mallaturnos  malla INNER JOIN tickets_empleados emp on (emp.id = malla.empleado_id)  INNER JOIN tickets_sedes sedes on (1=1)  INNER JOIN tickets_areas area on (area.sedes_id = sedes.id AND area.id = malla.area_id) LEFT JOIN tickets_tiposturno tur1   ON (tur1.id = malla.dia1_id) LEFT JOIN tickets_tiposturno tur2   ON (tur2.id = malla.dia2_id) LEFT JOIN tickets_tiposturno tur3   ON (tur3.id = malla.dia3_id) LEFT JOIN tickets_tiposturno tur4   ON (tur4.id = malla.dia4_id) LEFT JOIN tickets_tiposturno tur5   ON (tur5.id = malla.dia5_id) LEFT JOIN tickets_tiposturno tur6   ON (tur6.id = malla.dia6_id) LEFT JOIN tickets_tiposturno tur7   ON (tur7.id = malla.dia7_id) LEFT JOIN tickets_tiposturno tur8   ON (tur8.id = malla.dia8_id) LEFT JOIN tickets_tiposturno tur9   ON (tur9.id = malla.dia9_id) LEFT JOIN tickets_tiposturno tur10   ON (tur10.id = malla.dia10_id) LEFT JOIN tickets_tiposturno tur11   ON (tur11.id = malla.dia11_id) LEFT JOIN tickets_tiposturno tur12   ON (tur12.id = malla.dia12_id) LEFT JOIN tickets_tiposturno tur13   ON (tur13.id = malla.dia13_id) LEFT JOIN tickets_tiposturno tur14   ON (tur14.id = malla.dia14_id) LEFT JOIN tickets_tiposturno tur15   ON (tur15.id = malla.dia15_id) LEFT JOIN tickets_tiposturno tur16   ON (tur16.id = malla.dia16_id) LEFT JOIN tickets_tiposturno tur17   ON (tur17.id = malla.dia17_id) LEFT JOIN tickets_tiposturno tur18   ON (tur18.id = malla.dia18_id) LEFT JOIN tickets_tiposturno tur19   ON (tur19.id = malla.dia19_id) LEFT JOIN tickets_tiposturno tur20   ON (tur20.id = malla.dia20_id) LEFT JOIN tickets_tiposturno tur21   ON (tur21.id = malla.dia21_id) LEFT JOIN tickets_tiposturno tur22   ON (tur22.id = malla.dia22_id) LEFT JOIN tickets_tiposturno tur23   ON (tur23.id = malla.dia23_id) LEFT JOIN tickets_tiposturno tur24   ON (tur24.id = malla.dia24_id) LEFT JOIN tickets_tiposturno tur25   ON (tur25.id = malla.dia25_id) LEFT JOIN tickets_tiposturno tur26   ON (tur26.id = malla.dia26_id) LEFT JOIN tickets_tiposturno tur27   ON (tur27.id = malla.dia27_id) LEFT JOIN tickets_tiposturno tur28   ON (tur28.id = malla.dia28_id) LEFT JOIN tickets_tiposturno tur29   ON (tur29.id = malla.dia29_id) LEFT JOIN tickets_tiposturno tur30   ON (tur30.id = malla.dia30_id) LEFT JOIN tickets_tiposturno tur31   ON (tur31.id = malla.dia31_id) where sedes.id = ' + str(sede) + ' AND  malla.ano = ' + str(ano) + ' AND malla.area_id = ' + str(area) + ' ORDER BY  malla.ano, malla.mes, malla.area_id '


    print(comando)
    cur.execute(comando)

    malla = []

    if (perfil != 'COLABORADOR'):

        for id, nom_sede, empleado_id, nombreEmpleado, area_id,nombreArea, ano, mes, dia1,dia2,  dia3,dia4, dia5, dia6, dia7, dia8, dia9, dia10,dia11,dia12,dia13,dia14,dia15,dia16,dia17,dia18,dia19,dia20,dia21,dia22,dia23,dia24,dia25,dia26,dia27,dia28,dia29,dia30,dia31 in cur.fetchall():

            malla.append(
                {"model":"tickets.tickets_mallaturnos","pk":id,"fields":
                {"id": id,"nom_sede":nom_sede,
                    "empleado_id": empleado_id,"nombreEmpleado":nombreEmpleado,
                    "area_id":area_id,"nombreArea":nombreArea,
                    "ano": ano, "mes": mes,
                    "dia1": dia1,"dia2": dia2,"dia3":dia3, "dia4":dia4,"dia5":dia5,"dia6":dia6,"dia7":dia7,"dia8":dia8,"dia9":dia9,"dia10":dia10,
                    "dia11": dia11,"dia12": dia12,"dia13":dia13, "dia14":dia14,"dia15":dia15,"dia16":dia16,"dia17":dia17,"dia18":dia18,"dia19":dia19,"dia20":dia20,
                    "dia21": dia21,"dia22": dia22,"dia23":dia23, "dia24":dia24,"dia25":dia25,"dia26":dia26,"dia27":dia27,"dia28":dia28,"dia29":dia29,"dia30":dia30,"dia31":dia31}})

    miConexion.close()
    print("malla")
    print(malla)

    # Cierro Conexion


    context['Malla'] = malla

    ## Voy a enviar tickets

    serialized1 = json.dumps(malla)

    print ("Envio = ", json)

    return HttpResponse(serialized1, content_type='application/json')



## Aqui el Update View de la Malla

class GestionCoordMallaUpdate(UpdateView):
    print ("Entre a GestionCoordMallaUpdate")

    model = MallaTurnos
    form_class = mallaTurnosForm

    context_object_name = 'gestionCoordMallaUpdate'
    template_name = 'tickets/GestionCoordMallaUpdate.html'

    sucess_url = reverse_lazy ('gestionCoord')
    #sucess_url = reverse_lazy('gestionCoord', kwargs={'username': username, 'nombreUsuario': nombreUsuario, 'nombreSede': nombreSede,                                         'empleadoId': empleadoId, 'sedeSeleccionada': sedeSeleccionada,                                         'perfil': perfil, 'ano': ano, 'mes': mes, 'sedeMalla': sedeMalla,                                         'areaMalla': areaMalla, 'nombreMalla': nombreMalla})

    def form_valid (self, form):

        print ("Entre a form valid de GestionCoordMallaUpdate :")
        print ("Kwargs aqui :", self.kwargs)

        form.instance.save()

        # Aqui Rutina graba en tabla tickets_ticketsmalla INSERT
        ticSeleccionado = self.request.POST['ticket']
        empleadoId = self.kwargs['empleadoId']
        fecha =  datetime.now()
        estadoReg= 'A'
        mallaTurnosId= self.kwargs['pk']

        print ("ticSeleccionado = ", ticSeleccionado)
        print("empleadoId = ", empleadoId)
        print("fecha = ", fecha)
        print("estadoReg = ", estadoReg)
        print("mallaTurnosId = ", mallaTurnosId)

        ## Realizo el INSERT

        miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        cur.execute("set client_encoding='LATIN1';")

        comando = 'INSERT INTO tickets_ticketsmalla (fecha,"estadoReg", empleado_id, "mallaTurnos_id", ticket_id) VALUES ( ' + "'" + str(fecha) + "'," + "'" + str(estadoReg) + "'" + ","  + str(empleadoId) + "," + str(mallaTurnosId) + "," + str(ticSeleccionado) + ")"

        print(comando)
        resultado = cur.execute(comando)
        print("resultado =", resultado)
        n = cur.rowcount
        print("Registros commit = ", n)

        miConexion.commit()
        #mallaTicket = cur.fetchone()[0]

        #print("mallaTicket = ", mallaTicket)
        miConexion.close()


        # Fin Rutina graba en tabla tickets_ticketsmalla INSERT

        context = {}

        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']

        context["Ano"] = self.kwargs['ano']
        context["Mes"] = self.kwargs['mes']
        context["AreaMalla"] = self.kwargs['areaMalla']
        context["SedeMalla"] = self.kwargs['sedeMalla']
        context["NombreMalla"] = self.kwargs['nombreMalla']


        messages.success(self.request, "La asignacion fue satisfactoria.")
        return super(GestionCoordMallaUpdate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        print("Entre Contexto de Updated View GestionCoordUpdate")
        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(" kwargs de update = ", self.kwargs)

        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']

        context["Ano"] = self.kwargs['ano']
        context["Mes"] = self.kwargs['mes']
        context["AreaMalla"] = self.kwargs['areaMalla']
        context["SedeMalla"] = self.kwargs['sedeMalla']
        context["NombreMalla"] = self.kwargs['nombreMalla']


        print("context en el get_context_data AsignacionUpdated = ", context)
        print(context["Username"])
        print(context["NombreUsuario"])
        print(context["NombreSede"])
        print(context["EmpleadoId"])
        print(context["SedeSeleccionada"])
        empleadoId= self.kwargs['empleadoId']

        # Día actual
        today = date.today()

        now = datetime.now()
        print(today.year)
        print(today.month)
        num_days = monthrange(today.year, today.month)[1]  # num_days = 31
        print(num_days)  # Imprime 31
        context['num_days'] = num_days



        ## Creamos los tickets

        # Consigo las areas

        miConexion = psycopg2.connect(host="192.168.0.237", database="thtickets", port="5432", user="postgres",
                                      password="BD_m3d1c4l")
        miConexion.set_client_encoding('LATIN1')
        cur = miConexion.cursor()
        cur.execute("set client_encoding='LATIN1';")

        comando = "SELECT tic.id id , tic.id nombre FROM public.tickets_tickets tic  WHERE tic.asignado_id = " + str(empleadoId) + " AND " + 'tic."estadoRespuestaCoordinador"=' + "'Pendiente'"

        cur.execute(comando)
        print(comando)

        ticket = []


        for id, nombre in cur.fetchall():
            ticket.append({'id': id, 'nombre':nombre})

        miConexion.close()

        context['Ticket'] = ticket

        ## Fin Tickets

        return context


    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        print ("Entre sucess url con kwargs  GestionCoordMallaUpdate = ", self.kwargs)


        username = self.kwargs['username']
        nombreUsuario = self.kwargs['nombreUsuario']
        nombreSede = self.kwargs['nombreSede']
        empleadoId = self.kwargs['empleadoId']
        sedeSeleccionada = self.kwargs['sedeSeleccionada']
        perfil = self.kwargs['perfil']

        ano         = self.kwargs['ano']
        mes         = self.kwargs['mes']
        areaMalla   = self.kwargs['areaMalla']
        sedeMalla   = self.kwargs['sedeMalla']
        nombreMalla = self.kwargs['nombreMalla']

        print ("Aqui voy en get_success_url")

        return reverse_lazy('gestionCoord', kwargs={'username':username,'nombreUsuario':nombreUsuario,'nombreSede': nombreSede,'empleadoId':empleadoId ,'sedeSeleccionada':sedeSeleccionada, 'perfil':perfil, 'ano':ano, 'mes':mes, 'sedeMalla':sedeMalla, 'areaMalla':areaMalla, 'nombreMalla':nombreMalla })



class CrearMalla(  CreateView ):

    print("Entre Creae View de Crearmalla")
    model = MallaTurnos
    fields = ['ano', 'mes', 'empleado','area','dia1','dia2','dia3','dia4','dia5','dia6','dia7','dia8','dia9','dia10','dia11','dia12','dia13','dia14','dia15','dia16','dia17','dia18','dia19','dia20','dia21','dia22','dia23','dia24','dia25','dia26','dia27','dia28','dia29','dia30','dia31']
    template_name = 'tickets/crearMallaTurnos.html'

    def get_initial(self):
        print ("initial = ", self.kwargs)
        initial = super(CrearMalla, self).get_initial()
        initial['empleado'] = self.kwargs['empleadoId']

        return initial


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(" kwargs =", self.kwargs)
        print(" kwargs de get_context_data =", self.kwargs['username'])
        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']

        context["Ano"] = self.kwargs['ano']
        context["Mes"] = self.kwargs['mes']
        context["AreaMalla"] = self.kwargs['areaMalla']
        context["SedeMalla"] = self.kwargs['sedeMalla']
        context["NombreMalla"] = self.kwargs['nombreMalla']


        print ("context en el get_context_data = ", context)
        print(context["Username"])
        print(context["NombreUsuario"])
        print(context["NombreSede"])
        print(context["EmpleadoId"])
        print(context["SedeSeleccionada"])

        return context

    def form_valid(self, form):

        print ("FormaValida Clean de Crear malla = ",form.cleaned_data)

        instance = form.save()
        context={}
        envio = self.kwargs['username'] + ',' + self.kwargs['sedeSeleccionada'] + ',' + self.kwargs['nombreUsuario'] + ',' + self.kwargs['nombreSede'] + ',' + self.kwargs['empleadoId'] + ',' + self.kwargs['perfil'] + ',' + self.kwargs['ano']  + ',' + self.kwargs['mes'] + ',' + self.kwargs['sedeMalla'] + ',' + self.kwargs['areaMalla']  + ',' + self.kwargs['nombreMalla']
        redirect_url = reverse('gestionCoord_A')
        print ("redirect_url = ",redirect_url )

        print ("Envio = ", envio)
        return redirect(f'{redirect_url}{envio}')


    def form_invalid(self, form):
        print("Entre form_invalid de crear malla")
        response = super().form_invalid(form)
        print("pase1")
        print ("responde = ", response)
        if self.request.accepts('text/html'):
            print("pase2")

            return response
        else:
            print("pase3")
            return JsonResponse(form.errors, status=400)

## Desde aquip talento humano

class THumano(ListView):
    print ("Entre List View Gestion Talento Humano")

    queryset = Tickets.objects.filter().order_by('-fecha','empleado_id')
    context_object_name = 'THumano'
    paginate_by = 10
    template_name = 'tickets/tHumano.html'


    def get_context_data(self, **kwargs):


        context = super().get_context_data(**kwargs)
        user = self.request.user

        print(" SELF Thumano = ", self.kwargs)

        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"]           = self.kwargs['perfil']

        print(context["Username"])
        print(context["NombreUsuario"])
        print(context["NombreSede"])
        print(context["EmpleadoId"])
        print(context["SedeSeleccionada"])
        print("perfil = " , context["Perfil"])

        return context


    def get_queryset(self):

        ticketId = self.kwargs['ticketId']
        empleadoNom = self.kwargs['nombre']
        perfil = self.kwargs['perfil']

        print("kwargs de queryset", self.kwargs)
        print("CONCLUSION ticketId = ", ticketId)
        nombreSede = self.kwargs['nombreSede']
        print("nombreSede", nombreSede)

        print ("Entre querySet de THumano  ")
        #print ("empleadoId", empleadoId)
        print("perfil = ", perfil)

        try:

            if (perfil != 'TALENTO HUMANO'):
                print ("Entre por Error a No talento Humano")
                return Tickets.objects.none()

            if (ticketId == '0' and empleadoNom == 'null'):
                # busqueda general
                print("Entre todos los ticket= ", ticketId)
                # queryset = Tickets.objects.filter(asignado_id__isnull=True).order_by('id')
                queryset = Tickets.objects.filter(asignado_id__isnull=True).select_related('tiposTicket',
                                                                                           'empleado').order_by(
                    '-fecha', 'empleado_id')

            if (ticketId != '0' and empleadoNom == 'null'):
                # busqueda por ticket

                print("Entre por ticket = ", ticketId)
                queryset = Tickets.objects.filter(asignado_id__isnull=True, id=ticketId).order_by('-fecha',
                                                                                                  'empleado_id')
                print("queryset = ", queryset)

            if (ticketId == '0' and empleadoNom != 'null'):
                ## busqueda por nombre
                print("Entre  por nombre = ", empleadoNom)
                # queryset = Tickets.objects.filter(asignado_id__isnull=True, empleado_id__contains=empleadoNom).select_related('empleado').order_by('id')
                queryset = Tickets.objects.select_related('empleado').filter(asignado_id__isnull=True,
                                                                             empleado_id__nombre__icontains=empleadoNom).order_by(
                    '-fecha', 'empleado_id')
                print("queryset = ", queryset)

            if (ticketId != '0' and empleadoNom != 'null'):
                ## busqueda por ticket, nombre
                print("Entre por ticket y por nombre = ", empleadoNom)
                queryset = Tickets.objects.select_related('empleado').filter(asignado_id__isnull=True, id=ticketId,
                                                                             empleado_id__nombre__icontains=empleadoNom).order_by(
                    '-fecha', 'empleado_id')
                print("queryset = ", queryset)

            return queryset.all()

        except Tickets.DoesNotExist:
            print("sali posr exception")
            return Tickets.objects.none()


class THumanoUpdate(UpdateView):
    print ("Entre THumanoUpdate ")
    form_class = ticketsForm3
    model = Tickets
    #fields = ['id', 'tiposTicket', 'empleado','sedeInicial','desdeInicial','sedeFinal','hastaFinal', 'asignado']
    #fields = ['asignado']
    context_object_name = 'THumanoUpdate'
    template_name = 'tickets/tHumanoUpdate.html'
    success_url = reverse_lazy('tHumano')

    def get_initial(self):
        print("initial = ", self.kwargs)
        initial = super(THumanoUpdate, self).get_initial()
        initial['respuestaEmpleadoThumano'] = self.kwargs['empleadoId']

        return initial

    def form_valid(self, form):
        print ("Entre Forma VALIDA THumanoUpdate ")

        print ("forma valida sef.kwargs =" , self.kwargs)
        form.instance.save()

        print ("acabe de grabar la actualziacion de THumanoUpdate")

        context = {}

        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']

        #self.get_context_data(   context=context )

        messages.success(self.request, "La actualizacion fue satisfactoria.")
        return super(THumanoUpdate, self).form_valid(form)



    def get_context_data(self, **kwargs):

        print ("Entre Contexto de Updated View THumanoUpdate")
        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(" kwargs de THumanoUpdate = ", self.kwargs)

        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']

        print("context en el get_context_data THumanoUpdate = ", context)
        print(context["Username"])
        print(context["NombreUsuario"])
        print(context["NombreSede"])
        print(context["EmpleadoId"])
        print(context["SedeSeleccionada"])

        return context

    def get_success_url(self):
        # if you are passing 'pk' from 'urls' to 'DeleteView' for company
        # capture that 'pk' as companyid and pass it to 'reverse_lazy()' function
        print ("Entre sucess url con kwargs  GestionCoordUpdate = ", self.kwargs)


        username = self.kwargs['username']
        nombreUsuario = self.kwargs['nombreUsuario']
        nombreSede = self.kwargs['nombreSede']
        empleadoId = self.kwargs['empleadoId']
        sedeSeleccionada = self.kwargs['sedeSeleccionada']
        perfil= self.kwargs['perfil']


        return reverse_lazy('tHumano', kwargs={'ticketId':0, 'username':username,'nombreUsuario':nombreUsuario,'nombreSede': nombreSede,'empleadoId':empleadoId ,'sedeSeleccionada':sedeSeleccionada, 'perfil':perfil})



class TicketsMalla1(ListView):
    print ("Entre List View TicketsMalla1")

    queryset = TicketsMalla.objects.filter().order_by('id')
    context_object_name = 'TicketsMalla1'
    paginate_by = 10
    template_name = 'tickets/ticketsMalla.html'



    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        user = self.request.user

        print(" SELF Thumano = ", self.kwargs)

        context["Username"] = self.kwargs['username']
        context["NombreUsuario"] = self.kwargs['nombreUsuario']
        context["NombreSede"] = self.kwargs['nombreSede']
        context["EmpleadoId"] = self.kwargs['empleadoId']
        context["SedeSeleccionada"] = self.kwargs['sedeSeleccionada']
        context["Perfil"] = self.kwargs['perfil']

        print(context["Username"])
        print(context["NombreUsuario"])
        print(context["NombreSede"])
        print(context["EmpleadoId"])
        print(context["SedeSeleccionada"])


        return context

    def get_queryset(self):
        #empleadoId = self.kwargs['empleadoId']
        print ("Entre querySet de TicketsMalla  ")
        #print ("empleadoId", empleadoId)

        ticketId = self.kwargs['ticketId']
        empleadoNom = self.kwargs['nombre']
        perfil = self.kwargs['perfil']

        try:

            if (perfil != 'COORDINADOR'):
                print("Entre NO ENTREGO PAGINA A COLABORADOR")
                return Tickets.objects.none()

            if (ticketId == '0' and empleadoNom == 'null'):
                # busqueda general
                print("Entre todos los ticket= ", ticketId)
                # queryset = Tickets.objects.filter(asignado_id__isnull=True).order_by('id')

                queryset = TicketsMalla.objects.all().select_related('mallaTurnos', 'ticket', 'empleado').order_by('-fecha', 'empleado_id', 'ticket_id')

            if (ticketId != '0' and empleadoNom == 'null'):
                # busqueda por ticket

                print("Entre por ticket = ", ticketId)

                queryset = TicketsMalla.objects.filter(id=ticketId).select_related('mallaTurnos', 'ticket', 'empleado').order_by('-fecha', 'empleado_id', 'ticket_id')

                print("queryset = ", queryset)

            if (ticketId == '0' and empleadoNom != 'null'):
                ## busqueda por nombre
                print("Entre  por nombre = ", empleadoNom)
                # queryset = Tickets.objects.filter(asignado_id__isnull=True, empleado_id__contains=empleadoNom).select_related('empleado').order_by('id')
                queryset = TicketsMalla.objects.filter( empleado_id__nombre__icontains=empleadoNom).select_related('mallaTurnos', 'ticket', 'empleado').order_by('-fecha', 'empleado_id', 'ticket_id')

                print("queryset = ", queryset)

            if (ticketId != '0' and empleadoNom != 'null'):
                ## busqueda por ticket, nombre
                print("Entre por ticket y por nombre = ", empleadoNom)

                queryset = TicketsMalla.objects.filter( id=ticketId , empleado_id__nombre__icontains=empleadoNom).select_related('mallaTurnos', 'ticket', 'empleado').order_by('-fecha', 'empleado_id', 'ticket_id')
                print("queryset = ", queryset)

            return queryset.all()

        except Tickets.DoesNotExist:
            print("sali posr exception")
            return Tickets.objects.none()


