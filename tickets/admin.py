from django.contrib import admin

# Register your models here.


from tickets.models import Sedes, TiposEmpresa, TiposTicket, Areas, Ubicaciones, Cargos, TiposTurno, TiposEmpleadosPerfil, Empleados, Tickets, MallaTurnos, TicketsMalla


@admin.register(Sedes)
class sedesAdmin(admin.ModelAdmin):
    list_display = ("id", "codreg_sede", "nom_sede", "codreg_ips", "direccion", "telefono", "departamento", "municipio")
    search_fields = ("id", "codreg_sede", "nom_sede", "codreg_ips", "direccion", "telefono", "departamento", "municipio")
    # Filtrar

    list_filter = ("id", "codreg_sede", "nom_sede", "codreg_ips", "direccion", "telefono", "departamento", "municipio")

    def get_actions(self, request):
        actions = super(sedesAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(TiposEmpresa)
class tiposEmpresaAdmin(admin.ModelAdmin):
    list_display = ("id", "codigoEmpresa", "nombre","estadoReg")
    search_fields = ("id", "codigoEmpresa", "nombre","estadoReg")
    # Filtrar
    list_filter = ("id", "codigoEmpresa", "nombre","estadoReg")

@admin.register(TiposTicket)
class tiposTicketAdmin(admin.ModelAdmin):

    list_display = ("id", "nombre","estadoReg")
    search_fields = ("id", "nombre","estadoReg")
    # Filtrar
    list_filter = ("id", "nombre","estadoReg")

@admin.register(Areas)
class areasAdmin(admin.ModelAdmin):

    list_display = ("id","sedes", "nombre","estadoReg")
    search_fields = ("id","sedes_id__nom_sede", "nombre","estadoReg")
    # Filtrar
    list_filter = ("id","sedes", "nombre","estadoReg")


@admin.register(Ubicaciones)
class ubicacionesAdmin(admin.ModelAdmin):
    list_display = ("id","sedes", "nombre", "estadoReg")
    search_fields = ("id", "sedes_id__nom_sede","nombre", "estadoReg")
    # Filtrar
    list_filter = ("id","sedes", "nombre", "estadoReg")

@admin.register(Cargos)
class cargosAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "estadoReg")
    search_fields = ("id", "nombre", "estadoReg")
    # Filtrar
    list_filter = ("id", "nombre", "estadoReg")


@admin.register(TiposTurno)
class tiposTurnoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre","abrev", "desde", "hasta", "estadoReg")
    search_fields = ("id", "nombre", "abrev", "desde", "hasta", "estadoReg")
    # Filtrar
    list_filter = ("id", "nombre", "abrev","desde", "hasta", "estadoReg")

@admin.register(TiposEmpleadosPerfil)
class tiposEmpleadosPerfilAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "estadoReg")
    search_fields = ("id", "nombre", "estadoReg")
    # Filtrar
    list_filter = ("id", "nombre", "estadoReg")


@admin.register(Empleados)
class empleadosAdmin(admin.ModelAdmin):
    list_display = ("id", "tiposEmpleadoPerfil", "cedula","nombre","salario","fechaIngreso","fechaRetiro","empresa","sede", "area")
    search_fields = ("id", "tiposEmpleadoPerfil_id__nombre", "cedula","nombre","salario","fechaIngreso","fechaRetiro","empresa_id__nombre","sede_id__nom_sede", "area_id__nombre")
    # Filtrar
    list_filter =  ("id", "tiposEmpleadoPerfil", "cedula","nombre","salario","fechaIngreso","fechaRetiro","empresa","sede", "area")


@admin.register(Tickets)
class ticketsAdmin(admin.ModelAdmin):

    list_display = ("id", "tiposTicket",  "sedeInicial", "tiposTurnoInicial", "desdeInicial","hastaInicial","sedeFinal","tiposTurnoFinal","desdeFinal","hastaFinal","visibleTicketEmpleado")
    search_fields = ("id", "tiposTicket_id__nombre", "sedeInicial_id__nom_sede", "tiposTurnoInicial_id__nombre", "desdeInicial","hastaInicial","sedeFinal_id__nom_sede","tiposTurnoFinal_id__nombre","desdeFinal","hastaFinal","visibleTicketEmpleado")
    # Filtrar
    list_filter =  ("id", "tiposTicket",  "sedeInicial", "tiposTurnoInicial", "desdeInicial","hastaInicial","sedeFinal","tiposTurnoFinal","desdeFinal","hastaFinal","visibleTicketEmpleado")


@admin.register(MallaTurnos)
class mallaTurnosAdmin(admin.ModelAdmin):
    list_display = ("id", "empleado", "ano","mes","dia1","dia2","dia3","dia4","dia5","dia6","dia7","dia8","dia9","dia10","estadoReg")
    search_fields = ("id", "empleado_id__nombre", "ano","mes","dia1_id__nombre","dia2_id__nombre","dia3_id__nombre","dia4_id__nombre","dia5_id__nombre","dia6_id__nombre","dia7_id__nombre","dia8_id__nombre","dia9_id__nombre","dia10_id__nombre","estadoReg")
    # Filtrar
    list_filter = ("id", "empleado", "ano","mes","dia1","dia2","dia3","dia4","dia5","dia6","dia7","dia8","dia9","dia10","estadoReg")


@admin.register(TicketsMalla)
class ticketsMallaAdmin(admin.ModelAdmin):
    list_display =  ("id", "fecha", "empleado","ticket","mallaTurnos")
    search_fields = ("id", "fecha", "empleado_id__nombre")
    # Filtrar
    list_filter =   ("id", "fecha", "empleado_id__nombre","mallaTurnos")
