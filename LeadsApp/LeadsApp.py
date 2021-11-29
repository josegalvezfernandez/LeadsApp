# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 13:39:37 2021
@author: Usuario
"""
from typing import Any, Union

import pandas as pd
import sys
from datetime import datetime
import os.path

from pandas import DataFrame, Series
from pandas.io.parsers import TextFileReader
from pandastable import Table, TableModel
import tkinter as tk
from PIL import ImageTk,Image
from Mensajes import VentanaMensajes
from LoginLeads import VentanaLoginLeads
from Filtros import VentanaAnyadirFiltro
import ConfiguracionVentanas as conf
from Email import EmailReader
from DatosLead import VentanaDatosLead
from GestorLeads import LeadMaduracion,LeadSiNoNSNC
from Eventos import VentanaEventos
from GestorEventos import EventoEstado
from datetime import date

class LeadsApp(tk.Frame):
    

        RUTA_LEADS = "Leads.csv"
        COLUMNAS_LEADS = ["Nombre", "Email", "Teléfono", "Fecha captación",
                    "Modo captación","Tipología","Promoción de interés",
                    "Maduración","Capacidad entrada","Profesión","Tipo de contrato","Ingresos mensuales familia",
                    "Endeudamiento","Años máximo hipoteca","Avalistas","Comentarios"]
        RUTA_MENSAJES = "Mensajes.csv"
        COLUMNAS_MENSAJES = ["Email","Fecha","Asunto","Mensaje","Lista adjuntos","Recibido","Enviado"]
        RUTA_EVENTOS = "Eventos.csv"
        COLUMNAS_EVENTOS = ["Email","Tipo","Fecha","Lugar","Estado","Comentarios"]

        def __init__(self,master,df=None, df_mensajes = None, df_eventos = None):
                    tk.Frame.__init__(self)#Construye el objeto del padre y nosotros podemos añadir nuevas cosas (ampliaciones de la clase hija)
                    self.table = None
                    self.df = df
                    self.df_mensajes = df_mensajes
                    self.df_eventos = df_eventos
                    self.email_recordado = ''
                    self.password_recordado = ''
                    self.master = master
                    self.master.protocol("WM_DELETE_WINDOW",self.cm_salir)
                    self.master.geometry('1000x1000+0+0')
                    self.master.title('Datos Clientes')
                    self.create_icons()
                    self.create_buttons()
                    self.create_menu()
                    self.abrir()


                    
        def create_icons(self):
            
            self.imagen_filtrar = Image.open(r"LeadsApp/Iconos/ICON_Filter.png")# el r es rawstrin no trata caracteres espaeciales como \
            self.imagen_filtrar = self.imagen_filtrar.resize((conf.TAMAÑO_BOTON,conf.TAMAÑO_BOTON),Image.ANTIALIAS)
            self.icono_filtrar = ImageTk.PhotoImage(self.imagen_filtrar)#Creas el icono a través de la imagen
            
            self.imagen_email = Image.open(r"LeadsApp/Iconos/ICON_Email.png")# el r es rawstrin no trata caracteres espaeciales como \
            self.imagen_email = self.imagen_email.resize((conf.TAMAÑO_BOTON,conf.TAMAÑO_BOTON),Image.ANTIALIAS)
            self.icono_email = ImageTk.PhotoImage(self.imagen_email)
        
        def create_buttons(self):
            self.botones_barra = tk.Frame(self.master,borderwidth = conf.BORDERWIDTH,relief = "raised")

            self.bt_email = tk.Button(self.botones_barra,command = self.cm_email,text = "Email",image = self.icono_email)
            self.bt_email.pack(side=tk.LEFT,fill = tk.X)

            self.bt_filtrar = tk.Button(self.botones_barra,command = self.cm_añadir_filtro,text = "Añadir Filtro",state = tk.DISABLED,image = self.icono_filtrar)
            self.bt_filtrar.pack(side=tk.LEFT,fill = tk.X)

            self.botones_barra.pack(side=tk.TOP,fill = tk.X)
            
        def create_menu(self):
            self.menu_barra = tk.Menu(self.master)#Barra de Menú
            self.master.config(menu=self.menu_barra)
            
            self.menu_archivo = tk.Menu(self.menu_barra,tearoff = 0)
            self.menu_archivo.add_command(label = "Salir",command = self.cm_salir)
            
            self.menu_operaciones = tk.Menu(self.menu_barra,tearoff = 0)
            self.menu_operaciones.add_command(label = "Email", command= self.cm_email,image=self.icono_email,compound = "left")
            self.menu_operaciones.add_command(label = "Seleccionar todos", command= self.cm_seleccionar_todos,compound = "left")
            self.menu_operaciones.add_command(label = "Deseleccionar todos", command= self.cm_deseleccionar_todos,compound = "left")
            self.menu_operaciones.add_command(label="Añadir lead", command=self.cm_añadir_registro,accelerator = "Ctrl+Shift+A",compound="left")
            self.menu_operaciones.add_command(label="Modificar lead", command=self.cm_modificar_registro,compound="left")
            self.menu_operaciones.add_command(label="Borrar lead", command=self.cm_borrar_registro,compound="left")

            self.menu_filtrar = tk.Menu(self.menu_barra,tearoff = 0)
            self.menu_filtrar.add_command(label = "Añadir filtro", command= self.cm_añadir_filtro,image=self.icono_filtrar,compound = "left",state=tk.DISABLED)
            self.menu_filtrar.add_command(label = "Quitar todos los filtros", command= self.cm_quitar_filtros,compound = "left",state=tk.DISABLED)
            self.menu_archivo.add_separator()
            
            self.menu_mensajes = tk.Menu(self.menu_barra, tearoff = 0)
            self.menu_mensajes.add_command(label = "Ver mensajes", command = self.cm_ver_mensajes, compound ="left")

            self.menu_eventos = tk.Menu(self.menu_barra, tearoff = 0)
            self.menu_eventos.add_command(label = "Ver eventos", command = self.cm_ver_eventos, compound ="left")
            
            self.menu_barra.add_cascade(label = "Archivo",menu = self.menu_archivo)
            self.menu_barra.add_cascade(label = "Operaciones",menu = self.menu_operaciones)
            self.menu_barra.add_cascade(label = "Filtrado",menu = self.menu_filtrar)
            self.menu_barra.add_cascade(label = "Mensajes",menu = self.menu_mensajes)
            self.menu_barra.add_cascade(label="Eventos", menu=self.menu_eventos)
        
        def create_table(self):
            #self.frame_numero_filas = tk.Frame(self)
            #self.frame_numero_filas.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY) 
            #self.lb_numero_filas = tk.Label(self.frame_numero_filas, text=f"{self.df.shape[0]} filas",width = 10,anchor="e")
            #self.lb_numero_filas.pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
            
            if hasattr(self,"frame_table"):
                self.frame_table.destroy()
                
            self.frame_table = tk.Frame(self.master)
            self.frame_table.pack(fill=tk.BOTH,expand=1)
            self.table = Table(self.frame_table, dataframe=self.df,showtoolbar=False, showstatusbar=True)
            self.set_color_masks()
            #self.table.pack(side=tk.BOTTOM)#Metemos los botones en la parte de abajo. Además en Python si pones todo en mayusc. 
            #como en BOTTOM se refiere a una constante. NO me tengo que aprender el número, pongo tk.BOTTOM por eso hago 
            #la constante
            self.table.setSelectedRow(0)
            self.table.show()

        def set_color_masks(self):
            for maduracion in LeadMaduracion:
                mascara = self.table.model.df["Maduración"].str.contains(str(maduracion))
                color = maduracion.getcolor()
                self.table.setColorByMask("Maduración", mascara, color)

            for capacidad in LeadSiNoNSNC:
                mascara = self.table.model.df["Capacidad entrada"].str.match(str(capacidad))
                color = capacidad.getcolor()
                self.table.setColorByMask("Capacidad entrada", mascara, color)

            for avalistas in LeadSiNoNSNC:
                mascara = self.table.model.df["Avalistas"].str.match(str(avalistas))
                color = avalistas.getcolor()
                self.table.setColorByMask("Avalistas", mascara, color)

            mascara_endeudamiento_verde = self.table.model.df["Endeudamiento"] <= 0.3
            self.table.setColorByMask("Endeudamiento", mascara_endeudamiento_verde, "green")

            mascara_endeudamiento_rojo = self.table.model.df["Endeudamiento"] > 0.3 # Ponemos self.table.model.df porque si ponemos solo self.df la tabla no cambia, deberíamos estar recargando la tabla en el dibujo
            self.table.setColorByMask("Endeudamiento", mascara_endeudamiento_rojo, "red")#Aquí cambiamos los colores sobre el table no el df (table es el dibujo y el df son los datos)


        def cm_salir(self):
            self.imagen_email.close()
            self.imagen_filtrar.close()
            self.master.destroy()
            sys.exit()    
            
        def cm_email(self):
            selection = self.get_selection()
            if selection.shape[0] == 0:
                tk.messagebox.showerror("Error envío email","Ninguna fila seleccionada para enviar email. Realice una selección")
            else:
                ventanaEmail = VentanaLoginLeads(self,selection,email = self.email_recordado,password = self.password_recordado)
                
        def cm_seleccionar_todos(self):
            self.table.selectAll()
            
        def cm_deseleccionar_todos(self):
            self.table.selectNone()
            self.table.redraw()
        
        def cm_añadir_filtro(self):#Comando es abrir la ventana
            if self.df.shape[0] == 0:
                tk.messagebox.showerror("Error añadir filtro","No se puede añadir un filtro a una tabla vacía")
            else:
                VentanaAnyadirFiltro(self)

        def cm_quitar_filtros(self,borrar_lista=True):
            self.df = self.df_sin_filtros
            self.table.updateModel(TableModel(self.df))#Hemos cambiado los datos de la tabla
            self.table.redraw()#Pintar/Redibujar en la tabla que ya teníamos, hasta ahora habíamos cambiado el dataframe
            for filtro in self.lista_filtros:
                if filtro != None:
                    self.menu_filtrar.delete(f"Quitar {filtro.nombre} ")
            self.lista_filtros=[]
            self.menu_filtrar.entryconfig("Quitar todos los filtros",state = tk.DISABLED)

        def aplicar_filtro(self, filtro):
            # filtro.df = self.df
            df_anterior = self.df
            self.df = filtro.obtener_datos_filtrados(self.df)
            if self.df.shape == df_anterior.shape:
                tk.messagebox.showwarning("Filtro sin Efecto", f"Error, el filtro no filtro ninguna fila")
            else:
                self.table.updateModel(TableModel(self.df))  # Hemos cambiado los datos de la tabla
                self.table.redraw()  # Pintar/Redibujar en la tabla que ya teníamos, hasta ahora habíamos cambiado el dataframe
            longitud = len(self.lista_filtros)
            self.menu_filtrar.add_command(label=f"Quitar {filtro.nombre} ",
                                          command=lambda: self.cm_eliminar_filtro(longitud), compound="left",
                                          state=tk.NORMAL)
            self.lista_filtros.append(filtro)
            self.menu_filtrar.entryconfig("Quitar todos los filtros", state=tk.NORMAL)
            self.table.setSelectedRow(0)

        def reaplicar_filtros(self):
            self.df = self.df_sin_filtros
            for filtro in self.lista_filtros:
                if filtro != None:
                    self.df = filtro.obtener_datos_filtrados(self.df)
            self.table.updateModel(TableModel(self.df))
            self.table.redraw()

        def cm_ver_mensajes(self):
            selection = self.get_selection()
            if selection.shape[0] == 0:
                tk.messagebox.showerror("Error mostrar mensajes","Ninguna fila seleccionada para mostrar mensajes. Realice una selección")
            
            else:
                for index,row in selection.iterrows(): # row diccionario con todos los campos
                    mensajes_cliente = self.df_mensajes.loc[self.df_mensajes["Email"] == selection.iloc[index]["Email"]]
                    VentanaMensajes(self,selection.iloc[index],mensajes_cliente)


        def cm_ver_eventos(self):
            selection = self.get_selection()
            if selection.shape[0] == 0:
                tk.messagebox.showerror("Error mostrar eventos",
                                        "Ninguna fila seleccionada para mostrar mensajes. Realice una selección")

            else:
                for index, row in selection.iterrows():  # row diccionario con todos los campos
                    lead = selection.iloc[index]
                    self.mostrarEventos(lead)


        def crear_ventana_eventos(self, date, lead):
            eventos_cliente = self.df_eventos.loc[self.df_eventos["Email"] == lead["Email"]]
            VentanaEventos(self, lead, eventos_cliente,date = date)

        def cm_añadir_registro(self):

             VentanaDatosLead(self) #Pasamos un objeto de la clase LeadsApp en el parámetro self dentro de VentanaDatosLead


        def añadirLead(self, lead):
            self.df = self.df_sin_filtros
            self.df = self.df.append(lead,ignore_index = True)
            self.df_sin_filtros = self.df
            self.guardar_y_actualizar()
            self.reaplicar_filtros()

        def añadirEvento(self, evento):
            self.df_eventos = self.df_eventos.append(evento,ignore_index = True)
            self.guardar_y_actualizar()

        def añadirMensaje(self, mensaje, email, indice_evento = -1,ventana_mensajes = None, ventana_eventos = None):
            if indice_evento != -1:
                self.df_eventos.at[indice_evento,"Estado"] = str(EventoEstado.REALIZADO)
            self.df_mensajes = self.df_mensajes.append(mensaje, ignore_index=True)
            self.guardar_y_actualizar()
            lead = self.df.loc[self.df["Email"] == email].iloc[0].to_dict()#Seleccionamos con iloc[0] el primero del resultado anterior(i.e. en loc)
            if ventana_mensajes != None:#
                ventana_mensajes.destroy()
                mensajes_cliente = self.df_mensajes.loc[self.df_mensajes["Email"] == email]
                VentanaMensajes(self, lead, mensajes_cliente)
            if ventana_eventos != None:
                ventana_eventos.destroy()
                self.mostrarEventos(lead,ventana_eventos.date())#Comprobar que el date es correcto


        def mostrarEventos(self,lead,fecha=date.today()):
            # mensajes = self.df_mensajes.loc[self.df_mensajes["Email"] == lead["Email"]]
            eventos_cliente = self.df_eventos.loc[self.df_eventos["Email"] == lead["Email"]]
            VentanaEventos(self, lead, eventos_cliente,fecha).lift()




        def cm_modificar_registro(self):
            selection = self.get_selection()
            if selection.shape[0] == 0:
                tk.messagebox.showerror("Error modificar registros","Ninguna fila seleccionada para modificar registros. Realice una selección")

            else:
                for index, row in selection.iterrows():  # row diccionario con todos los campos
                    lead = row.to_dict() #Las condición es para obtener el lead
                    VentanaDatosLead(self,lead) #self al estar dentro de la Clase LeadsApp se refiere a un objeto de esa clase

        def modificarLead(self,lead,email_borrar):
            # self.df.loc[self.df["Email"] == lead["Email"]] = lead
            self.df = self.df_sin_filtros
            self.df = self.df.drop(self.df.loc[self.df["Email"] == email_borrar].index,axis=0)#Borrar filas a través del indice con axis = 0, aunque los podíamos haber evitado
            self.df = self.df.append(lead,ignore_index=True)
            self.df = self.df.sort_values(by="Fecha captación")
            self.df_sin_filtros = self.df
            self.guardar_y_actualizar()
            self.reaplicar_filtros()


        def modificarEvento(self, evento, evento_anterior):
            self.df_eventos = self.df_eventos.drop(evento_anterior["index"])
            self.df_eventos = self.df_eventos.append(evento,ignore_index = True)
            self.guardar_y_actualizar()

        def cm_borrar_registro(self):
            selection = self.get_selection()
            if selection.shape[0] == 0:
                tk.messagebox.showerror("Error eliminando registros", "Ninguna fila seleccionada para eliminar registros. Realice una selección")

            else:
                msgbox = tk.messagebox.askquestion("Borrando Leads",f"Estás seguro de que deseas eliminar {selection.shape[0]} leads?",icon = "warning")
                if msgbox == "yes":
                    self.df = self.df_sin_filtros
                    for index, row in selection.iterrows():# row diccionario con todos los campos
                        lead = row.to_dict()  # Las condición es para obtener el lead
                        self.df = self.df.drop(self.df.loc[self.df["Email"] == lead["Email"]].index,axis=0)  # Borrar filas a través del indice con axis = 0, aunque los podíamos haber evitado
                    self.df_sin_filtros = self.df
                    self.guardar_y_actualizar()
                    self.reaplicar_filtros()


        def guardar_y_actualizar(self):
            self.salvar()
            self.table.updateModel(TableModel(self.df))
            self.set_color_masks()
            self.table.setSelectedRow(0)
            self.table.redraw()

        def get_selection(self):
            selection = self.table.getSelectedRows()
            selection = pd.merge(selection,self.df,how = "inner") # Para conseguir los mensajes. En selection no están pero sí en self.df
            return selection
            
        
        def abrir(self):
            # print("Estamos en comando abrir")
            def abrir_tabla(ruta, columnas):
                if os.path.isfile(ruta):
                    return pd.read_csv(ruta)
                else:
                    return pd.DataFrame(columns=columnas)

            self.df = abrir_tabla(LeadsApp.RUTA_LEADS,LeadsApp.COLUMNAS_LEADS)
            self.df["Fecha captación"] = pd.to_datetime(self.df["Fecha captación"])
            self.df['Fecha captación'] = [time.date() for time in self.df['Fecha captación']]
            # self.df['Teléfono']= self.df['Teléfono'].map(str)
            self.df = self.df.fillna("")


            self.df_mensajes = abrir_tabla(LeadsApp.RUTA_MENSAJES, LeadsApp.COLUMNAS_MENSAJES)
            self.df_mensajes["Fecha"] = pd.to_datetime(self.df_mensajes["Fecha"])
            self.df_eventos = abrir_tabla(LeadsApp.RUTA_EVENTOS, LeadsApp.COLUMNAS_EVENTOS)
            self.df_eventos["Fecha"] = pd.to_datetime(self.df_eventos["Fecha"])
            #self.actualizarLeadsDesdeEmail() # ARREGLAR DESCARGAS CON CARLOS
            # self.df_mensajes = self.df.loc[:,["Email","Mensaje"]]
            self.salvar()
            self.df_sin_filtros = self.df
            self.bt_filtrar["state"] = tk.NORMAL # Habilitar botón de filtrar
            self.menu_filtrar.entryconfig("Añadir filtro",state = tk.NORMAL)
            self.create_table()
            # print("Tabla creada")
            self.lista_filtros = []


        def salvar(self):
            self.df.to_csv(LeadsApp.RUTA_LEADS, index = False)
            self.df_mensajes.to_csv(LeadsApp.RUTA_MENSAJES, index=False)
            self.df_eventos.to_csv(LeadsApp.RUTA_EVENTOS, index=False)

            
        def actualizarLeadsDesdeEmail(self):
            lectoremail = EmailReader("info@grupoedetica.com","QhnbFrQ34vXP","mail.grupoedetica.com")
            leadsFormulario = lectoremail.obtenerClientesFormulario()
            # leadsIdealista = lectoremail.obtenerClientesIdealista()
            self.añadirLeads(leadsFormulario)
            # self.añadirLeads(leadsIdealista)
            mensajes_lead = lectoremail.obtenerMensajesDeCliente(self.df["Email"].to_list()) #Convertimos una serie de un panda en una lista para poder recorrerlo
            self.df_mensajes = self.df_mensajes.append(mensajes_lead, ignore_index=True)
            
            
            
        def añadirLeads(self,leads):
            for lead in leads:
                mensaje = {"Email":lead["Email"],"Fecha":lead["Fecha captación"],"Asunto":"Primer contacto, mediante formulario","Mensaje":lead["Mensaje"],"Lista adjuntos":[] ,"Recibido":True,"Enviado":False}
                self.df_mensajes = self.df_mensajes.append(mensaje, ignore_index=True)
                del lead["Mensaje"]
                if lead["Email"] not in self.df["Email"].tolist():# Si el lead no existe:
                    self.df = self.df.append(lead,ignore_index=True)#Porque no tenemos indice porque es un diccionario sin indice





