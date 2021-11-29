# -*- coding: utf-8 -*-
"""
Created on Sat May  1 18:17:07 2021

@author: Usuario
"""

import tkinter as tk
import pandas as pd
import ConfiguracionVentanas as conf
from LoginLeads import VentanaLoginLeads


class VentanaMensajes(tk.Toplevel):
    
    def __init__(self,leadsapp,lead,mensajes,email='',password=''):
        super().__init__(master=leadsapp)
        self.geometry(f"800x500+{leadsapp.master.winfo_width()}+0")
        #self.resizable(0,0)#No podemos cambiar el tamaño de la ventana
        self.leadsapp = leadsapp
        self.title("Visor Mensajes")
        self.lead = lead
        self.mensajes = mensajes
        # self.mensajes["Fecha"] = pd.to_datetime(self.mensajes["Fecha"])
        self.crear_vista_cliente()
        self.crear_vista_mensaje()
        self.deiconify()
        # self.pack(fill = tk.BOTH, expand = True)#Esta función existe en Tk frame Organiza los widgets en bloques antes de colocarlos en la ventana
    
    def crear_vista_cliente(self): # Parte de la ventana con el Nombre, Email, Teléfono
        
        self.frame_nombre = tk.Frame(self)
        self.frame_nombre.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)
        sv_nombre = tk.StringVar(value = self.lead["Nombre"]) #et es emailto
        tk.Label(self.frame_nombre, text="Nombre:",width = 10, anchor ="e").pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        self.en_nombre = tk.Entry(self.frame_nombre, textvariable=sv_nombre,width = 55,state= "disabled")#en es entry
        self.en_nombre.pack(side = tk.LEFT, fill = tk.X,padx = conf.PADX, pady = conf.PADY)
        
        self.frame_email = tk.Frame(self)
        self.frame_email.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)
        sv_email = tk.StringVar(value = self.lead["Email"]) #et es emailto
        tk.Label(self.frame_email, text="Email:",width = 10, anchor ="e").pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        self.en_email = tk.Entry(self.frame_email, textvariable=sv_email,width = 55,state= "disabled")#en es entry
        self.en_email.pack(side = tk.LEFT, fill = tk.X,padx = conf.PADX, pady = conf.PADY)
    
        self.frame_telefono = tk.Frame(self)
        self.frame_telefono.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)
        sv_telefono = tk.StringVar(value = self.lead["Teléfono"]) #et es emailto
        tk.Label(self.frame_telefono, text="Telefono:",width = 10, anchor ="e").pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        self.en_telefono = tk.Entry(self.frame_telefono, textvariable=sv_telefono,width = 55,state= "disabled")#en es entry
        self.en_telefono.pack(side = tk.LEFT, fill = tk.X,padx = conf.PADX, pady = conf.PADY)
        
    def crear_vista_mensaje(self): # Parte de la ventana con Mensajes y Fecha
        
        self.frame_mensajes = tk.Frame(self)
        tk.Label(self.frame_mensajes,text = "Mensajes:",width = 10, anchor ="e").pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        self.bt_mensaje_primero = tk.Button(self.frame_mensajes, command=self.cm_mensaje_primero,text="<<")  # Constructor de un botón
        self.bt_mensaje_primero.pack(side=tk.LEFT, fill=tk.X)
        self.bt_mensaje_anterior = tk.Button(self.frame_mensajes, command=self.cm_mensaje_anterior,text="<")  # Constructor de un botón
        self.bt_mensaje_anterior.pack(side=tk.LEFT, fill=tk.X)
        if self.mensajes.shape[0] >= 1:#shape devuelve una tupla y queremos acceder al primer valor que son las filas
            self.numero_mensaje = tk.IntVar(value=self.mensajes.shape[0])
        else:
            self.numero_mensaje = tk.IntVar(value=0)
        self.numero_mensaje.trace_add("write",self.actualizar_mensaje)#el segundo parámetro no lleva paréntesis porque no la llamamos a la función
        self.en_numero_mensaje = tk.Entry(self.frame_mensajes, textvariable=self.numero_mensaje,width = 2)#en es entry
        self.en_numero_mensaje.pack(side = tk.LEFT, fill = tk.X,padx = conf.PADX, pady = conf.PADY)
        tk.Label(self.frame_mensajes,text = "/",width = 1, anchor ="e").pack(side = tk.LEFT,padx = 1, pady = conf.PADY)
        total_mensajes = tk.IntVar(value = self.mensajes.shape[0]) #shape devuelve una tupla y queremos acceder al primer valor que son las filas
        self.en_total_mensajes = tk.Entry(self.frame_mensajes, textvariable=total_mensajes,width = 2,state= "disabled")#en es entry
        self.en_total_mensajes.pack(side = tk.LEFT, fill = tk.X,padx = conf.PADX, pady = conf.PADY)
        self.bt_mensaje_siguiente = tk.Button(self.frame_mensajes,command = self.cm_mensaje_siguiente,text = ">", state = "disabled")#Constructor de un botón
        self.bt_mensaje_siguiente.pack(side=tk.LEFT, fill=tk.X)
        self.bt_mensaje_ultimo = tk.Button(self.frame_mensajes, command=self.cm_mensaje_ultimo, text=">>",state="disabled")  # Constructor de un botón
        self.bt_mensaje_ultimo.pack(side=tk.LEFT, fill=tk.X)
        if self.mensajes.shape[0] > 1:
            self.bt_mensaje_anterior["state"] =  tk.NORMAL
        else:
            self.bt_mensaje_anterior["state"] =  tk.DISABLED
        self.frame_mensajes.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)
        
        
        self.frame_fecha = tk.Frame(self)
        tk.Label(self.frame_fecha,text = "Fecha:",width = 10, anchor ="e").pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        if self.mensajes.shape[0] == 0:
            self.sv_fecha = tk.StringVar(value="")  # Accemos a la fila 0 y columna fecha
        else:
            self.sv_fecha = tk.StringVar(value=self.mensajes.iloc[-1]["Fecha"].strftime("%d-%m-%Y %H:%M"))  # Accemos a la fila 0 y columna fecha
        self.en_fecha = tk.Entry(self.frame_fecha, textvariable=self.sv_fecha,width = 55,state= tk.DISABLED)#en es entry
        self.en_fecha.pack(side = tk.LEFT, fill = tk.X,padx = conf.PADX, pady = conf.PADY)
        self.frame_fecha.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)

        self.frame_asunto = tk.Frame(self)
        tk.Label(self.frame_asunto, text="Asunto:", width=10, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,
                                                                              pady=conf.PADY)
        if self.mensajes.shape[0] == 0:
            self.sv_asunto = tk.StringVar(value="")  # Accemos a la fila 0 y columna fecha
        else:
            self.sv_asunto = tk.StringVar(value=self.mensajes.iloc[-1]["Asunto"])  # Accemos a la fila 0 y columna fecha
        self.en_asunto = tk.Entry(self.frame_asunto, textvariable=self.sv_asunto, width=55, state=tk.DISABLED)  # en es entry
        self.en_asunto.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        self.frame_asunto.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        self.frame_mensaje = tk.Frame(self)
        self.frame_mensaje.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)
        if self.mensajes.iloc[-1]["Recibido"]:
            self.sv_mensaje = tk.StringVar(value="Mensaje:\n Recibido")
        else:
            self.sv_mensaje = tk.StringVar(value="Mensaje:\n Enviado")
        self.lb_mensaje = tk.Label(self.frame_mensaje, textvariable=self.sv_mensaje,width = 10,anchor="e")
        self.lb_mensaje.pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        self.tx_mensaje = tk.scrolledtext.ScrolledText(self.frame_mensaje,height = 7,width = 40,wrap = tk.WORD)
        if self.mensajes.shape[0] > 0:
            self.tx_mensaje.insert(tk.INSERT, self.mensajes.iloc[-1]["Mensaje"])
        self.tx_mensaje["state"] = tk.DISABLED
        self.tx_mensaje.pack(side = tk.LEFT, fill = tk.X,padx = conf.PADX, pady = conf.PADY)
        
        self.frame_enviar = tk.Frame(self)
        self.bt_send = tk.Button(self.frame_enviar, text="Enviar Email", command=self.cm_email)
        self.bt_send.pack(side = tk.RIGHT,padx = conf.PADX, pady = conf.PADY)
        self.frame_enviar.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)

    def actualizar_mensaje(self,*args):
        '''Este método puede necesitar diferentes argumentos *args,
        en función desde donde le llamamemos, como es el caso
         de pulsar un botón nosotros o cambiar el número de
        mensaje '''
        try:
            ''' Cuando introducimos a mano el número de mensaje que queremos ver y
            tenemos que borrar la casilla, entonces 
             self.numero_mensaje.get() da un
            TclError expected floating point number but got"" y no puede hacer un iloc,
            con una cadena vacía
            Entonces como la casilla de mensaje actual esta vacia y tiene un try, saltaría
            al except y por tanto pass, es decir no se pararía la ejecución
            
            '''
            mensaje_actual = self.mensajes.iloc[self.numero_mensaje.get() - 1]
            self.tx_mensaje["state"] = tk.NORMAL
            self.tx_mensaje.delete("1.0", tk.END)
            self.tx_mensaje.insert(tk.INSERT, mensaje_actual["Mensaje"])
            self.tx_mensaje["state"] = tk.DISABLED

            if mensaje_actual["Recibido"]:
                self.sv_mensaje.set("Mensaje:\n Recibido")
            else:
                self.sv_mensaje.set("Mensaje:\n Enviado")
        # self.sv_fecha.set(mensaje_actual["Fecha"].split("+")[0])
            self.sv_fecha.set(mensaje_actual["Fecha"].strftime("%d-%m-%Y %H:%M"))
            self.sv_asunto.set(mensaje_actual["Asunto"])

            self.autoconfigurar_botones()

        except:
            pass

    def cm_mensaje_primero(self):
        self.numero_mensaje.set(1)
        self.actualizar_mensaje()

    def cm_mensaje_anterior(self):
        self.numero_mensaje.set(self.numero_mensaje.get() - 1)
        self.actualizar_mensaje()
    
    def cm_mensaje_siguiente(self):
        self.numero_mensaje.set(self.numero_mensaje.get() + 1)
        self.actualizar_mensaje()

    def cm_mensaje_ultimo(self):
        self.numero_mensaje.set(self.mensajes.shape[0])
        self.actualizar_mensaje()
        self.autoconfigurar_botones()

    def autoconfigurar_botones(self):
        numero_mensaje = self.numero_mensaje.get()
        if numero_mensaje == 1 or self.mensajes.shape[0] == 1:# Si es el primero o sólo hay uno
            self.bt_mensaje_anterior["state"] = tk.DISABLED
            self.bt_mensaje_primero["state"] = tk.DISABLED
        else:
            self.bt_mensaje_anterior["state"] = tk.NORMAL
            self.bt_mensaje_primero["state"] = tk.NORMAL
        if numero_mensaje == self.mensajes.shape[0] or  self.mensajes.shape[0] == 1:#Cuando estemos en el último o bien el número de mensajes es uno
            self.bt_mensaje_siguiente["state"] = tk.DISABLED
            self.bt_mensaje_ultimo["state"] = tk.DISABLED
        else:
            self.bt_mensaje_siguiente["state"] = tk.NORMAL
            self.bt_mensaje_ultimo["state"] = tk.NORMAL

    def cm_email(self):
        lead_df = pd.DataFrame(self.lead).transpose() # Conversion de Series a Dataframe
        # lead_df= self.lead.to_frame() # Series a Dataframe que no ha funcionado
        # print(lead_df)
        ventanaEmail = VentanaLoginLeads(self.leadsapp,lead_df,ventana_mensajes = self)
