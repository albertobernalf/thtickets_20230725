from django.db import models

# Create your models here.
from django.utils.timezone import now

class Sedes(models.Model):
    ACTIVO   = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO,'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    id = models.AutoField(primary_key=True)
    codreg_sede = models.CharField(max_length=30, default='')
    nom_sede    = models.CharField(max_length=30, default='')
    codreg_ips  = models.CharField(max_length=30, default='')
    direccion   = models.CharField(max_length=200, default='')
    telefono    = models.CharField(max_length=120, default='')
    departamento= models.CharField(max_length=120, default='')
    municipio   = models.CharField(max_length=120, default='')
    zona        = models.CharField(max_length=120, default='')
    sede = models.CharField(max_length=120, default='')
    estadoReg = models.CharField(max_length=1, default='A', editable=True,choices = TIPO_CHOICES, )

    class Meta:
        unique_together = ("codreg_sede", "nom_sede")


    def __str__(self ):
        return self.nom_sede

class TiposEmpresa(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )

    id = models.AutoField(primary_key=True)
    codigoEmpresa = models.CharField(max_length=1, default='')
    nombre        = models.CharField(max_length=30, default='')
    estadoReg = models.CharField(max_length=1, default='A', editable=True, choices=TIPO_CHOICES, )

    def __str__(self ):
        return self.nombre


class TiposTicket(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    VACACIONES = 'V'
    INCAPACIDAD = 'I'
    PERMISO = 'P'
    REEMPLAZO = 'R'
    TRASLADO_SEDE = 'T'
    CAMBIO_JORNADA = 'J'
    CALAMIDAD = 'C'
    LICENCIA_REMUNERADA = 'L'
    LICENCIA_NO_REMUNERADA = 'N'
    CAMBIO_DE_TURNO = 'X'
    TIPO_CHOICES1 = (
        (VACACIONES, 'Vacaciones'),
        (INCAPACIDAD, 'Incapacidad'),
        (PERMISO, 'Permiso'),
        (REEMPLAZO, 'Reemplazo'),
        (TRASLADO_SEDE, 'Traslado Sede'),
        (CALAMIDAD, 'Calamidad'),
        (LICENCIA_REMUNERADA, 'Licencia Remunerada'),
        (LICENCIA_NO_REMUNERADA, 'Licencia No remunerada'),
        (CAMBIO_DE_TURNO, 'Cambio de Turno'),
    )

    id = models.AutoField(primary_key=True)
    nombre        = models.CharField(max_length=30, default='')
    abrev        = models.CharField(max_length=1, blank=True,null= True, editable=True, choices=TIPO_CHOICES1, )
    estadoReg = models.CharField(max_length=1, default='A', editable=True, choices=TIPO_CHOICES, )

    def __str__(self ):
        return self.nombre


class Areas(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )

    id   = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, default='')
    sedes = models.ForeignKey('tickets.Sedes', blank=False,  null=False, on_delete=models.PROTECT, related_name='ssedes')
    estadoReg = models.CharField(max_length=1, default='A', editable=True, choices=TIPO_CHOICES, )

    def __str__(self ):
        return str(self.sedes) + ' ' + str(self.nombre)


class Ubicaciones(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    id   = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, default='')
    sedes = models.ForeignKey('tickets.Sedes', on_delete=models.PROTECT,  related_name='ssedes2')
    estadoReg = models.CharField(max_length=1, default='A', editable=True, choices=TIPO_CHOICES, )

    def __str__(self ):
        return self.nombre

class Cargos(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )

    id   = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, default='')
    estadoReg = models.CharField(max_length=1, default='A', editable=True, choices=TIPO_CHOICES, )

    def __str__(self ):
        return self.nombre

class TiposTurno(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )

    id   = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30, default='')
    abrev = models.CharField(max_length=2, blank=True, null=True)
    desde  =  models.CharField(max_length=30, blank=True, null=True)
    hasta  = models.CharField(max_length=30,blank=True, null=True)
    estadoReg = models.CharField(max_length=1, default='A', editable=True, choices=TIPO_CHOICES, )

    def __str__(self ):
        return self.nombre


class TiposEmpleadosPerfil(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )


    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=80, default='')
    estadoReg = models.CharField(max_length=1, default='A', editable=True, choices=TIPO_CHOICES, )

    def __str__(self ):
        return self.nombre


class Empleados (models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )

    id       = models.AutoField(primary_key=True)
    tiposEmpleadoPerfil = models.ForeignKey('tickets.TiposEmpleadosPerfil', on_delete=models.PROTECT, blank=False, null=True,related_name='ttiposEmpleadosPerfil')
    cedula   =  models.CharField(max_length=30, default='')
    nombre   = models.CharField(max_length=150, default='')
    salario  =  models.DecimalField(max_digits=15, decimal_places=2)
    fechaIngreso = models.DateTimeField(default=now, editable=True)
    fechaRetiro = models.DateTimeField(default=now, editable=True)
    empresa = models.ForeignKey('tickets.TiposEmpresa',  on_delete=models.PROTECT, null=True,related_name='ttiposEmpresas')
    sede  = models.ForeignKey('tickets.Sedes',  on_delete=models.PROTECT, related_name='sSedes')
    area  = models.ForeignKey('tickets.Areas',  on_delete=models.PROTECT, blank=  True, null=True,related_name='aSreas')
    ubicacion = models.ForeignKey('tickets.Ubicaciones', on_delete=models.PROTECT, blank=  True, null=True,related_name='uubicaciones')
    tiposTurno = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=  True, null=True,related_name='ttiposTurnos_3')
    cargo =  models.ForeignKey('tickets.Cargos', on_delete=models.PROTECT, blank=  True, null=True,related_name='ttiposEmpleadosPerfil_1')
    contrasena = models.CharField(max_length=20, default='')
    estadoReg = models.CharField(max_length=1, default='A', editable=True, choices=TIPO_CHOICES, )

    def __str__(self ):
        return self.nombre


class Tickets(models.Model):
    A = 'Aprobado'
    R = 'Rechazado'
    P = 'Pendiente'
    TIPOS_ESTADOS = (
        (A, 'Aprobado'),
        (R, 'Rechazado'),
        (P, 'Pendiente'),
    )
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    SI = 'S'
    NO = 'N'
    TIPO_CHOICES1 = (
        (SI, 'Si'),
        (NO, 'No'),
    )

    id = models.AutoField(primary_key=True)
    tiposTicket  = models.ForeignKey('tickets.TiposTicket',  on_delete=models.PROTECT,  related_name='ttiposTicket_1')
    #sede         = models.ForeignKey('tickets.Sedes',  on_delete=models.PROTECT, related_name='sSedes_7')
    fecha = models.DateTimeField(default=now, editable=True)
    #cedula = models.CharField(max_length=30, default='')
    empleado = models.ForeignKey('tickets.Empleados', on_delete=models.PROTECT, related_name='eempleados1')
    sedeInicial  = models.ForeignKey('tickets.Sedes',  on_delete=models.PROTECT,related_name='sSedes_1')
    tiposTurnoInicial = models.ForeignKey('tickets.TiposTurno', on_delete=models.PROTECT, blank= True, null=True,related_name='ttiposTurnos_1')
    desdeInicial =  models.DateTimeField(default=now, editable=True, blank=False, null=False)
    hastaInicial =  models.DateTimeField(default=now, editable=True, blank=False, null=False)
    sedeFinal   = models.ForeignKey('tickets.Sedes',  on_delete=models.PROTECT,blank=True, null=True,related_name='sSedes_3')
    tiposTurnoFinal = models.ForeignKey('tickets.TiposTurno', on_delete=models.PROTECT, blank=True, null=True,related_name='ttiposTurnos_2')
    desdeFinal  =  models.DateTimeField(  blank=True,null= True,editable=True)
    hastaFinal  =  models.DateTimeField(  blank=True,null= True, editable=True)
    adjunto     = models.FileField(upload_to="Uploaded Files/", blank=True,null= True)
    sedeReemplazo = models.ForeignKey('tickets.Sedes',  on_delete=models.PROTECT, blank=True, null=True, related_name='sSedes_5')
    reemplazo   = models.ForeignKey('tickets.Empleados', on_delete=models.PROTECT, blank=True, null=True,related_name='tEmpleados_1')
    asignado   = models.ForeignKey('tickets.Empleados', on_delete=models.PROTECT, blank=True, null=True,related_name='tEmpleados_7')
    respuestaEmpleadoCoordinador = models.ForeignKey('tickets.Empleados', on_delete=models.PROTECT,  blank=True,null= True,related_name='eempleados_1')
    textoRespuestaCoordinador = models.CharField(max_length=200,  blank=True,null= True)
    estadoRespuestaCoordinador = models.CharField(max_length=9, default='Pendiente', editable=True, choices=TIPOS_ESTADOS, )
    respuestaEmpleadoThumano = models.ForeignKey('tickets.Empleados',  on_delete=models.PROTECT, blank=True, null=True,related_name='eempleados_2')
    textoRespuestaThumano = models.CharField(max_length=200, blank=True,null= True)
    estadoRespuestaThumano = models.CharField(max_length=9, default='Pendiente', editable=True, choices=TIPOS_ESTADOS, )
    respuestaEmpleadoDueno = models.ForeignKey('tickets.Empleados',  on_delete=models.PROTECT,  blank=True,null= True,  related_name='eempleados_3')
    textoRespuestaDueno = models.CharField(max_length=200,  blank=True,null= True)
    estadoRespuestaDueno = models.CharField(max_length=9, default='Pendiente', editable=True, choices=TIPOS_ESTADOS, )
    visibleTicketEmpleado = models.CharField(max_length=1, default='N', editable=True, choices=TIPO_CHOICES1, )
    estadoReg  = models.CharField(max_length=1, default='A', editable=True, choices=TIPO_CHOICES, )

    def __str__(self ):
        return self.estadoReg

    #def get_absolute_url(self):
    #    return reverse('books:detail', args=[self.id])


class MallaTurnos(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    id = models.AutoField(primary_key=True)
    empleado = models.ForeignKey('tickets.Empleados',  on_delete=models.PROTECT, null=True, related_name='eempleados_4')
    area = models.ForeignKey('tickets.Areas', on_delete=models.PROTECT, blank=True, null=True, related_name='aareas_2')
    ano = models.IntegerField()
    mes = models.IntegerField()
    dia1 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_1')
    dia2 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_2')
    dia3 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_3')
    dia4 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_4')
    dia5 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT, blank=True,null=True,related_name='ttTiposTurno_5')
    dia6 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_6')
    dia7 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_7')
    dia8 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_8')
    dia9 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_9')
    dia10 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_10')
    dia11 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_11')
    dia12 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_12')
    dia13 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_13')
    dia14 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_14')
    dia15 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_15')
    dia16 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_16')
    dia17 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_17')
    dia18 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_18')
    dia19 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_19')
    dia20 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_20')
    dia21 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_21')
    dia22 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_22')
    dia23 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_23')
    dia24 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_24')
    dia25 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_25')
    dia26 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_26')
    dia27 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_27')
    dia28 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_28')
    dia29 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_29')
    dia30 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_30')
    dia31 = models.ForeignKey('tickets.TiposTurno',  on_delete=models.PROTECT,blank=True, null=True,related_name='ttTiposTurno_31')
    estadoReg = models.CharField(max_length=1, default='A', blank=True, null=True,editable=True, choices=TIPO_CHOICES, )

    def __str__(self):
        return self.estadoReg

class TicketsMalla(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    VACACIONES = 'V'
    INCAPACIDAD = 'I'
    PERMISO = 'P'
    REEMPLAZO = 'R'
    TRASLADO_SEDE = 'T'
    CAMBIO_JORNADA = 'J'
    CALAMIDAD = 'C'
    LICENCIA_REMUNERADA = 'L'
    LICENCIA_NO_REMUNERADA = 'N'
    CAMBIO_DE_TURNO = 'X'
    TIPO_CHOICES1 = (
        (VACACIONES, 'Vacaciones'),
        (INCAPACIDAD, 'Incapacidad'),
        (PERMISO, 'Permiso'),
        (REEMPLAZO, 'Reemplazo'),
        (TRASLADO_SEDE, 'Traslado Sede'),
        (CALAMIDAD, 'Calamidad'),
        (LICENCIA_REMUNERADA, 'Licencia Remunerada'),
        (LICENCIA_NO_REMUNERADA, 'Licencia No remunerada'),
        (CAMBIO_DE_TURNO, 'Cambio de Turno'),
    )
    id = models.AutoField(primary_key=True)
    fecha = models.DateTimeField(default=now, editable=True)
    empleado = models.ForeignKey('tickets.Empleados', on_delete=models.PROTECT, null=True, related_name='eempleados_5')
    ticket = models.ForeignKey('tickets.Tickets', on_delete=models.PROTECT, null=True, related_name='tticket1')
    mallaTurnos = models.ForeignKey('tickets.MallaTurnos', on_delete=models.PROTECT, null=True, related_name='mmalla1')
    estadoReg = models.CharField(max_length=1, default='A', editable=True, choices=TIPO_CHOICES, )

    def __str__(self):
        return self.estadoReg


class Calendario(models.Model):
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPO_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    id = models.AutoField(primary_key=True)
    ano = models.IntegerField()
    mes    = models.IntegerField()
    dia    = models.IntegerField()
    nombre   = models.CharField(max_length=2, default='')
    estadoReg = models.CharField(max_length=1, default='A', editable=True,choices = TIPO_CHOICES, )


    def __str__(self ):
        return self.nombre
