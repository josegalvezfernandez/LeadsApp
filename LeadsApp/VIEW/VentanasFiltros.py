# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 12:45:50 2021

@author: Usuario
"""

# from ClientesApp import ClientesApp

import tkinter as tk
from datetime import  date
import numpy as np
from tkcalendar import DateEntry  # Los paquetes se escriben con minúsculas y las clases
# con mayúsculas
from LeadsApp.CONTROLLER.leadscontroller import LeadsController
from LeadsApp.MODEL.Filtro import *
from LeadsApp.VIEW import ConfiguracionVentanas as conf


class VentanaAnyadirFiltro(tk.Toplevel):  # Toplevel es una ventana aparece por encima
    PORCENTAJE_INCREMENTO = 0.05

    def __init__(self, ventanaPrincipal):
        super().__init__(master=ventanaPrincipal.master)  # llama al constructor de Toplevel
        # tk.Tk.__init__(self)
        # self.resizable(0,0)
        self.title("Añadir Filtro")
        self.df = LeadsController.get_instance().get_leads()
        self.ventanaPrincipal = ventanaPrincipal
        self.frame_creados = []

        self.frame_campos = tk.Frame(self)
        self.frame_campos.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_campos, text="Campo:", width=10, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,
                                                                              pady=conf.PADY)
        self.cb_campos = tk.ttk.Combobox(self.frame_campos, width=40, state="readonly")
        self.cb_campos["values"] = list(self.df.columns.values)
        self.cb_campos.current(0)  # Selecciona el primer campo y no deja elección vacía
        self.cb_campos.pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)
        self.bt_filtrar = tk.Button(self.frame_campos, text="Seleccionar", command=self.cm_seleccionar)
        self.bt_filtrar.pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)

    def cm_seleccionar(self):
        for frame in self.frame_creados:
            frame.pack_forget()
            frame.destroy()
        self.df = self.df.infer_objects()
        self.campo = self.cb_campos.get()
        print(f"Tipo : {self.df[self.campo].dtype}")
        if self.df[self.campo].dtype == float:
            self.mostrar_filtro_float()
        elif self.df[self.campo].dtype == np.int64:  # Comprueba el tipo de la columna entera es igual a numpy int 64
            self.mostrar_filtro_int()
        elif isinstance(self.df[self.campo][0], date):  # Ver si la el primer valor de la columna es una fecha
            self.mostrar_filtro_date()
        else:
            try:
                valores = self.df[self.campo].unique()
                tengo_valores = True
            except:
                tengo_valores = False
            if tengo_valores and len(valores) <= 20:
                self.mostrar_filtro_valores(
                    valores)  # Si valores estuviera en self.valores no se lo hubiéramos pasado parametro self porque ya tiene acceso a estos parámetros
            else:
                self.mostrar_filtro_valor()

    def mostrar_filtro_float(self):
        valor_minimo = self.df[self.campo].min()
        valor_maximo = self.df[self.campo].max()

        self.anyadir_titulo_filtro()
        self.frame_maximo = tk.Frame(self)
        self.frame_maximo.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_maximo, text="Maximo:", width=10, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,
                                                                               pady=conf.PADY)
        varmax = tk.DoubleVar(value=valor_maximo)
        self.sb_maximo = tk.Spinbox(self.frame_maximo, from_=valor_minimo, to=valor_maximo, increment=(
                                                                                                                  valor_maximo - valor_minimo) * VentanaAnyadirFiltro.PORCENTAJE_INCREMENTO,
                                    textvariable=varmax)
        self.sb_maximo.pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)

        self.frame_minimo = tk.Frame(self)
        self.frame_minimo.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_minimo, text="Minimo:", width=10, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,
                                                                               pady=conf.PADY)
        varmin = tk.DoubleVar(value=valor_minimo)
        self.sb_minimo = tk.Spinbox(self.frame_minimo, from_=valor_minimo, to=valor_maximo, increment=(
                                                                                                                  valor_maximo - valor_minimo) * VentanaAnyadirFiltro.PORCENTAJE_INCREMENTO,
                                    textvariable=varmin)
        self.sb_minimo.pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)

        self.anyadir_botones_filtro(
            self.cm_aplicar_filtro_float)  # Ponemos sin parentesis porque pasamos la propia f(x) no el resultado de llamarla

        self.frame_creados = [self.frame_titulo, self.frame_maximo, self.frame_minimo, self.frame_botones]

    def mostrar_filtro_int(self):
        print("mostrar_filtro_int")
        valor_minimo = self.df[self.campo].min()
        valor_maximo = self.df[self.campo].max()

        self.anyadir_titulo_filtro()
        self.frame_maximo = tk.Frame(self)
        self.frame_maximo.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_maximo, text="Maximo:", width=10, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,
                                                                               pady=conf.PADY)
        varmax = tk.IntVar(value=valor_maximo)
        self.sb_maximo = tk.Spinbox(self.frame_maximo, from_=valor_minimo, to=valor_maximo, increment=1,
                                    textvariable=varmax)
        self.sb_maximo.pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)

        self.frame_minimo = tk.Frame(self)
        self.frame_minimo.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_minimo, text="Minimo:", width=10, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,
                                                                               pady=conf.PADY)
        varmin = tk.IntVar(value=valor_minimo)
        self.sb_minimo = tk.Spinbox(self.frame_minimo, from_=valor_minimo, to=valor_maximo, increment=1,
                                    textvariable=varmin)
        self.sb_minimo.pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)

        self.anyadir_botones_filtro(self.cm_aplicar_filtro_float)

        self.frame_creados = [self.frame_titulo, self.frame_maximo, self.frame_minimo, self.frame_botones]

    def mostrar_filtro_date(self):
        print("mostrar_filtro_date")
        valor_minimo = min(self.df[self.campo])
        valor_maximo = max(self.df[self.campo])
        print(valor_minimo, valor_maximo)

        self.anyadir_titulo_filtro()

        self.frame_minimo = tk.Frame(self)
        self.frame_minimo.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_minimo, text="Fecha Minima:", width=13, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,
                                                                                     pady=conf.PADY)
        self.cl_minimo = DateEntry(self.frame_minimo,date_pattern = "dd-mm-yyyy")
        self.cl_minimo.set_date(valor_minimo)
        self.cl_minimo.pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)

        self.frame_maximo = tk.Frame(self)
        self.frame_maximo.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_maximo, text="Fecha Maxima:", width=13, anchor="e").pack(side=tk.LEFT, fill=tk.X,
                                                                                     padx=conf.PADX, pady=conf.PADY)
        self.cl_maximo = DateEntry(self.frame_maximo, date_pattern="dd-mm-yyyy")
        self.cl_maximo.set_date(
            valor_maximo)  # valor máximo lo teníamos en datetime64 y hemos hecho un método para pasarlo a date
        self.cl_maximo.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.anyadir_botones_filtro(self.cm_aplicar_filtro_date)

        self.frame_creados = [self.frame_titulo, self.frame_maximo, self.frame_minimo, self.frame_botones]

    def mostrar_filtro_valores(self, valores):
        valores = [str(x) for x in valores]
        print(valores)
        if "nan" in valores:
            valores.remove("nan")
            valores.append("No definido")
        valores.sort()

        self.anyadir_titulo_filtro()

        self.frame_valores = tk.Frame(self)
        self.frame_valores.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        self.ck_boxes = []
        self.variables = []
        for valor in valores:  # Cada cosa (i.e. cada ck_button) en un frame diferente
            frame_valor = tk.Frame(self.frame_valores)
            frame_valor.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
            var = tk.IntVar()  # Creo una variable entera
            ck_box = tk.Checkbutton(frame_valor, text=valor, var=var, onvalue=1, offvalue=0)  # ON y OFF para var
            ck_box.pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)
            self.ck_boxes.append(ck_box)
            self.variables.append(var)

        self.frame_seleccion = tk.Frame(self)
        self.frame_seleccion.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        self.bt_todo = tk.Button(self.frame_seleccion, text="Seleccionar todos", command=self.cm_seleccionar_todos)
        self.bt_todo.pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)
        self.bt_nada = tk.Button(self.frame_seleccion, text="Deseleccionar todos", command=self.cm_deseleccionar_todos)
        self.bt_nada.pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)
        self.bt_invertir = tk.Button(self.frame_seleccion, text="Invertir seleccion",
                                     command=self.cm_invertir_seleccion)
        self.bt_invertir.pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)

        self.anyadir_botones_filtro(self.cm_aplicar_filtro_valores)

        self.frame_creados = [self.frame_titulo, self.frame_botones, self.frame_valores, self.frame_seleccion]

    def mostrar_filtro_valor(self):

        self.anyadir_titulo_filtro()

        self.frame_valor = tk.Frame(self)
        self.frame_valor.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        tk.Label(self.frame_valor, text="Valor Filtro:", width=13, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,
                                                                                    pady=conf.PADY)
        self.sv_valor = tk.StringVar()
        self.en_valor = tk.Entry(self.frame_valor, textvariable=self.sv_valor, width=55)  # en es entry
        self.en_valor.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.anyadir_botones_filtro(self.cm_aplicar_filtro_valor)

        self.frame_creados = [self.frame_titulo, self.frame_botones, self.frame_valor]

    def anyadir_titulo_filtro(self):
        self.frame_titulo = tk.Frame(self)
        self.frame_titulo.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        titulo = f"Filtro para el campo {self.campo}"
        self.lb_titulo = tk.Label(self.frame_titulo, text=titulo, width=len(titulo), anchor="e")
        self.lb_titulo.config(font="Arial 12 bold")
        self.lb_titulo.pack(anchor=tk.W)

    def anyadir_botones_filtro(self, cm_aplicar_filtro):
        self.frame_botones = tk.Frame(self)
        self.frame_botones.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        self.bt_filtrar = tk.Button(self.frame_botones, text="Filtrar", command=cm_aplicar_filtro)
        self.bt_filtrar.pack(side=tk.RIGHT, padx=conf.PADX, pady=conf.PADY)
        # self.bt_send["state"]=tk.DISABLED

        self.bt_salir = tk.Button(self.frame_botones, text="Cancelar", command=self.destroy)
        self.bt_salir.pack(side=tk.RIGHT, padx=conf.PADX, pady=conf.PADY)

    def cm_aplicar_filtro_float(self):
        minimo = float(self.sb_minimo.get())
        maximo = float(self.sb_maximo.get())
        filtro = Filtro_Float(self.campo, maximo, minimo)
        self.ventanaPrincipal.aplicar_filtro(filtro)
        self.destroy()

    def cm_aplicar_filtro_date(self):
        minimo = (self.cl_minimo.get_date())
        maximo = (self.cl_maximo.get_date())
        print(maximo, minimo)
        filtro = Filtro_Date(self.campo, maximo, minimo)
        self.ventanaPrincipal.aplicar_filtro(filtro)
        self.destroy()

    def cm_aplicar_filtro_valores(self):
        valores_seleccionados = []
        for ck_box, variable in zip(self.ck_boxes, self.variables):
            if variable.get() == 1:
                valores_seleccionados.append(ck_box.cget("text"))
        filtro = Filtro_Valores(self.campo, valores_seleccionados)
        self.ventanaPrincipal.aplicar_filtro(filtro)
        self.destroy()

    def cm_aplicar_filtro_valor(self):
        filtro = Filtro_Valor(self.campo, self.sv_valor.get())
        self.ventanaPrincipal.aplicar_filtro(filtro)
        self.destroy()

    def cm_seleccionar_todos(self):
        for variable in self.variables:
            variable.set(1)

    def cm_deseleccionar_todos(self):
        for variable in self.variables:
            variable.set(0)

    def cm_invertir_seleccion(self):
        for variable in self.variables:
            if variable.get() == 0:
                variable.set(1)
            else:
                variable.set(0)


