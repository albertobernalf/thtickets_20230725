from django import forms
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from tickets.models import Empleados, Tickets, MallaTurnos
import django.core.validators
import django.core.exceptions
from django.core.exceptions import ValidationError
from django.forms.widgets import NumberInput
import datetime
from .widget import  DateTimePickerInput


class ticketsForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ticketsForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['fecha'].disabled = True
        self.fields['empleado'].disabled = True

    class Meta:
        model = Tickets

        # fields = '__all__'
        fields = ['tiposTicket', 'fecha', 'empleado','sedeInicial','tiposTurnoInicial','desdeInicial','hastaInicial','adjunto','sedeFinal' ,'tiposTurnoFinal', 'desdeFinal','hastaFinal' ,'sedeReemplazo', 'reemplazo']
        widgets = {
           'desdeInicial': forms.DateTimeInput(attrs={'type': 'datetime-local' ,'placeholder': 'yyyy-mm-ddThh:mm:ss' , 'class': 'form-control'}),
            'hastaInicial': forms.DateTimeInput(attrs={'type': 'datetime-local' ,'placeholder': 'yyyy-mm-ddThh:mm:ss', 'class': 'form-control'}),
            'desdeFinal': forms.DateTimeInput(attrs={'type': 'datetime-local' ,'placeholder': 'yyyy-mm-dd hh:mm:ss (DOB)', 'class': 'form-control'}),
            'hastaFinal': forms.DateTimeInput(attrs={'type': 'datetime-local' ,'placeholder': 'yyyy-mm-dd hh:mm:ss (DOB)', 'class': 'form-control'}),
        }


    def clean_tiposTicket(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.tiposTicket
        else:
            return self.cleaned_data['tiposTicket']

    def clean_empleado(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.empleado
        else:
            return self.cleaned_data['empleado']

    def clean_sedeInicial(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.sedeInicial
        else:
            return self.cleaned_data['sedeInicial']

    def clean_sedeFinal(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.sedeFinal
        else:
            return self.cleaned_data['sedeFinal']


class ticketsAsignacionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ticketsAsignacionForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['fecha'].disabled = True
        self.fields['empleado'].disabled = True
        self.fields['tiposTicket'].disabled = True
        self.fields['sedeInicial'].disabled = True
        self.fields['desdeInicial'].disabled = True
        self.fields['sedeFinal'].disabled = True
        self.fields['hastaFinal'].disabled = True


    class Meta:
        model = Tickets


        fields = ['id', 'fecha', 'tiposTicket', 'empleado','sedeInicial','desdeInicial','sedeFinal','hastaFinal', 'asignado']
        widgets = {
           'desdeInicial': forms.DateTimeInput(attrs={'type': 'datetime-local' ,'placeholder': 'yyyy-mm-dd hh:mm:ss ', 'class': 'form-control'}),
            'hastaInicial': forms.DateTimeInput(attrs={'type': 'datetime-local' ,'placeholder': 'yyyy-mm-dd hh:mm:ss ', 'class': 'form-control'}),
            'desdeFinal': forms.DateTimeInput(attrs={'type': 'datetime-local' ,'placeholder': 'yyyy-mm-dd hh:mm:ss (DOB)', 'class': 'form-control'}),
            'hastaFinal': forms.DateTimeInput(attrs={'type': 'datetime-local' ,'placeholder': 'yyyy-mm-dd hh:mm:ss (DOB)', 'class': 'form-control'}),
        }


    def clean_tiposTicket(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.tiposTicket
        else:
            return self.cleaned_data['tiposTicket']

    def clean_empleado(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.empleado
        else:
            return self.cleaned_data['empleado']

    def clean_sedeInicial(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.sedeInicial
        else:
            return self.cleaned_data['sedeInicial']

    def clean_sedeFinal(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.sedeFinal
        else:
            return self.cleaned_data['sedeFinal']

class ticketsForm2(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ticketsForm2, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['fecha'].disabled = True
        self.fields['empleado'].disabled = True
        self.fields['tiposTicket'].disabled = True
        self.fields['sedeInicial'].disabled = True
        self.fields['sedeFinal'].disabled = True
        self.fields['desdeInicial'].disabled = True
        self.fields['hastaInicial'].disabled = True
        self.fields['sedeFinal'].disabled = True
        self.fields['desdeFinal'].disabled = True
        self.fields['hastaFinal'].disabled = True
        self.fields['sedeReemplazo'].disabled = True
        self.fields['reemplazo'].disabled = True
        self.fields['asignado'].disabled = True
        self.fields['tiposTurnoInicial'].disabled = True
        self.fields['tiposTurnoFinal'].disabled = True
        self.fields['respuestaEmpleadoCoordinador'].disabled = True


    class Meta:
        model = Tickets

        # fields = '__all__'
        fields = ['id', 'empleado', 'fecha','tiposTicket', 'sedeInicial','tiposTurnoInicial', 'desdeInicial', 'hastaInicial', 'sedeFinal','tiposTurnoFinal',  'desdeFinal', 'hastaFinal', 'asignado',
                  'adjunto','sedeReemplazo','reemplazo','respuestaEmpleadoCoordinador','textoRespuestaCoordinador','estadoRespuestaCoordinador']
        widgets = {
            'textoRespuestaCoordinador': forms.Textarea(attrs={"rows":"3"}),
        }


    def clean_tiposTicket(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.tiposTicket
        else:
            return self.cleaned_data['tiposTicket']

    def clean_empleado(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.empleado
        else:
            return self.cleaned_data['empleado']

    def clean_sedeInicial(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.sedeInicial
        else:
            return self.cleaned_data['sedeInicial']

    def clean_sedeFinal(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.sedeFinal
        else:
            return self.cleaned_data['sedeFinal']

    def clean_fecha(self):
        print ("Entre campo fecha CLEAN")

        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.fecha
        else:
            return self.cleaned_data['fecha']

    def clean_adjunto(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.adjunto
        else:
            return self.cleaned_data['adjunto']

    def clean_sedeReemplazo(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.sedeReemplazo
        else:
            return self.cleaned_data['sedeReemplazo']

    def clean_reemplazo(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.reemplazo
        else:
            return self.cleaned_data['reemplazo']

    def clean_asignado(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.asignado
        else:
            return self.cleaned_data['asignado']

    def respuestaEmpleadoCoordinador_asignado(self):
        print ("Entre CLEAN DE respuestaEmpleadoCoordinador" )
        instance = getattr(self, 'instance', None)
        print("instance = ", instance)

        if instance and instance.pk:
            return instance.respuestaEmpleadoCoordinador
        else:
            return self.cleaned_data['respuestaEmpleadoCoordinador']



# Fin ticketsForm2

##############################################################################################
# Para ticketsForm3

class ticketsForm3(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ticketsForm3, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['tiposTicket'].disabled = True
        self.fields['empleado'].disabled = True
        self.fields['sedeInicial'].disabled = True
        self.fields['tiposTurnoInicial'].disabled = True
        self.fields['sedeFinal'].disabled = True
        self.fields['tiposTurnoFinal'].disabled = True
        self.fields['sedeReemplazo'].disabled = True
        self.fields['reemplazo'].disabled = True
        self.fields['fecha'].disabled = True
        self.fields['respuestaEmpleadoThumano'].disabled = True
        self.fields['desdeInicial'].disabled = True
        self.fields['hastaInicial'].disabled = True
        self.fields['desdeFinal'].disabled = True
        self.fields['hastaFinal'].disabled = True
        self.fields['asignado'].disabled = True


    APROBADO = 'Aprobado'
    RECHAZADO = 'Rechazado'
    PENDIENTE = 'Pendiente'
    TIPOS_ESTADOS = (
        (APROBADO, 'Aprobado'),
        (RECHAZADO, 'Rechazado'),
        (PENDIENTE, 'Pendiente'),
    )
    ACTIVO = 'A'
    INACTIVO = 'I'
    TIPOS_CHOICES = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
    )
    SI = 'S'
    NO = 'N'
    TIPO_CHOICES1 = (
        (SI, 'Si'),
        (NO, 'No'),
    )
    id = forms.IntegerField(label='Solicitud No', disabled=True, initial=0)
    tiposTicket = forms.Select()
    empleado = forms.Select()
    fecha = forms.DateTimeField()
    sedeInicial = forms.Select()
    tiposTurnoInicial = forms.Select()
    desdeInicial = forms.DateTimeField()
    hastaInicial = forms.DateTimeField()
    sedeFinal = forms.Select()
    tiposTurnoFinal = forms.Select()

    asignado = forms.Select()

    sedeReemplazo = forms.Select()
    reemplazo = forms.Select()
    respuestaEmpleadoThumano = forms.Select()
    textoRespuestaThumano = forms.CharField(widget=forms.Textarea(attrs={"rows": "5"}))
    estadoRespuestaThumano = forms.ChoiceField(choices=TIPOS_ESTADOS)
    visibleTicketEmpleado = forms.ChoiceField(choices=TIPO_CHOICES1)

    widgets = {
        'id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        'tiposTicket': forms.Select(attrs={'readonly': 'readonly','disabled':True}),
    }

    class Meta:
        model = Tickets

        # fields = '__all__'
        fields = ['id', 'empleado', 'fecha','tiposTicket', 'sedeInicial','tiposTurnoInicial', 'desdeInicial', 'hastaInicial', 'sedeFinal','tiposTurnoFinal',  'desdeFinal', 'hastaFinal', 'asignado',
                  'adjunto','sedeReemplazo','reemplazo','respuestaEmpleadoThumano','textoRespuestaThumano','estadoRespuestaThumano','visibleTicketEmpleado']


    def clean_tiposTicket(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.tiposTicket
        else:
            return self.cleaned_data['tiposTicket']

    def clean_empleado(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.empleado
        else:
            return self.cleaned_data['empleado']

    def clean_sedeInicial(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.sedeInicial
        else:
            return self.cleaned_data['sedeInicial']

    def clean_sedeFinal(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.sedeFinal
        else:
            return self.cleaned_data['sedeFinal']

    def clean_fecha(self):
        print ("Entre campo fecha CLEAN")

        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.fecha
        else:
            return self.cleaned_data['fecha']

    def clean_adjunto(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.adjunto
        else:
            return self.cleaned_data['adjunto']

    def clean_sedeReemplazo(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.sedeReemplazo
        else:
            return self.cleaned_data['sedeReemplazo']

    def clean_reemplazo(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.reemplazo
        else:
            return self.cleaned_data['reemplazo']

    def clean_asignado(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.asignado
        else:
            return self.cleaned_data['asignado']

## Fin tiicketsForm3
##############################################################################################

class mallaTurnosForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(mallaTurnosForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        self.fields['ano'].disabled = True
        self.fields['mes'].disabled = True
        self.fields['empleado'].disabled = True
        self.fields['area'].disabled = True
        self.fields['estadoReg'].disabled = True


    class Meta:
        model = MallaTurnos

        id = forms.IntegerField(label='Solicitud No', disabled=False, initial=0)
        ano = forms.IntegerField(label='Ano', disabled=True, initial=0)
        mes = forms.IntegerField(label='Mes', disabled=True, initial=0)
        empleado = forms.IntegerField(label='Empleado', disabled=True, initial=0)
        area = forms.IntegerField(label='Area', disabled=True, initial=0)
        dia1 = forms.IntegerField(label='1', disabled=True, initial=0)
        dia2 = forms.IntegerField(label='2', disabled=True, initial=0)
        dia3 = forms.IntegerField(label='3', disabled=True, initial=0)
        dia4 = forms.IntegerField(label='4', disabled=True, initial=0)
        dia5 = forms.IntegerField(label='5', disabled=True, initial=0)
        dia6 = forms.IntegerField(label='6', disabled=True, initial=0)
        dia7 = forms.IntegerField(label='7', disabled=True, initial=0)
        dia8 = forms.IntegerField(label='8', disabled=True, initial=0)
        dia9 = forms.IntegerField(label='9', disabled=True, initial=0)
        dia10 = forms.IntegerField(label='10', disabled=True, initial=0)
        dia11 = forms.IntegerField(label='11', disabled=True, initial=0)
        dia12 = forms.IntegerField(label='12', disabled=True, initial=0)
        dia13 = forms.IntegerField(label='13', disabled=True, initial=0)
        dia14 = forms.IntegerField(label='14', disabled=True, initial=0)
        dia15 = forms.IntegerField(label='15', disabled=True, initial=0)
        dia16 = forms.IntegerField(label='16', disabled=True, initial=0)
        dia17 = forms.IntegerField(label='17', disabled=True, initial=0)
        dia18 = forms.IntegerField(label='18', disabled=True, initial=0)
        dia19 = forms.IntegerField(label='19', disabled=True, initial=0)
        dia20 = forms.IntegerField(label='20', disabled=True, initial=0)
        dia21 = forms.IntegerField(label='21', disabled=True, initial=0)
        dia22 = forms.IntegerField(label='22', disabled=True, initial=0)
        dia23 = forms.IntegerField(label='23', disabled=True, initial=0)
        dia24 = forms.IntegerField(label='24', disabled=True, initial=0)
        dia25 = forms.IntegerField(label='25', disabled=True, initial=0)
        dia26 = forms.IntegerField(label='26', disabled=True, initial=0)
        dia27 = forms.IntegerField(label='27', disabled=True, initial=0)
        dia28 = forms.IntegerField(label='28', disabled=True, initial=0)
        dia29 = forms.IntegerField(label='29', disabled=True, initial=0)
        dia30 = forms.IntegerField(label='30', disabled=True, initial=0)
        dia31 = forms.IntegerField(label='31', disabled=True, initial=0)


        fields = '__all__'

        widgets = {

            'id': forms.TextInput(attrs={'class': 'form-control','readonly': 'readonly'}),
            'ano': forms.TextInput(attrs={'readonly': 'readonly'}),
            'mes': forms.TextInput(attrs={'readonly': 'readonly'}),
            'empleado': forms.Select(attrs={'readonly': 'readonly'}),
            'area': forms.Select(attrs={'readonly': 'readonly'}),

        }
