import tkinter as tk

import pandas as pd
from tkcalendar import DateEntry

import LeadsApp.VIEW.ConfiguracionVentanas as conf
from datetime import date,datetime

from LeadsApp.CONTROLLER.leadscontroller import LeadsController
from LeadsApp.MODEL.GestorEventos import EventoEstado
from LeadsApp.VIEW.Iconos import get_photo_image_evento
from LeadsApp.VIEW.VentanaDatosEvento import VentanaDatosEvento
import math
from LeadsApp.VIEW.TablaEventos import TablaEventos
from LeadsApp.VIEW.VentanaLoginEmail import VentanaLoginEmail



class VentanaEventos(tk.Toplevel):


    def __init__(self, leadsapp, lead, date=date.today(), email='', password=''):
        super().__init__(master=leadsapp.master)# No lo inicializamos nosotros porque es un
        # atributo del padre. No hacemos self.master = master, lo hace el padre donde
        # aparecerá self.master = master, el padre es tk.Toplevel que en este caso es Leads
        # App
        self.geometry(f"800x500+{leadsapp.master.winfo_width()}+0")
        # self.resizable(0,0)#No podemos cambiar el tamaño de la ventana
        self.eventos_cliente = LeadsController.get_instance().get_eventos_lead(lead["Email"])
        self.date = date
        self.title("Visor Eventos")
        self.lead = lead
        self.leadsapp = leadsapp
        # self.mensajes = mensajes
        self.crear_vista_cliente()
        self.crear_vista_eventos_cliente()
        self.deiconify()
        LeadsController.get_instance().suscribir_eventos(self)
        # self.pack(fill = tk.BOTH, padx = conf.PADX, pady = conf.PADY, expand = True)#Esta función existe en Tk frame Organiza los widgets en bloques antes de colocarlos en la ventana

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

        self.cl_evento = DateEntry(self.frame_calendar, date_pattern = "dd-mm-yyyy")
        self.cl_evento.set_date(self.date)
        self.cl_evento.pack(side=tk.TOP, padx=conf.PADX, pady=conf.PADY)
        self.cl_evento.bind("<<DateEntrySelected>>", self.__load_date_events) # Cuando seleccionamos
        # una fecha del widget calendar (i.e. <<DateEntrySelected>> ) llamamos a la función
        # self.date_entry_selected

        contenido = self.generar_contenido_eventos()
        self.frame_eventos = TablaEventos(self, content = contenido)
        self.frame_eventos.pack(anchor = tk.W, fill=tk.X, padx=conf.PADX + 30, pady=conf.PADY)

        self.crear_botones()

    def crear_botones(self):

        self.frame_botones = tk.Frame(self)
        self.bt_nuevo_evento = tk.Button(self.frame_botones,text = "Nuevo Evento", command = self.cm_nuevo_evento)
        self.bt_nuevo_evento.pack(side=tk.LEFT, fill=tk.X,  padx=conf.PADX, pady=conf.PADY)
        self.bt_cancelar = tk.Button(self.frame_botones, text = "Cerrar", command=self.destroy)
        self.bt_cancelar.pack(side=tk.RIGHT, fill=tk.X,  padx=conf.PADX, pady=conf.PADY)
        self.frame_botones.pack(side=tk.RIGHT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

    def actualizar(self):
        self.eventos_cliente = LeadsController.get_instance().get_eventos_lead(self.lead["Email"])
        self.__load_date_events()
        
    def __load_date_events(self): # Ponemos None para cuando no le pasemos funcione y
        # cuando se lo pasmos también
        ''' La función carga los even1tos de la fecha que hemos
        seleccionado'''
        # self.frame_botones.pack_forget()
        # self.frame_botones.destroy()
        # self.frame_eventos.update_content(self.generar_contenido_eventos())
        self.frame_eventos.destroy()
        self.date = self.cl_evento.get_date()
        contenido = self.generar_contenido_eventos()
        self.frame_eventos = TablaEventos(self, content=contenido)
        self.frame_eventos.pack(anchor = tk.W, fill=tk.X, padx=conf.PADX + 30, pady=conf.PADY)
        # self.crear_botones()

    def generar_contenido_eventos(self):
        ''' Ordena eventos del cliente seleccionados por fecha
         y en lugar de un str con Tipo, Hora, Estado, Lugar utilizamos una
         lista para rellenar el LabelGrid con imágenes'''

        date_selected = self.cl_evento.get_date()
        self.eventos_dia = self.eventos_cliente.loc[self.eventos_cliente["Fecha"].dt.date == date_selected]
        self.eventos_dia = self.eventos_dia.sort_values(by=["Fecha"])

        if self.eventos_dia.shape[0] == 0:# shape es para ver el tamaño del dataframe.
            # si ponemos el shape[0] es ver si es una lista sin eventos
            contenido = [["Sin Eventos"]]
        else:
            contenido = [["  Tipo  ","  Hora  ","  Estado  ","  Lugar  "]]
            for index,evento in self.eventos_dia.iterrows(): # iterrows es para recorrer un dataframe
                str_hora = str(evento["Fecha"])[-8:-3]
                fila = [(get_photo_image_evento(evento["Tipo"]),evento["Tipo"]),str_hora,evento["Estado"]]
                # fila = [(evento["Tipo"]), str_hora, evento["Estado"]]
                if isinstance(evento["Lugar"], float) and math.isnan(evento["Lugar"]):
                   evento["Lugar"] = "" #Como no existe lo ponemos a vacío
                fila.append(evento["Lugar"])
                contenido.append(fila)

        return contenido


    def scrolllistbox(event, lb):
    	global switch
    	if switch==1:
    		lb.yview_scroll(int(-4*(event.delta/120)), "units")
    		print(event)

    def cm_nuevo_evento(self):
        self.nuevo_evento = VentanaDatosEvento(self.leadsapp,self,self.lead,fecha=self.cl_evento.get_date())

    def cm_editar_evento(self, indice):
        evento = self.eventos_dia.iloc[indice].to_dict()
        evento["index"] = self.eventos_dia.index[indice]
        VentanaDatosEvento(self.leadsapp, self, self.lead, evento = evento, fecha = self.cl_evento.get_date())

    def cm_enviar_email(self, indice_tabla_eventos):
        lead_df = pd.DataFrame(self.lead , index = [0])# Conversion de Series a Dataframe
        # lead_df= self.lead.to_frame() # Series a Dataframe que no ha funcionado
        # print(lead_df)
        indice_df = self.eventos_dia.index[indice_tabla_eventos]
        VentanaLoginEmail(self.leadsapp, lead_df, indice = indice_df)

    def cm_realizar_evento(self, indice_tabla_eventos):
        indice_df = self.eventos_dia.index[indice_tabla_eventos]
        LeadsController.get_instance().realizarEvento(indice_df)

    def cm_borrar_evento(self, indice_tabla_eventos):
        indice_df = self.eventos_dia.index[indice_tabla_eventos]
        LeadsController.get_instance().borrarEvento(indice_df)




