from django.shortcuts import render
from django.http import FileResponse
import psycopg2
import json
from django.views.generic import View
from django.views.generic import TemplateView
from tickets.models import Empleados, Tickets
from django.views.generic import FormView, CreateView
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.http import urlencode
# Create your views here.
from django.http import JsonResponse

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

            comando = 'SELECT cedula cedula,nom_sede nom_sede  FROM public.tickets_empleados usu, public.tickets_sedes sedes WHERE usu.sede_id = sedes.id and usu."estadoReg" = ' + "'A" + "'" + " and usu.cedula = '" + username + "' and sedes.codreg_sede =  '" + sedeSeleccionada + "'"
            print(comando)
            cur.execute(comando)

            permitido = []

            for cedula, nom_sede in cur.fetchall():
                permitido.append({'cedula': cedula, 'nom_sede': nom_sede})

            miConexion.close()



            if permitido == []:

                context['Error'] = "Usuario no tiene autorizacion para la sede seleccionada y/o Reportes no asignados ! "
                return render(request, "tickets/accesoPrincipal.html", context)

            else:
                pass
                print("Paso Autenticacion")

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

    model = Tickets
    #fields = ['sede','tiposTicket', 'fecha','empleado','sedeInicial','tiposTurnoInicial','desdeInicial','hastaInicial','sedeFinal','tiposTurnoFinal','desdeFinal','hastaFinal','adjunto']
    fields = ['sede', 'tiposTicket', 'fecha', 'empleado','sedeInicial','tiposTurnoInicial','desdeInicial','hastaInicial','adjunto','sedeFinal' ,'tiposTurnoFinal', 'desdeFinal','hastaFinal' ,'sedeReemplazo', 'reemplazo']

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

        print ("context en el get_context_data = ", context)
        print(context["Username"])
        print(context["NombreUsuario"])
        print(context["NombreSede"])
        print(context["EmpleadoId"])
        print(context["SedeSeleccionada"])

        return context

    def form_valid(self, form):

        print ("FormaValida Clean = ",form.cleaned_data)

        #form.cleaned_data['empleado'] = self.kwargs['username']
        print("form.cleaned_data['empleado ya actualizada = ", form.cleaned_data['empleado'])
        instance = form.save()
        context={}
        #return HttpResponseRedirect(reverse_lazy('ticket:detail', args=[instance.id]))
        #redirect_url = reverse('CreacionTickets', args=(backend,))
        ruta = reverse("creacion_ticketsA")
        print ("ruta = ", ruta)
        ruta2 = reverse_lazy("creacion_ticketsA")
        print("ruta2 = ", ruta2)
        redirect_url = reverse('creacion_ticketsA')
        print ("redirect_url = ",redirect_url )
        #parameters = urlencode(form.cleaned_data)
        # return redirect(f'{redirect_url}?{parameters}')

        parameters = urlencode(self.kwargs)
        envio=self.kwargs['username']+','+ self.kwargs['sedeSeleccionada']  + ',' + self.kwargs['nombreUsuario'] + ',' + self.kwargs['nombreSede'] + ','  + self.kwargs['empleadoId']
        print ("parameters = " , parameters)
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

    comando = 'SELECT ticket.id,ticket.sede_id  , sedes.nom_sede nom_sede,ticket."tiposTicket_id",  tiposticket.nombre nombreTiposTicket ,to_char(ticket.fecha,' + "'" + "YYYY-MM-DD HH:MM.SS" + "')" + ',empleado_id,"sedeInicial_id","tiposTurnoInicial_id",tiposturno.nombre nombreTiposTurnoInicial,  to_char(ticket."desdeInicial",' + "'" + "YYYY-MM-DD HH:MM.SS" + "')" + ',to_char(ticket."hastaInicial",' + "'" + "YYYY-MM-DD HH:MM.SS" + "')"'   FROM tickets_tickets  ticket, tickets_sedes sedes, tickets_tiposticket tiposticket , tickets_tiposturno tiposturno   WHERE ticket.sede_id = sedes.id and ticket."tiposTicket_id" = tiposticket.id and ticket."tiposTurnoInicial_id" = tiposturno.id and ticket.empleado_id = ' + "'" +  empleadoId + "'"
    print(comando)
    cur.execute(comando)

    tickets = []

    for id, sede_id, nom_sede,tiposTicket_id, nombreTiposTicket, fecha, empleado, sedeInicial_id,tiposTurnoInicial_id,  nombreTiposTurnoInicial,desdeInicial, hastaInicial in cur.fetchall():
        tickets.append(
            {"model":"tickets.tickets","pk":id,"fields":
            {"id": id, "sede_id": sede_id, "nom_sede":nom_sede,
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

        comando = 'SELECT ticket.id,ticket.sede_id  , sedes.nom_sede nom_sede,ticket."tiposTicket_id",  tiposticket.nombre nombreTiposTicket ,to_char(ticket.fecha,' + "'" + "YYYY-MM-DD HH:MM.SS" + "')" + ',empleado_id empleado,"sedeInicial_id","tiposTurnoInicial_id",tiposturno.nombre nombreTiposTurnoInicial,  to_char(ticket."desdeInicial",' + "'" + "YYYY-MM-DD HH:MM.SS" + "')" + ',to_char(ticket."hastaInicial",' + "'" + "YYYY-MM-DD HH:MM.SS" + "')"'   FROM tickets_tickets  ticket, tickets_sedes sedes, tickets_tiposticket tiposticket , tickets_tiposturno tiposturno   WHERE ticket.sede_id = sedes.id and ticket."tiposTicket_id" = tiposticket.id and ticket."tiposTurnoInicial_id" = tiposturno.id and empleado_id = ' + "'" + empleadoId + "'"
        print(comando)
        cur.execute(comando)

        tickets = []

        for id, sede_id, nom_sede, tiposTicket_id, nombreTiposTicket, fecha, empleado, sedeInicial_id, tiposTurnoInicial_id, nombreTiposTurnoInicial, desdeInicial, hastaInicial in cur.fetchall():
            tickets.append( {"id": id, "sede_id": sede_id, "nom_sede": nom_sede,
                     "tiposTicket_id": tiposTicket_id,
                     "nombreTiposTicket": nombreTiposTicket,
                     "fecha": fecha, "empleado": empleado,
                     "sedeInicial_id": sedeInicial_id, "tiposTurnoInicial_id": tiposTurnoInicial_id,
                     "nombreTiposTurnoInicial": nombreTiposTurnoInicial,
                     "desdeInicial": desdeInicial, "hastaInicial": hastaInicial})

        miConexion.close()
        print("tickets")
        print(tickets)

        # Cierro Conexion
        print ("Me devuelvo a la MODAL")

        return JsonResponse({'pk':tickets[0]['id'],'sede_id':tickets[0]['sede_id'],
                             'nom_sede': tickets[0]['nom_sede'],
                             'tiposTicket_id':tickets[0]['tiposTicket_id'],'nombreTiposTicket':tickets[0]['fecha'], 'tiposCompra':tickets[0]['fecha'],
                             'empleado':tickets[0]['empleado'],
                             'sedeInicial_id': tickets[0]['sedeInicial_id'],
                             'tiposTurnoInicial_id': tickets[0]['tiposTurnoInicial_id'],
                             'nombreTiposTurnoInicial':tickets[0]['nombreTiposTurnoInicial'],
                             'desdeInicial':tickets[0]['desdeInicial'],'hastaInicial':tickets[0]['hastaInicial']
                              })
    else:
        return JsonResponse({'errors':'Something went wrong!'})
