# -*- coding: utf-8 -*-
"""
Created on Fri May 14 12:17:44 2021

@author: Usuario
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 12:37:29 2021

@author: Usuario
"""
#from conf import conf
import tkinter as tk
from LeadsApp.CONTROLLER.Email import EmailSender
from LeadsApp.VIEW.VentanaEnviarEmail import VentanaEnviarEmail
from LeadsApp.VIEW import ConfiguracionVentanas as conf


class VentanaLoginEmail(tk.Toplevel):
    '''Here the Login window appears and receives data from:
        - Email account.
        - Password.
        Furthermore, tries to log in to your gmail account.'''
    AUTOLOGIN = True#Si le pongo False lo desactivo 
    email_recordado = None 
    password_recordado = None 
    
    def __init__(self,master,destinatarios_email, indice = -1,ventana_eventos= None, ventana_mensajes = None, email='',password=''):
        super().__init__(master=master)
        #self.geometry("268x157")
        #self.resizable(0,0)#No podemos cambiar el tamaño de la ventana
        self.title("Login Email")
        self.destinatarios_email = destinatarios_email
        self.ventana_mensajes = ventana_mensajes
        self.ventana_eventos = ventana_eventos
        self.email = email
        self.password = password
        self.indice = indice
        self.frame_usuario = tk.Frame(self)
        self.frame_usuario.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)
        sv_email = tk.StringVar()#variable de tipo string para tkinter
        
        tk.Label(self.frame_usuario, text="Email:",width = 10 ).pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)#grid(row = 0, column = 0, sticky=tk.W)
        self.en_email = tk.Entry(self.frame_usuario, textvariable=sv_email, width = 25)#en significa entry. self.frame es ek recuadro creado en la ventana
        #self.en_email.grid(row = 0, column = 1)
        self.en_email.pack(fill = tk.X,padx = conf.PADX, pady = conf.PADY)
        
        self.frame_passw = tk.Frame(self)
        self.frame_passw.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)
        sv_password = tk.StringVar()
    
        tk.Label(self.frame_passw, text="Contraseña:",width = 10).pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)#.grid(row = 1, column = 0, sticky=tk.W)
        self.en_passw = tk.Entry(self.frame_passw, textvariable=sv_password, width = 25,show = "*")        #self.en_passw.grid(row = 1, column = 1)
        self.en_passw.pack(side = tk.LEFT, fill = tk.X,padx = conf.PADX, pady = conf.PADY)
        
        if VentanaLoginEmail.AUTOLOGIN:#Atributo de la clase por eso pongo Clase.atributo. Además se pone en mayñusculas porque es una constante
            sv_email.set("josegalvez@grupoedetica.com")#"","BUSCADORIDEALISTA123")
            sv_password.set("dQd(suGS0,*N")
            #sv_email.set("buscadoridealista@gmail.com")
            #sv_password.set("BUSCADORIDEALISTA123")
        else:
            sv_email.set(self.email)#"","BUSCADORIDEALISTA123")
            sv_password.set(self.password)
            
        self.bt_cancelar = tk.Button(self, text="Cancelar", command=self.destroy,width = 10)
        self.bt_cancelar.pack(side = tk.RIGHT,padx = conf.PADX, pady = conf.PADY)#.grid(row = 2, column = 1, sticky=tk.NSEW)
        
        self.bt_entrar= tk.Button(self, text="Entrar", command=self.cm_email,width = 10)
        self.bt_entrar.pack(side = tk.RIGHT,padx = conf.PADX, pady = conf.PADY)#grid(row = 2, column = 0, sticky=tk.NSEW)
 
        
 
    def cm_email(self):#cm significa comando 
        self.account = self.en_email.get()
        self.password = self.en_passw.get()
        self.master.email_recordado = self.account
        self.master.password_recordado = self.password
        self.email_sender = EmailSender(self.account,self.password,server = "cpanel.grupoedetica.com")
        #self.email_sender = EmailSender(self.account,self.password)
        VentanaEnviarEmail(self.master, self.email_sender, self.destinatarios_email, indice = self.indice, ventana_mensajes = self.ventana_mensajes, ventana_eventos = self.ventana_eventos)
        self.withdraw()#Oculta ventana

        """try:
            self.email_sender.login()
            tk.messagebox.showinfo("Conectado", "Logeado correctamente.")
            VentanaNuevoEmail(self.master,self.email_sender,self.df)
            self.withdraw()#Oculta ventana

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error realizando el login con '{self.account}'")
            print(e)
            self.deiconify()#Contrario del withdraw"""
