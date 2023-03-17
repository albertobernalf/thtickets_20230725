from django.contrib import admin

# Register your models here.


from tickets.models import Sedes, TiposEmpresa, TiposTicket, Areas, Ubicaciones, Cargos, TiposTurno, TiposEmpleadosPerfil, Empleados, Tickets, MallaTurnos


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
    search_fields = ("id","sedes", "nombre","estadoReg")
    # Filtrar
    list_filter = ("id","sedes", "nombre","estadoReg")


@admin.register(Ubicaciones)
class ubicacionesAdmin(admin.ModelAdmin):
    list_display = ("id","sedes", "nombre", "estadoReg")
    search_fields = ("id", "sedes","nombre", "estadoReg")
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
    list_display = ("id", "nombre", "desde", "hasta", "estadoReg")
    search_fields = ("id", "nombre", "desde", "hasta", "estadoReg")
    # Filtrar
    list_filter = ("id", "nombre", "desde", "hasta", "estadoReg")

@admin.register(TiposEmpleadosPerfil)
class tiposEmpleadosPerfilAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "estadoReg")
    search_fields = ("id", "nombre", "estadoReg")
    # Filtrar
    list_filter = ("id", "nombre", "estadoReg")


@admin.register(Empleados)
class empleadosAdmin(admin.ModelAdmin):
    list_display = ("id", "tiposEmpleadoPerfil", "cedula","nombre","salario","fechaIngreso","fechaRetiro","empresa","sede", "area")
    search_fields = ("id", "tiposEmpleadoPerfil", "cedula","nombre","salario","fechaIngreso","fechaRetiro","empresa","sede", "area")
    # Filtrar
    list_filter =  ("id", "tiposEmpleadoPerfil", "cedula","nombre","salario","fechaIngreso","fechaRetiro","empresa","sede", "area")


@admin.register(Tickets)
class ticketsAdmin(admin.ModelAdmin):

    list_display = ("id", "tiposTicket",  "sedeInicial", "tiposTurnoInicial", "desdeInicial","hastaInicial","sedeFinal","tiposTurnoFinal","desdeFinal","hastaFinal")
    search_fields = ("id", "tiposTicket", "sedeInicial", "tiposTurnoInicial", "desdeInicial","hastaInicial","sedeFinal","tiposTurnoFinal","desdeFinal","hastaFinal")
    # Filtrar
    list_filter =  ("id", "tiposTicket",  "sedeInicial", "tiposTurnoInicial", "desdeInicial","hastaInicial","sedeFinal","tiposTurnoFinal","desdeFinal","hastaFinal")



@admin.register(MallaTurnos)
class mallaTurnosAdmin(admin.ModelAdmin):
    list_display = ("id", "empleado", "año","mes","dia1","dia2","dia3","dia4","dia5","dia6","dia7","dia8","dia9","dia10")
    search_fields = ("id", "empleado", "año","mes","dia1","dia2","dia3","dia4","dia5","dia6","dia7","dia8","dia9","dia10")
    # Filtrar
    list_filter = ("id", "empleado", "año","mes","dia1","dia2","dia3","dia4","dia5","dia6","dia7","dia8","dia9","dia10")

