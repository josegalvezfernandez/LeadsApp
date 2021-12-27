# -*- coding: utf-8 -*-
"""
Created on Mon Feb 15 12:42:23 2021

@author: Usuario
"""
from LeadsApp.VIEW.ConfiguracionVentanas import get_filename_from_IOWrapper
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from LeadsApp.VIEW import ConfiguracionVentanas as conf
from datetime import datetime
from LeadsApp.CONTROLLER.leadscontroller import LeadsController



class VentanaEnviarEmail(tk.Toplevel):#Toplevel es una ventana aparece por encima
    ''' Now we can create a new email, specifying:
            - to
            - subject
            - message'''
    
    def __init__(self, master,email_sender,destinatarios_email, indice = -1,ventana_eventos = None, ventana_mensajes = None):
        super().__init__(master=master)#llama al constructor de Toplevel. Además si refactorizamos (utilizando super) y cambiamos el nombre de la clase padre (i.e. tk.Toplevel),
        # el código sigue funcionando
       # tk.Tk.__init__(self)
        #self.resizable(0,0)
        self.title("Nuevo Email")
        self.email_sender = email_sender
        self.ventana_mensajes = ventana_mensajes
        self.ventana_eventos = ventana_eventos
        self.destinatarios_email = destinatarios_email
        self.frame_from = tk.Frame(self)
        self.frame_from.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)
        sv_from = tk.StringVar(value = email_sender.usuario) #et es emailto
        tk.Label(self.frame_from, text="De:",width = 10, anchor ="e").pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        self.en_from = tk.Entry(self.frame_from, textvariable=sv_from,width = 55,state= "disabled")#en es entry
        self.en_from.pack(side = tk.LEFT, fill = tk.X,padx = conf.PADX, pady = conf.PADY)
        self.indice = indice
        
        self.frame_to = tk.Frame(self)
        self.frame_to.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)        
        #sv_to = tk.StringVar(value = str(df["e-mail"].to_list()))#et es emailto
        tk.Label(self.frame_to, text="Para:",width = 10,anchor="e").pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        #self.sc_to = tk.Scrollbar(self.master)# sc scroll bar
        #self.sc_to.pack(side = tk.RIGHT, fill = tk.Y)
        self.en_to = scrolledtext.ScrolledText(self.frame_to, width = 55,height = 3)
        #self.en_to.config(yscrollcommand=self.sc_to.set)
        #self.sc_to.config(command=self.en_to.yview)
        # no_email = df.loc[df["Email"].astype(bool) == False] # Ojo en Clientes App viene como E-MAIL
        # if no_email.shape[0] > 0:
            # nombres_sin_email = no_email["Nombre"].to_list()
            # nombres_sin_email = [", ".join(nombres) for nombres in nombres_sin_email if len(nombres) > 0]#El join devuelve un str
            # #TRANSFORMAR NOMBRES A STRING, ES UNA LISTA DE LISTAS
            # print(nombres_sin_email)
            # tk.messagebox.showwarning("AVISO Clientes sin email",f"No se enviará el email a los siguientes clientes: {', '.join(nombres_sin_email)}")
            # self.lift()
        
        ###TODO ESTO ES POR NO PODER DEBUGGEAR
        # print(df)
        # print("tipo2",type(df))
        # print("indices",df.index) # Indices son los títulos de las filas
        # print("columnas",list(df.columns))
        
        if isinstance(self.destinatarios_email,str):
            self.en_to.insert(tk.INSERT,self.destinatarios_email +"\n")
        else:
            for email in self.destinatarios_email:
                self.en_to.insert(tk.INSERT,email +"\n")
            
            
        self.en_to["state"]="disabled"#Como no puedo desabilitarlo desde el principio (i.e. cuando lo isntancio) por eso lo hago ahora como accediendo como diccionario
        self.en_to.pack(side = tk.LEFT, fill = tk.X,padx = conf.PADX, pady = conf.PADY)
        
        
        self.frame_asunto = tk.Frame(self)
        self.frame_asunto.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)        
        sv_asunto = tk.StringVar()#emailsubject    
        tk.Label(self.frame_asunto, text="Asunto:",width = 10,anchor="e").pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        self.en_asunto = tk.Entry(self.frame_asunto, textvariable=sv_asunto, width = 55)
        self.en_asunto.pack(side = tk.LEFT, fill = tk.X,padx = conf.PADX, pady = conf.PADY)#pack es otra forma de grid (cuadrícula)
        
        self.frame_adjuntos = tk.Frame(self)
        self.frame_adjuntos.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)
        tk.Label(self.frame_adjuntos, text="Adjuntos:",width = 10,anchor="e").pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        self.lb_adjuntos = tk.Listbox(self.frame_adjuntos, height = 5,selectmode=tk.MULTIPLE,width=55)
        self.lb_adjuntos.pack(side = tk.LEFT, fill = tk.X,padx = 0, pady = 0)
        self.sc_adjuntos = tk.Scrollbar(self.frame_adjuntos)#sc scroll
        self.sc_adjuntos.pack(side = tk.LEFT,fill = tk.Y,padx=0)#fill ocupa el scrollbar igual que el listbox (altura del frame)
        self.sc_adjuntos.config(command=self.lb_adjuntos.yview)
        self.lb_adjuntos.config(yscrollcommand=self.sc_adjuntos.set)
        self.lb_adjuntos.bind("<MouseWheel>", lambda event: VentanaEnviarEmail.scrolllistbox(event, self.lb_adjuntos))
        self.bt_adjuntar = tk.Button(self.frame_adjuntos, text ="Adjuntar", command  = self.cm_adjuntar)
        self.bt_adjuntar.pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        self.bt_borrar_adjunto = tk.Button(self.frame_adjuntos, text ="Borrar Adjuntos", command  = self.cm_borrar_adjunto)
        self.bt_borrar_adjunto.pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
            
        self.frame_campos = tk.Frame(self)
        self.frame_campos.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)        
        tk.Label(self.frame_campos, text="Campo:",width = 10,anchor="e").pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        self.cb_campos=tk.ttk.Combobox(self.frame_campos, width = 40,state="readonly")
        self.cb_campos["values"]=list(LeadsController.get_instance().get_leads_columns())
        self.cb_campos.pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        self.bt_añadir = tk.Button(self.frame_campos, text ="Añadir", command  = self.cm_add)
        self.bt_añadir.pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        
        self.frame_mensaje = tk.Frame(self)
        self.frame_mensaje.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)        
        tk.Label(self.frame_mensaje, text="Mensaje:",width = 10,anchor="e").pack(side = tk.LEFT,padx = conf.PADX, pady = conf.PADY)
        self.tx_mensaje = tk.scrolledtext.ScrolledText(self.frame_mensaje,height = 20,wrap = tk.WORD)
        self.tx_mensaje.insert(tk.INSERT,"Estimado/s [Nombre]:\n\n\nUn cordial saludo.")
        self.tx_mensaje.pack(side = tk.LEFT, fill = tk.X,padx = conf.PADX, pady = conf.PADY)
        self.tx_mensaje.bind('<Tab>',self.teclear)
    
        self.frame_botones = tk.Frame(self)
        self.frame_botones.pack(fill=tk.X,padx = conf.PADX, pady = conf.PADY)        
        self.bt_send = tk.Button(self.frame_botones, text="Enviar", command=self.cm_send)
        self.bt_send.pack(side = tk.RIGHT,padx = conf.PADX, pady = conf.PADY)
        #self.bt_send["state"]=tk.DISABLED
        
        
        self.bt_salir = tk.Button(self.frame_botones, text="Cancelar", command=self.destroy)
        self.bt_salir.pack(side = tk.RIGHT,padx = conf.PADX, pady = conf.PADY)
    
    def cm_adjuntar(self):
        rutas = tk.filedialog.askopenfiles(parent = self.master,mode="r")
        if rutas:
            for ruta in rutas:
                filename = get_filename_from_IOWrapper(ruta)
                self.lb_adjuntos.insert(tk.END,filename)
        self.lift()
    
    def cm_borrar_adjunto(self):
        seleccionados = self.lb_adjuntos.curselection()
        if len(seleccionados) == 0:
            tk.messagebox.showerror("Error eliminando adjuntos",f"Selecciona algún archivo antes de pulsar borrar")
        else:
            for s in seleccionados[::-1]:#Invertimos la lista
                self.lb_adjuntos.delete(s)
    
    def cm_add(self):
        campo = self.cb_campos.get()
        if len(campo) > 0:
            self.tx_mensaje.insert(tk.INSERT,f'[{campo}]')
    
    def scrolllistbox(event, lb):
    	global switch
    	if switch==1:
    		lb.yview_scroll(int(-4*(event.delta/120)), "units")
    		print(event)
        
    
    def cm_send(self):
        tos = self.en_to.get("0.0",tk.END).strip().split("\n")#tos para varios destinatarios. Lista de listas. Lista con cada línea
        subject = self.en_asunto.get()
        msg = self.tx_mensaje.get("1.0", tk.END)
        envio_ok = 0
        envio_error = 0
        emails_error = []
        campos_bien = True
        
        if msg =="":
            tk.messagebox.showinfo("Mensaje Vacío",f"Error, texto de mensaje vacío")
        elif subject == "":
            tk.messagebox.showinfo("Asunto Vacío",f"Error, asunto de mensaje vacío")
        else: 
            for i in range(len(tos)):
                to =tos[i]
                fila = LeadsController.get_instance().get_lead_by_email(to)
                msg_transformado = self.transformar(msg, to, fila)
                if msg_transformado == "":
                    #tk.messagebox.showerror("Mensaje con fallos",f"Compruebe que el mensaje no esté vacio y que todos los campos sean correctos")
                    #envio_error = len(tos)
                    campos_bien=False
                    break
                else:
                    print(f"El mensaje transformado {msg_transformado}")
                #headers = f"From: {self.email_sender.usuario}\nTo: {to}\nSubject: {subject}\n\n" 
                #body = str(headers + msg_transformado)
                body = msg_transformado
                adjuntos = list(self.lb_adjuntos.get(0,tk.END))
                try:
                    self.email_sender.sendEmail2(to.split(","),subject,body,adjuntos=adjuntos)#hemos cambiado el to de str a lista
                    envio_ok += 1
                    data={"Email":to, "Fecha": datetime.now(), "Asunto": subject, "Mensaje": msg_transformado, "Lista adjuntos": adjuntos, "Recibido": False, "Enviado": True}
                    LeadsController.get_instance().añadirMensaje(data,indice_evento = self.indice)
                    '''LeadsController.get_instance() el PATRON SINGLETON le pedimos a la 
                    clase la instancia única'''
                except Exception as e:
                    envio_error +=1
                    emails_error.append(to)
            if campos_bien:
                if envio_error == 0:
                    tk.messagebox.showinfo("Envio correcto",f"Se enviaron {envio_ok} emails. Comprueba tu email para posibles errores en el envío")
                    self.destroy()
                else:
                    direcciones_error = ",".join(emails_error)
                    tk.messagebox.showerror("Envio con fallos",f"Se enviaron correctamnete {envio_ok} e-mails.\nNo se enviaron"+
                                            f"{envio_error} e-mails\nDirecciones erróneas: {direcciones_error} ")
        
    def transformar(self,msg,to,fila):
         #print(self.df)
         #print(to)
         #fila = self.df.loc[self.df["E-MAIL"]==to]#El df es el filtrado de la ventana anterior, donde elegimos los destinatarios
         msg_transformado = msg[:]#Es una copia
         i = 0
         while i < len(msg_transformado):#Lo hacemos por indices para mantener saltos de linea etc..
             if msg_transformado[i]=="[":
                 pos_fin = msg_transformado.find("]",i)
                 if pos_fin != -1:#Si no existe el caracter dice -1 porque es un indice no valido
                     campo = msg_transformado[i+1:pos_fin].lower()#bien escrito pero en minusculas y lo susti. por mayus
                     campo = campo[0].upper() + campo[1:] 
                     try:
                         valor = fila[campo]
                     except KeyError:
                         tk.messagebox.showerror("Error en campo",f"Error, el campo [{campo}] no existe")
                         return ""
                     if isinstance(valor,list):
                         valor = ", ".join(valor)
                     elif "fecha" in campo.lower():
                         valor = valor.strftime("%d/%m/%Y")
                         
                     else:
                         valor = str(valor)
                     msg_transformado = msg_transformado[:i]+valor+msg_transformado[pos_fin+1:]
                     i = i + len(valor) -1
             i += 1
                     
         return msg_transformado
         
    def teclear(self,event):#Este método autocompleta si tecleas el tabulador. VER self.tx_mensaje.bind('<Tab>',self.teclear)
         def buscar_campos_autocompletar(campo):
             campos = []
             for opcion in LeadsController.get_instance().get_leads_columns():
                 if opcion.startswith(campo):
                     campos.append(opcion)
             return campos
         
         posicion_cursor = self.tx_mensaje.index(tk.INSERT)
         texto_anterior = self.tx_mensaje.get("1.0", posicion_cursor)
         posicion_corchete_abierto = texto_anterior.rfind('[')
         posicion_corchete_cerrado = texto_anterior.rfind(']')
         if posicion_corchete_abierto != -1:#Si lo has encontrado
             if posicion_corchete_cerrado < posicion_corchete_abierto:
                 campo = texto_anterior[posicion_corchete_abierto+1:]
                 #print(f'campo para completar {campo}')
                 opciones = buscar_campos_autocompletar(campo.upper())
                 if len(opciones) == 1:
                     if campo != campo.upper():
                         posicion = self.tx_mensaje.index(tk.INSERT)
                         posicion_linea = int(posicion[:posicion.find(".")])
                         posicion_caracter = int(posicion[posicion.find(".")+1:])
                         posicion_inicio = str(posicion_linea)+'.'+str(posicion_caracter-len(campo))
                         self.tx_mensaje.delete(posicion_inicio,tk.INSERT)
                         self.tx_mensaje.insert(posicion_inicio,campo.upper())
                     completar = opciones[0][len(campo):]
                     self.tx_mensaje.insert(tk.INSERT,completar + ']')
                     
                    
           
         
         
         """for palabra in msg.split():
             if palabra[0] == "[" :
                 try:
                     pos_fin = palabra.index("]")#te da el indice de la subcadena en la palabra, es decir la posicion del corchete cerrado
                 except ValueError:
                     tk.messagebox.showerror(f"El campo {palabra} no se ha cerrado")
                     return ""#También podía poner None
                 campo = palabra[1:pos_fin]
                 print(campo)
                 valor = fila[campo]
                 print(f"El valor transformado es {valor}")
                 if isinstance(valor,list):
                     valor = ", ".join(valor)
                 else:
                     valor = str(valor)
                 palabra = palabra.replace(campo,valor)
                 palabra = palabra.replace("[","")
                 palabra = palabra.replace("]","")
             msg_transformado=msg_transformado+palabra+" "
         return msg_transformado""" #ESTE BUCLE NO MANTIENE LOS SALTOS DE LINEA POR ESO HACEMOS EL DE ARRIBA, QUE LO HACE POR INDICES
         
                    
         
         
                             
 