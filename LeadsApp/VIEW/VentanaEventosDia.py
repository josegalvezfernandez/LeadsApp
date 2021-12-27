import math
import tkinter as tk
from datetime import date
from tkcalendar import DateEntry

import LeadsApp.VIEW.ConfiguracionVentanas as conf
from LeadsApp.CONTROLLER.leadscontroller import LeadsController
from LeadsApp.VIEW.Iconos import get_photo_image_action, ACCION_EDITAR, ACCION_BORRAR, ACCION_ENVIAR_EMAIL, \
    ACCION_MARCAR_REALIZADO, get_photo_image_evento
from LeadsApp.VIEW.TablaEventos import TablaEventos
from LeadsApp.VIEW.VentanaDatosEvento import VentanaDatosEvento
from LeadsApp.VIEW.VentanaLoginEmail import VentanaLoginEmail


class VentanaEventosDia(tk.Toplevel):

    def __init__(self, master, date=date.today(), email='', password=''):
        super().__init__(master=master)
        self.geometry(f"800x500+{master.winfo_width()}+0")
        self.title("Visor Eventos")
        #elegir un dia concreto?
        self.crear_vista_eventos(date)
        LeadsController.get_instance().suscribir_eventos(self)


    def crear_vista_eventos(self,date):
        self.frame_calendar = tk.Frame(self)
        self.frame_calendar.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.cl_evento = DateEntry(self.frame_calendar, date_pattern="dd-mm-yyyy")
        self.cl_evento.set_date(date)
        self.cl_evento.pack(side=tk.TOP, padx=conf.PADX, pady=conf.PADY)
        self.cl_evento.bind("<<DateEntrySelected>>", self.__load_date_events)  # Cuando seleccionamos
        # una fecha del widget calendar (i.e. <<DateEntrySelected>> ) llamamos a la función
        # self.date_entry_selected

        contenido = self.generar_contenido_eventos()
        self.frame_eventos = TablaEventos(self, content=contenido)
        self.frame_eventos.pack(anchor=tk.W, fill=tk.X, padx=conf.PADX + 30, pady=conf.PADY)

        self.crear_botones()

    def generar_contenido_eventos(self):

        date_selected = self.cl_evento.get_date()
        self.eventos_dia = LeadsController.get_instance().get_eventos_dia(date_selected)  # El parámetro sería date (i.e. hoy) no sería el que aparece en la ventana para
        self.eventos_dia = self.eventos_dia.sort_values(by=["Fecha"])

        if self.eventos_dia.shape[0] == 0:  # shape es para ver el tamaño del dataframe.
            # si ponemos el shape[0] es ver si es una lista sin eventos
            contenido = [["Sin Eventos"]]
        else:
            contenido = [["  Nombre  ","  Tipo  ", "  Hora  ", "  Estado  ", "  Lugar  "]]
            for index, evento in self.eventos_dia.iterrows():  # iterrows es para recorrer un dataframe
                str_hora = str(evento["Fecha"])[-8:-3]
                nombre = LeadsController.get_instance().get_lead_by_email(evento["Email"])["Nombre"]
                fila = [nombre,(get_photo_image_evento(evento["Tipo"]), evento["Tipo"]), str_hora, evento["Estado"]]
                if isinstance(evento["Lugar"], float) and math.isnan(evento["Lugar"]):
                    evento["Lugar"] = ""  # Como no existe lo ponemos a vacío
                fila.append(evento["Lugar"])
                contenido.append(fila)

        return contenido


    def __load_date_events(self):
        self.frame_eventos.destroy()
        contenido = self.generar_contenido_eventos()
        self.frame_eventos = TablaEventos(self, content=contenido)
        self.frame_eventos.pack(anchor=tk.W, fill=tk.X, padx=conf.PADX + 30, pady=conf.PADY)

    def actualizar(self):
        self.__load_date_events()

    def cm_editar_evento(self, indice):
        evento = self.eventos_dia.iloc[indice].to_dict()
        evento["index"] = self.eventos_dia.index[indice]
        lead = LeadsController.get_instance().get_lead_by_email(evento["Email"])
        VentanaDatosEvento(self.master, self, lead, evento = evento, fecha = self.cl_evento.get_date())

    def cm_enviar_email(self, indice_tabla_eventos):
        indice_df = self.eventos_dia.index[indice_tabla_eventos]
        VentanaLoginEmail(self.master, [self.lead["Email"]], indice = indice_df)

    def cm_realizar_evento(self, indice_tabla_eventos):
        indice_df = self.eventos_dia.index[indice_tabla_eventos]
        LeadsController.get_instance().realizarEvento(indice_df)

    def cm_borrar_evento(self, indice_tabla_eventos):
        indice_df = self.eventos_dia.index[indice_tabla_eventos]
        LeadsController.get_instance().borrarEvento(indice_df)

    def crear_botones(self):

        self.frame_botones = tk.Frame(self)
        self.bt_nuevo_evento = tk.Button(self.frame_botones, text="Nuevo Evento", command=self.cm_nuevo_evento)
        self.bt_nuevo_evento.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        self.bt_cancelar = tk.Button(self.frame_botones, text="Cerrar", command=self.destroy)
        self.bt_cancelar.pack(side=tk.RIGHT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        self.frame_botones.pack(side=tk.RIGHT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

    def cm_nuevo_evento(self):
        self.nuevo_evento = VentanaDatosEvento(self.master, self, self.lead, fecha=self.cl_evento.get_date())






















