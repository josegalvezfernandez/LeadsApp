# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 13:39:37 2021
@author: Usuario
"""

import pandas as pd
import sys
import os.path

from pandastable import Table, TableModel
import tkinter as tk
from PIL import ImageTk,Image

from LeadsApp.VIEW.Iconos import get_photo_image_action, ACCION_ENVIAR_EMAIL, ACCION_VER_EVENTOS, ACCION_FILTRAR, ACCION_BORRAR, \
    ACCION_EDITAR, ACCION_AÑADIR
from LeadsApp.VIEW.VentanaMensajes import VentanaMensajes
from LeadsApp.VIEW.VentanaLoginEmail import VentanaLoginEmail
from LeadsApp.VIEW.VentanasFiltros import VentanaAnyadirFiltro
from LeadsApp.VIEW import ConfiguracionVentanas as conf
from LeadsApp.VIEW.DatosLead import VentanaDatosLead
from LeadsApp.MODEL.GestorLeads import LeadMaduracion,LeadSiNoNSNC
from LeadsApp.VIEW.VentanaEventos import VentanaEventos
from LeadsApp.CONTROLLER.leadscontroller import LeadsController


class VentanaPrincipal(tk.Frame):

        def __init__(self,master,df=None, df_mensajes = None, df_eventos = None):
            tk.Frame.__init__(self)#Construye el objeto del padre y nosotros podemos añadir nuevas cosas (ampliaciones de la clase hija)
            self.table = None
            self.email_recordado = ''
            self.password_recordado = ''
            self.master = master
            self.master.protocol("WM_DELETE_WINDOW",self.cm_salir)
            self.master.geometry('1000x1000+0+0')
            self.master.title('Datos Clientes')
            self.create_icons()
            self.create_buttons()
            self.create_menu()
            self.bt_filtrar["state"] = tk.NORMAL  # Habilitar botón de filtrar
            self.menu_filtrar.entryconfig("Añadir filtro", state=tk.NORMAL)
            self.create_table()
            # print("Tabla creada")
            self.lista_filtros = []
            LeadsController.get_instance().suscribir_leads(self)

        def create_icons(self):

            self.icono_filtrar = get_photo_image_action(ACCION_FILTRAR, width=conf.TAMAÑO_BOTON,height=conf.TAMAÑO_BOTON)
            self.icono_eventos = get_photo_image_action(ACCION_VER_EVENTOS, width=conf.TAMAÑO_BOTON,height=conf.TAMAÑO_BOTON)
            self.icono_email = get_photo_image_action(ACCION_ENVIAR_EMAIL, width = conf.TAMAÑO_BOTON,height = conf.TAMAÑO_BOTON)
            self.icono_borrar = get_photo_image_action(ACCION_BORRAR, width=conf.TAMAÑO_BOTON,height=conf.TAMAÑO_BOTON)
            self.icono_añadir = get_photo_image_action(ACCION_AÑADIR, width=conf.TAMAÑO_BOTON,height=conf.TAMAÑO_BOTON)
            self.icono_editar = get_photo_image_action(ACCION_EDITAR, width=conf.TAMAÑO_BOTON, height=conf.TAMAÑO_BOTON)

        def create_buttons(self):
            self.botones_barra = tk.Frame(self.master,borderwidth = conf.BORDERWIDTH,relief = "raised")
            self.botones_barra.pack(side=tk.TOP, fill=tk.X)

            self.bt_añadir = tk.Button(self.botones_barra, command=self.cm_añadir_lead, text="Añadir", image=self.icono_añadir)
            self.bt_añadir.pack(side=tk.LEFT, fill=tk.X)

            self.bt_borrar = tk.Button(self.botones_barra, command=self.cm_borrar_lead, text="Borrar", image=self.icono_borrar)
            self.bt_borrar.pack(side=tk.LEFT, fill=tk.X)

            self.bt_editar = tk.Button(self.botones_barra, command=self.cm_modificar_lead, text="Editar", image=self.icono_editar)
            self.bt_editar.pack(side=tk.LEFT, fill=tk.X)

            self.bt_email = tk.Button(self.botones_barra,command = self.cm_email,text = "Email",image = self.icono_email)
            self.bt_email.pack(side=tk.LEFT,fill = tk.X)

            self.bt_event = tk.Button(self.botones_barra, command=self.cm_ver_eventos, text="Eventos", image=self.icono_eventos)
            self.bt_event.pack(side=tk.LEFT, fill=tk.X)

            self.bt_filtrar = tk.Button(self.botones_barra,command = self.cm_añadir_filtro,text = "Añadir Filtro",state = tk.DISABLED,image = self.icono_filtrar)
            self.bt_filtrar.pack(side=tk.LEFT,fill = tk.X)


            
        def create_menu(self):
            self.menu_barra = tk.Menu(self.master)#Barra de Menú
            self.master.config(menu=self.menu_barra)
            
            self.menu_archivo = tk.Menu(self.menu_barra,tearoff = 0)
            self.menu_archivo.add_command(label = "Salir",command = self.cm_salir)
            
            self.menu_operaciones = tk.Menu(self.menu_barra,tearoff = 0)
            self.menu_operaciones.add_command(label = "Seleccionar todos", command= self.cm_seleccionar_todos,compound = "left")
            self.menu_operaciones.add_command(label = "Deseleccionar todos", command= self.cm_deseleccionar_todos,compound = "left")
            self.menu_operaciones.add_command(label="Añadir lead", command=self.cm_añadir_lead,image=self.icono_añadir, accelerator ="Ctrl+Shift+A", compound="left")
            self.menu_operaciones.add_command(label="Modificar lead", command=self.cm_modificar_lead,image = self.icono_editar, compound="left")
            self.menu_operaciones.add_command(label="Borrar lead", command=self.cm_borrar_lead,image = self.icono_borrar, compound="left")

            self.menu_filtrar = tk.Menu(self.menu_barra,tearoff = 0)
            self.menu_filtrar.add_command(label = "Añadir filtro", command= self.cm_añadir_filtro,image=self.icono_filtrar,compound = "left",state=tk.DISABLED)
            self.menu_filtrar.add_command(label = "Quitar todos los filtros", command= self.cm_eliminar_todos_filtros, compound ="left", state=tk.DISABLED)
            self.menu_archivo.add_separator()
            
            self.menu_mensajes = tk.Menu(self.menu_barra, tearoff = 0)
            self.menu_mensajes.add_command(label="Email", command=self.cm_email, image=self.icono_email,compound="left")
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
            self.table = Table(self.frame_table, dataframe=LeadsController.get_instance().get_leads(),showtoolbar=False, showstatusbar=True)
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
            self.master.destroy()
            sys.exit()    
            
        def cm_email(self):
            selection = self.table.getSelectedRows()
            if selection.shape[0] == 0:
                tk.messagebox.showerror("Error envío email","Ninguna fila seleccionada para enviar email. Realice una selección")
            else:
                ventanaEmail = VentanaLoginEmail(self, selection, email = self.email_recordado, password = self.password_recordado)
                
        def cm_seleccionar_todos(self):
            self.table.selectAll()
            
        def cm_deseleccionar_todos(self):
            self.table.selectNone()
            self.table.redraw()
        
        def cm_añadir_filtro(self):#Comando es abrir la ventana
            if self.table.model.df.shape[0] == 0:
                tk.messagebox.showerror("Error añadir filtro","No se puede añadir un filtro a una tabla vacía")
            else:
                VentanaAnyadirFiltro(self)

        def cm_eliminar_todos_filtros(self, borrar_lista=True):
            self.table.updateModel(TableModel(LeadsController.get_instance().get_leads()))#Hemos cambiado los datos de la tabla
            self.table.redraw()#Pintar/Redibujar en la tabla que ya teníamos, hasta ahora habíamos cambiado el dataframe
            for filtro in self.lista_filtros:
                if filtro != None:
                    self.menu_filtrar.delete(f"Quitar {filtro.nombre} ")
            self.lista_filtros=[]
            self.menu_filtrar.entryconfig("Quitar todos los filtros",state = tk.DISABLED)

        def cm_eliminar_filtro(self,indice):
            self.menu_filtrar.delete(f"Quitar {self.lista_filtros[indice].nombre} ")
            del self.lista_filtros[indice]
            copia_lista_filtros = self.lista_filtros[:]
            self.cm_eliminar_todos_filtros()
            for filtro in copia_lista_filtros:
                self.aplicar_filtro(filtro)
            
        def aplicar_filtro(self, filtro):
            df_filtrado = filtro.obtener_datos_filtrados(self.table.model.df)
            self.table.updateModel(TableModel(df_filtrado))  # Hemos cambiado los datos de la tabla
            self.table.redraw()  # Pintar/Redibujar en la tabla que ya teníamos, hasta ahora habíamos cambiado el dataframe
            longitud = len(self.lista_filtros)
            self.menu_filtrar.add_command(label=f"Quitar {filtro.nombre} ",
                                          command=lambda: self.cm_eliminar_filtro(longitud), compound="left",
                                          state=tk.NORMAL)
            self.lista_filtros.append(filtro)
            self.menu_filtrar.entryconfig("Quitar todos los filtros", state=tk.NORMAL)
            self.table.setSelectedRow(0)

        def reaplicar_filtros(self):
            df = LeadsController.get_instance().get_leads()
            for filtro in self.lista_filtros:
                if filtro != None:
                    df = filtro.obtener_datos_filtrados(df)
            self.table.updateModel(TableModel(df))
            self.table.redraw()

        def cm_ver_mensajes(self):
            selection = self.table.getSelectedRows()
            if selection.shape[0] == 0:
                tk.messagebox.showerror("Error mostrar mensajes","Ninguna fila seleccionada para mostrar mensajes. Realice una selección")
            
            else:
                for index,row in selection.iterrows(): # row fila  con todos los campos
                    lead = row.to_dict() #selection.iloc[index]
                    VentanaMensajes(self,lead)


        def cm_ver_eventos(self):
            selection = self.table.getSelectedRows()
            if selection.shape[0] == 0:
                tk.messagebox.showerror("Error mostrar eventos",
                                        "Ninguna fila seleccionada para mostrar mensajes. Realice una selección")

            else:
                for index, row in selection.iterrows():  # row fila con todos los campos
                    lead = row.to_dict()# Equivalente a selection.iloc[index] porque si a selection accedemos con el indice nos da la fila

                    VentanaEventos(self, lead).lift()


        def cm_añadir_lead(self):
             VentanaDatosLead(self) #Pasamos un objeto de la clase LeadsApp en el parámetro self dentro de VentanaDatosLead



        def cm_modificar_lead(self):
            selection = self.table.getSelectedRows()
            if selection.shape[0] == 0:
                tk.messagebox.showerror("Error modificar registros","Ninguna fila seleccionada para modificar registros. Realice una selección")

            else:
                for index, row in selection.iterrows():  # row diccionario con todos los campos
                    lead = row.to_dict() #Las condición es para obtener el lead
                    VentanaDatosLead(self,lead) #self al estar dentro de la Clase LeadsApp se refiere a un objeto de esa clase


        def cm_borrar_lead(self):
            selection = self.table.getSelectedRows()
            if selection.shape[0] == 0:
                tk.messagebox.showerror("Error eliminando registros", "Ninguna fila seleccionada para eliminar registros. Realice una selección")

            else:
                msgbox = tk.messagebox.askquestion("Borrando Leads",f"Estás seguro de que deseas eliminar {selection.shape[0]} leads?",icon = "warning")
                if msgbox == "yes":
                    # self.df = self.df_sin_filtros
                    for index, row in selection.iterrows():# row diccionario con todos los campos
                        lead = row.to_dict()  # Las condición es para obtener el lead
                        LeadsController.get_instance().borrar_lead(lead["Email"])


        def actualizar(self):
            df_leads = LeadsController.get_instance().get_leads()
            self.table.updateModel(TableModel(df_leads))
            self.reaplicar_filtros()
            self.set_color_masks()
            self.table.setSelectedRow(0)
            self.table.redraw()







