import tkinter as tk
import ConfiguracionVentanas as conf
from tkcalendar import DateEntry
from datetime import date,datetime
from DatosEvento import VentanaDatosEvento
import pandas as pd
import math


class VentanaEventos(tk.Toplevel):

    def __init__(self, leadsapp, lead, eventos_cliente, email='', password=''):
        super().__init__(master=leadsapp.master)# No lo inicializamos nosotros porque es un
        # atributo del padre. No hacemos self.master = master, lo hace el padre donde
        # aparecerá self.master = master, el padre es tk.Toplevel que en este caso es Leads
        # App
        # self.geometry("268x157")
        # self.resizable(0,0)#No podemos cambiar el tamaño de la ventana
        self.eventos_cliente = eventos_cliente
        self.title("Visor Eventos")
        self.lead = lead
        self.leadsapp = leadsapp
        self.crear_vista_cliente()
        self.crear_vista_eventos_cliente()
        # self.pack(fill = tk.BOTH, expand = True)#Esta función existe en Tk frame Organiza los widgets en bloques antes de colocarlos en la ventana

    def crear_vista_cliente(self):  # Parte de la ventana con el Nombre, Email, Teléfono

        self.frame_nombre = tk.Frame(self)
        self.frame_nombre.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_nombre, text="Nombre:", width=10, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,
                                                                               pady=conf.PADY)
        sv_nombre = tk.StringVar(value=self.lead["Nombre"])

        self.en_nombre = tk.Entry(self.frame_nombre, textvariable=sv_nombre, width=55, state="disabled")  # en es entry
        self.en_nombre.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_email = tk.Frame(self)
        self.frame_email.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_email, text="Email:", width=10, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,
                                                                             pady=conf.PADY)
        sv_email = tk.StringVar(value=self.lead["Email"])  # et es emailto

        self.en_email = tk.Entry(self.frame_email, textvariable=sv_email, width=55, state="disabled")  # en es entry
        self.en_email.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_telefono = tk.Frame(self)
        self.frame_telefono.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_telefono, text="Telefono:", width=10, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,
                                                                                   pady=conf.PADY)
        sv_telefono = tk.StringVar(value=self.lead["Teléfono"])  # et es emailto

        self.en_telefono = tk.Entry(self.frame_telefono, textvariable=sv_telefono, width=55,
                                    state="disabled")  # en es entry
        self.en_telefono.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

    def crear_vista_eventos_cliente(self):  # Parte de la ventana con Mensajes y Fecha
        self.frame_calendar = tk.Frame(self)
        self.frame_calendar.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.cl_evento = DateEntry(self.frame_calendar)
        self.cl_evento.set_date(date.today())
        self.cl_evento.pack(side=tk.TOP, padx=conf.PADX, pady=conf.PADY)
        self.cl_evento.bind("<<DateEntrySelected>>",self.date_entry_selected) # Cuando seleccionamos
        # una fecha del widget calendar (i.e. <<DateEntrySelected>> ) llamamos a la función
        # self.date_entry_selected

        self.frame_eventos = tk.Frame(self)
        tk.Label(self.frame_eventos, text="Eventos:", width=10, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,
                                                                                 pady=conf.PADY)
        self.lb_eventos = tk.Listbox(self.frame_eventos, height=5, selectmode=tk.MULTIPLE, width=55)
        # lb es un list box no hace falta desplegarlo como el combobox
        self.lb_eventos.pack(side=tk.LEFT, fill=tk.X, padx=0, pady=0)
        self.sc_eventos = tk.Scrollbar(self.frame_eventos)  # sc scroll
        self.sc_eventos.pack(side=tk.LEFT, fill=tk.Y,
                             padx=0)  # fill ocupa el scrollbar igual que el listbox (altura del frame)
        self.sc_eventos.config(command=self.lb_eventos.yview)
        self.lb_eventos.config(yscrollcommand=self.sc_eventos.set)
        self.lb_eventos.bind("<MouseWheel>",
                             lambda event: VentanaEventos.scrolllistbox(event, self.lb_eventos))
        self.mostrar_eventos_fecha()
        self.crear_botones()


    def crear_botones(self):

        self.frame_botones = tk.Frame(self)
        self.bt_nuevo_evento = tk.Button(self.frame_botones,text = "Nuevo Evento", command = self.cm_nuevo_evento)
        self.bt_nuevo_evento.pack(side=tk.LEFT, fill=tk.X)
        self.bt_cancelar = tk.Button(self.frame_botones, text = "Cancelar", command=self.destroy)
        self.bt_cancelar.pack(side=tk.RIGHT, fill=tk.X)
        self.frame_botones.pack(side=tk.RIGHT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)


    def date_entry_selected(self, evento): # La función carga los eventos de la fecha que hemos
        # seleccionado

        self.lb_eventos.delete(0,tk.END)
        self.mostrar_eventos_fecha()


    def mostrar_eventos_fecha(self):
        date_selected = self.cl_evento.get_date()
        self.eventos_dia = self.eventos_cliente.loc[self.eventos_cliente["Fecha"].dt.date == date_selected]
        self.eventos_dia = self.eventos_dia.sort_values(by=["Fecha"])



        for index,evento in self.eventos_dia.iterrows(): # iterrows es para recorrer un dataframe
            str_hora = str(evento["Fecha"])[-8:-3]
            str_evento = f"{evento['Tipo']} {str_hora} - {evento['Estado']}" # Comillas simples, dentro del
            # fstring para que no se líe con sus propias comillas dobles
            if isinstance(evento["Lugar"], float) and math.isnan(evento["Lugar"]):
                evento["Lugar"] = None
            if evento['Lugar']:
                str_evento = str_evento + f" ({evento['Lugar']})"

            self.lb_eventos.insert(tk.END, str_evento)


        self.frame_eventos.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)

    def scrolllistbox(event, lb):
    	global switch
    	if switch==1:
    		lb.yview_scroll(int(-4*(event.delta/120)), "units")
    		print(event)

    def cm_nuevo_evento(self):
        self.nuevo_evento = VentanaDatosEvento(self.leadsapp,self,self.lead,fecha=self.cl_evento.get_date())

    def añadir_evento(self,evento):
        str_evento = f"{evento['Tipo']} - {evento['Estado']}"  # Comillas simples, dentro del
        # fstring para que no se líe con sus propias comillas dobles
        self.lb_eventos.insert(tk.END, str_evento)
        self.eventos_cliente = self.eventos_cliente.append(evento,ignore_index = True)
        self.eventos_cliente["Fecha"] = pd.to_datetime(self.eventos_cliente["Fecha"])


    def actualizar_evento(self):
        pass

    def cm_evento_anterior(self):
        self.numero_eventos.set(self.numero_eventos.get() - 1)
        self.actualizar_evento()

        self.bt_evento_siguiente["state"] = tk.NORMAL  # Constructor de un botón

        if self.numero_eventos.get() > 1:
            self.bt_evento_anterior["state"] = tk.NORMAL  # Constructor de un botón
        else:
            self.bt_evento_anterior["state"] = tk.DISABLED  # Constructor de un botón

    def cm_evento_siguiente(self):
        self.numero_eventos.set(self.numero_eventos.get() + 1)
        self.actualizar_evento()

        self.bt_evento_anterior["state"] = tk.NORMAL  # Constructor de un botón

        if self.numero_eventos.get() < self.eventos.shape[0]:
            self.bt_evento_siguiente["state"] = tk.NORMAL  # Constructor de un botón
        else:
            self.bt_evento_siguiente["state"] = tk.DISABLED  # Constructor de un botón

