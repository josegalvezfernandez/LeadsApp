import tkinter as tk
import ConfiguracionVentanas as conf
from GestorLeads import LeadTipologia,LeadMaduracion,LeadCaptacion,LeadTipoContrato,LeadPromocion,LeadSiNoNSNC, getDefaultLead
from tkcalendar import DateEntry
from datetime import date,datetime
import math
from GestorEventos import getDefaultEvento,EventoTipo,EventoEstado

class VentanaDatosEvento(tk.Toplevel):  # Toplevel es una ventana aparece por encima
    LABEL_WITH = 22
    def __init__(self, leadsapp, ventana_eventos, lead, evento=None, fecha = date.today()): # La ventana principal es leadsapp y necesitamos pasarlo como argumento para que se comunique con ella
        super().__init__(master=leadsapp.master)  # llama al constructor de Toplevel
        self.leadsapp = leadsapp
        self.evento = evento
        self.lead  = lead
        self.fecha_inicial = fecha
        self.ventana_eventos = ventana_eventos

        if evento != None: # MODIFICA (Entra en el if si el evento existe, que es lo mismo que distinto de NONE)
            self.alta = False
            self.title("Modificar Evento")
            self.evento_anterior = evento.copy() # Ponemos copy porque sino sería una referencia al mismo objeto y no una copia
            if isinstance(self.evento["Comentarios"],float) and math.isnan(self.evento["Comentarios"]):
                self.evento["Comentarios"] = ""
            if isinstance(self.evento["Lugar"], float) and math.isnan(self.evento["Lugar"]):
                self.evento["Lugar"] = ""

        else:# ESTAMOS EN ALTA
            self.alta = True
            self.title("Alta Evento")
            self.evento = getDefaultEvento(self.lead["Email"])
            self.evento["Fecha"] = self.fecha_inicial

        self.create_fields()
        self.create_buttons()

    def create_fields(self):
        self.frame_nombre = tk.Frame(self)
        self.frame_nombre.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_nombre, text="Nombre:", width=VentanaDatosEvento.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)
        self.sv_nombre = tk.StringVar(value=self.lead["Nombre"])
        self.en_nombre = tk.Entry(self.frame_nombre, textvariable=self.sv_nombre, width=55, state = tk.DISABLED)  # en es entry
        self.en_nombre.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_email = tk.Frame(self)
        self.frame_email.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_email, text="Email:", width=VentanaDatosEvento.LABEL_WITH, anchor="e").pack(side=tk.LEFT,padx=conf.PADX,pady=conf.PADY)
        self.sv_email = tk.StringVar(value=self.lead["Email"])
        self.en_email = tk.Entry(self.frame_email, textvariable=self.sv_email, width=55,state=tk.DISABLED)  # en es entry
        self.en_email.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_telefono = tk.Frame(self)
        self.frame_telefono.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_telefono, text="Teléfono:", width=VentanaDatosEvento.LABEL_WITH, anchor="e").pack(side=tk.LEFT,padx=conf.PADX,pady=conf.PADY)
        self.sv_telefono = tk.StringVar(value=self.lead["Teléfono"])
        self.en_telefono = tk.Entry(self.frame_telefono, textvariable=self.sv_telefono, width=55, state=tk.DISABLED)  # en es entry
        self.en_telefono.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_fecha = tk.Frame(self)
        self.frame_fecha.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_fecha, text="Fecha:", width=VentanaDatosEvento.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)
        self.cl_fecha = DateEntry(self.frame_fecha)
        self.cl_fecha.set_date(self.evento["Fecha"].strftime("%x"))
        self.cl_fecha.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_fecha, text="Hora:", width=10, anchor="e").pack(side=tk.LEFT,padx=2,pady=conf.PADY)
        if self.alta:
            self.var_hora = tk.IntVar(value=9)
            self.var_minuto = tk.IntVar(value=0)
        else:
            self.var_hora = tk.IntVar(value=self.evento["Fecha"].hour)
            self.var_minuto = tk.IntVar(value=self.evento["Fecha"].minute)

        self.sb_hora = tk.Spinbox(self.frame_fecha, from_=0, to=23, increment=1,width = 3,textvariable=self.var_hora)
        self.sb_hora.pack(side=tk.LEFT, padx=1, pady=conf.PADY)
        tk.Label(self.frame_fecha, text=":", width=1, anchor="e").pack(side=tk.LEFT,padx=0,pady=conf.PADY)

        self.sb_minuto = tk.Spinbox(self.frame_fecha, from_=0, to=55, increment=5, width = 3, textvariable=self.var_minuto, format = "%02.0f")
        self.sb_minuto.pack(side=tk.LEFT, padx=2
                            , pady=conf.PADY)


        self.frame_tipo = tk.Frame(self)
        self.frame_tipo.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_tipo, text="Tipo:", width=VentanaDatosEvento.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)
        self.cb_tipo = tk.ttk.Combobox(self.frame_tipo, values=EventoTipo.values(), width=55)
        self.cb_tipo.current(EventoTipo.parse(self.evento["Tipo"]).value)
        self.cb_tipo.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_lugar = tk.Frame(self)
        self.frame_lugar.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_lugar, text="Lugar:", width=VentanaDatosEvento.LABEL_WITH, anchor="e").pack(side=tk.LEFT,padx=conf.PADX,pady=conf.PADY)
        self.sv_lugar = tk.StringVar(value=self.evento["Lugar"])
        self.en_lugar = tk.Entry(self.frame_lugar, textvariable=self.sv_lugar, width=55)  # en es entry
        self.en_lugar.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_estado = tk.Frame(self)
        self.frame_estado.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_estado, text="Estado:", width=VentanaDatosEvento.LABEL_WITH, anchor="e").pack(side=tk.LEFT,padx=conf.PADX,pady=conf.PADY)
        self.cb_estado = tk.ttk.Combobox(self.frame_estado, values=EventoEstado.values(), width=55)
        self.cb_estado.current(EventoEstado.parse(self.evento["Estado"]).value)
        self.cb_estado.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_comentarios = tk.Frame(self)
        self.frame_comentarios.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_comentarios, text="Comentarios:", width=VentanaDatosEvento.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)
        self.tx_comentarios = tk.scrolledtext.ScrolledText(self.frame_comentarios, height=7, width=40, wrap=tk.WORD)
        self.tx_comentarios.insert(tk.INSERT, self.evento["Comentarios"])
        self.tx_comentarios.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

    def create_buttons(self):
        self.frame_botones = tk.Frame(self)
        self.bt_cancelar = tk.Button(self.frame_botones, text="Cancelar", command=self.destroy)
        self.bt_cancelar.pack(side=tk.RIGHT, padx=conf.PADX, pady=conf.PADY)
        self.bt_aceptar = tk.Button(self.frame_botones, text="Aceptar", command=self.cm_aceptar)
        self.bt_aceptar.pack(side=tk.RIGHT, padx=conf.PADX, pady=conf.PADY)
        self.frame_botones.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)

    def cm_aceptar(self):

        str_fecha = str(self.cl_fecha.get_date()) + " " + self.sb_hora.get() + ":" + self.sb_minuto.get() + ":0"
        fecha = datetime.strptime(str_fecha,"%Y-%m-%d %H:%M:%S")# Parseo un str a datetime.date para que puede comparar (i.e >=)
        evento = {"Email":self.lead["Email"], "Tipo":self.cb_tipo.get(), "Lugar":self.sv_lugar.get(), "Estado":self.cb_estado.get(),"Comentarios": self.tx_comentarios.get("1.0", tk.END).strip(),"Fecha":fecha}

        if self.alta:
            self.ventana_eventos.añadir_evento(evento)

        else:
            self.ventana_eventos.actualizar_evento(evento, self.evento_anterior)


        self.destroy()
















