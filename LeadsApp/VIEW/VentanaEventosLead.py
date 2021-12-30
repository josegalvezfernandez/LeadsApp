import tkinter as tk
from functools import partial

import pandas as pd
from tkcalendar import DateEntry

import LeadsApp.VIEW.ConfiguracionVentanas as conf
from datetime import date,datetime

from LeadsApp.CONTROLLER.leadscontroller import LeadsController
from LeadsApp.MODEL.GestorEventos import EventoEstado, EventoTipo
from LeadsApp.VIEW.Iconos import get_photo_image_evento, get_photo_image_action, ACCION_EDITAR, ACCION_BORRAR, \
    ACCION_ENVIAR_EMAIL, ACCION_MARCAR_REALIZADO
from LeadsApp.VIEW.TablaEventos import TablaEventos
from LeadsApp.VIEW.VentanaDatosEvento import VentanaDatosEvento
import math

from LeadsApp.VIEW.VentanaEventos import VentanaEventos
from LeadsApp.VIEW.VentanaLoginEmail import VentanaLoginEmail



class VentanaEventosLead(VentanaEventos):


    def __init__(self, master, lead, date=date.today(), email='', password=''):
        #El master es el sistema de ventanas, en otras palabras el conjunto de ventanas
        super().__init__(master, lead=lead, date=date, email=email, password=password)# No lo inicializamos nosotros porque es un
        # atributo del padre. No hacemos self.master = master, lo hace el padre donde
        # aparecerá self.master = master, el padre es tk.Toplevel que en este caso es Leads
        # App

    def generar_contenido_eventos(self):
        ''' Ordena eventos del cliente seleccionados por fecha
         y en lugar de un str con Tipo, Hora, Estado, Lugar utilizamos una
         lista para rellenar el LabelGrid con imágenes'''

        self.eventos_cliente = LeadsController.get_instance().get_eventos_lead(self.lead["Email"])
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








