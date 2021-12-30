import tkinter as tk
from datetime import date

from tkcalendar import DateEntry
import abc#ABSTRACT BASE CLASSES
import LeadsApp.VIEW.ConfiguracionVentanas as conf
from LeadsApp.CONTROLLER.leadscontroller import LeadsController
from LeadsApp.VIEW.TablaEventos import TablaEventos
from LeadsApp.VIEW.VentanaDatosEvento import VentanaDatosEvento
from LeadsApp.VIEW.VentanaLoginEmail import VentanaLoginEmail


class VentanaEventos(tk.Toplevel):
    def __init__(self, master, lead = None, date=date.today(), email='', password=''):
        # El master es el sistema de ventanas, en otras palabras el conjunto de ventanas
        super().__init__(master=master)  # No lo inicializamos nosotros porque es un
        self.geometry(f"800x500+{master.winfo_width()}+0")
        self.lead = lead
        if self.lead != None:
            self.title("Visor Eventos Lead")
            self.crear_vista_lead()
        else:
            self.title("Visor Eventos ")

        self.crear_vista_eventos(date)
        self.deiconify()
        LeadsController.get_instance().suscribir_eventos(self)
        # self.pack(fill = tk.BOTH, padx = conf.PADX, pady = conf.PADY, expand = True)#Esta función existe en Tk frame Organiza los widgets en bloques antes de colocarlos en la ventana

    def crear_vista_lead(self):  # Parte de la ventana con el Nombre, Email, Teléfono

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

    def crear_vista_eventos(self, date):  # Parte de la ventana con Mensajes y Fecha
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

    def crear_botones(self):

        self.frame_botones = tk.Frame(self)
        self.bt_nuevo_evento = tk.Button(self.frame_botones, text="Nuevo Evento", command=self.cm_nuevo_evento)
        self.bt_nuevo_evento.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        self.bt_cancelar = tk.Button(self.frame_botones, text="Cerrar", command=self.destroy)
        self.bt_cancelar.pack(side=tk.RIGHT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        self.frame_botones.pack(side=tk.RIGHT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

    def actualizar(self):
        self.__load_date_events()

    def __load_date_events(self, *args):  # Ponemos None para cuando no le pasemos funcione y
        # cuando se lo pasmos también
        ''' La función carga los even1tos de la fecha que hemos
        seleccionado'''
        # self.frame_botones.pack_forget()
        # self.frame_botones.destroy()
        # self.frame_eventos.update_content(self.generar_contenido_eventos())
        self.frame_eventos.destroy()
        contenido = self.generar_contenido_eventos()
        self.frame_eventos = TablaEventos(self, content=contenido)
        self.frame_eventos.pack(anchor=tk.W, fill=tk.X, padx=conf.PADX + 30, pady=conf.PADY)
        # self.crear_botones()

    @abc.abstractmethod
    def generar_contenido_eventos(self):#ESTE METODO LO PROGRAMARAN LAS CLASES HIJAS
        pass

    def scrolllistbox(event, lb):
    	global switch
    	if switch==1:
    		lb.yview_scroll(int(-4*(event.delta/120)), "units")
    		print(event)

    def cm_nuevo_evento(self):
        self.nuevo_evento = VentanaDatosEvento(self.master,self,self.lead,fecha=self.cl_evento.get_date())

    def cm_editar_evento(self, indice):
        evento = self.eventos_dia.iloc[indice].to_dict()
        evento["index"] = self.eventos_dia.index[indice]
        VentanaDatosEvento(self.master, self, self.lead, evento = evento, fecha = self.cl_evento.get_date())

    def cm_enviar_email(self, indice_tabla_eventos):
        indice_df = self.eventos_dia.index[indice_tabla_eventos]
        VentanaLoginEmail(self.master, [self.lead["Email"]], indice = indice_df)

    def cm_realizar_evento(self, indice_tabla_eventos):
        indice_df = self.eventos_dia.index[indice_tabla_eventos]
        LeadsController.get_instance().realizarEvento(indice_df)

    def cm_borrar_evento(self, indice_tabla_eventos):
        indice_df = self.eventos_dia.index[indice_tabla_eventos]
        LeadsController.get_instance().borrarEvento(indice_df)





