import tkinter as tk

from LeadsApp.CONTROLLER.leadscontroller import LeadsController
from LeadsApp.VIEW import ConfiguracionVentanas as conf
from LeadsApp.MODEL.GestorLeads import LeadTipologia,LeadMaduracion,LeadCaptacion,LeadTipoContrato,LeadPromocion,LeadSiNoNSNC, getDefaultLead
from tkcalendar import DateEntry
from datetime import date
import math

class VentanaDatosLead(tk.Toplevel):  # Toplevel es una ventana aparece por encima
    LABEL_WITH = 22
    def __init__(self, leadsapp, lead=None): # La ventana principal es leadsapp y necesitamos pasarlo como argumento para que se comunique con ella
        super().__init__(master=leadsapp.master)  # llama al constructor de Toplevel
        self.leadsapp = leadsapp
        self.lead = lead
        if lead:
            self.alta = False
            self.email_anterior = self.lead["Email"]
            self.title('Modificar lead')
            if self.lead["Tipología"] == "" or isinstance(self.lead["Tipología"],float) and math.isnan(self.lead["Tipología"]):
                self.lead["Tipología"] = str(LeadTipologia.getdefault())
            if self.lead["Maduración"] == "" or isinstance(self.lead["Maduración"],float) and math.isnan(self.lead["Maduración"]):
                self.lead["Maduración"] = str(LeadMaduracion.getdefault())
            if self.lead["Modo captación"] == "" or isinstance(self.lead["Modo captación"],float) and math.isnan(self.lead["Modo captación"]):
                self.lead["Modo captación"] = str(LeadCaptacion.getdefault())
            if self.lead["Tipo de contrato"] == "" or isinstance(self.lead["Tipo de contrato"],float) and math.isnan(self.lead["Tipo de contrato"]):
                self.lead["Tipo de contrato"] = str(LeadTipoContrato.getdefault())
            if (self.lead["Promoción de interés"] == "") or (isinstance(self.lead["Promoción de interés"],float) and math.isnan(self.lead["Promoción de interés"])):
                self.lead["Promoción de interés"] = str(LeadPromocion.getdefault())
            if (self.lead["Promoción de interés"] == "") or (isinstance(self.lead["Promoción de interés"], float) and math.isnan(self.lead["Promoción de interés"])):
                self.lead["Promoción de interés"] = str(LeadPromocion.getdefault())
            if (self.lead["Promoción de interés"] == "") or (isinstance(self.lead["Promoción de interés"],float) and math.isnan(self.lead["Promoción de interés"])):
                self.lead["Promoción de interés"] = str(LeadPromocion.getdefault())
            if isinstance(self.lead["Comentarios"],float) and math.isnan(self.lead["Comentarios"]):
                self.lead["Comentarios"] = ""
            if isinstance(self.lead["Profesión"],float) and math.isnan(self.lead["Profesión"]):
                self.lead["Profesión"] = ""
            if isinstance(self.lead["Ingresos mensuales familia"],float) and math.isnan(self.lead["Ingresos mensuales familia"]):
                self.lead["Ingresos mensuales familia"] = ""
            if isinstance(self.lead["Endeudamiento"],float) and math.isnan(self.lead["Endeudamiento"]):
                self.lead["Endeudamiento"] = ""
            if isinstance(self.lead["Años máximo hipoteca"],float) and math.isnan(self.lead["Años máximo hipoteca"]):
                self.lead["Años máximo hipoteca"] = ""
        else:
            self.alta = True
            self.title('Alta lead')
            self.lead = getDefaultLead()


        self.create_fields()
        self.create_buttons()


    def create_fields(self):
        self.frame_fecha = tk.Frame(self)
        self.frame_fecha.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_fecha, text="Fecha Captación:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,pady=conf.PADY)
        self.cl_fecha = DateEntry(self.frame_fecha)
        if self.lead["Fecha captación"] == "":
            self.cl_fecha.set_date(date.today())  # valor máximo lo teníamos en datetime64 y hemos hecho un método para pasarlo a date
        else:
            self.cl_fecha.set_date(self.lead["Fecha captación"].strftime("%x"))
        self.cl_fecha.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_modo = tk.Frame(self)
        self.frame_modo.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_modo, text="Modo captación:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)
        self.cb_modo = tk.ttk.Combobox(self.frame_modo, values=LeadCaptacion.values(),width=55)
        # if not isinstance(self.lead["Modo captación"],float) or not math.isnan(self.lead["Modo captación"]):
        self.cb_modo.current(LeadCaptacion.parse(self.lead["Modo captación"]).value)
        self.cb_modo.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_nombre = tk.Frame(self)
        self.frame_nombre.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        self.sv_nombre = tk.StringVar(value=self.lead["Nombre"])  # et es emailto
        tk.Label(self.frame_nombre, text="Nombre:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,                                                                       pady=conf.PADY)
        self.en_nombre = tk.Entry(self.frame_nombre, textvariable=self.sv_nombre, width=55)  # en es entry
        self.en_nombre.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_email = tk.Frame(self)
        self.frame_email.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        self.sv_email = tk.StringVar(value=self.lead["Email"])  # et es emailto
        tk.Label(self.frame_email, text="Email:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,                                                                             pady=conf.PADY)
        self.en_email = tk.Entry(self.frame_email, textvariable=self.sv_email, width=55)  # en es entry
        self.en_email.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_telefono = tk.Frame(self)
        self.frame_telefono.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        self.sv_telefono = tk.StringVar(value=self.lead["Teléfono"])  # et es emailto
        tk.Label(self.frame_telefono, text="Teléfono:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,pady=conf.PADY)
        self.en_telefono = tk.Entry(self.frame_telefono, textvariable=self.sv_telefono, width=55)  # en es entry
        self.en_telefono.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_promocion = tk.Frame(self)
        self.frame_promocion.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_promocion, text="Promoción:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(
            side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)
        self.cb_promocion = tk.ttk.Combobox(self.frame_promocion, values=LeadPromocion.values(), width=55)
        # if not isinstance(self.lead["Promoción de interés"],float) or not math.isnan(self.lead["Promoción de interés"]):
        self.cb_promocion.current(LeadPromocion.parse(self.lead["Promoción de interés"]).value)# ponemos como valor actual un numero que es la posición del valor del lead en la lista de valores
        self.cb_promocion.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)


        self.frame_tipologia = tk.Frame(self)
        self.frame_tipologia.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_tipologia, text="Tipología:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,pady=conf.PADY)
        self.cb_tipologia = tk.ttk.Combobox(self.frame_tipologia,values = LeadTipologia.values(), width = 55)
        # if not isinstance(self.lead["Tipología"],float) or not math.isnan(self.lead["Tipología"]):
        self.cb_tipologia.current(LeadTipologia.parse(self.lead["Tipología"]).value)
        self.cb_tipologia.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_maduracion = tk.Frame(self)
        self.frame_maduracion.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_maduracion, text="Maduración:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,pady=conf.PADY)
        self.cb_maduracion = tk.ttk.Combobox(self.frame_maduracion, values= LeadMaduracion.values(), width=55)
        # if not isinstance(self.lead["Maduración"],float) or not math.isnan(self.lead["Maduración"]):
        self.cb_maduracion.current(LeadMaduracion.parse(self.lead["Maduración"]).value)
        self.cb_maduracion.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_capacidad = tk.Frame(self)
        self.frame_capacidad.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_capacidad, text="Capacidad de Entrada:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)
        self.cb_capacidad = tk.ttk.Combobox(self.frame_capacidad,values = LeadSiNoNSNC.values(),width=55)  # ON y OFF para var
        self.cb_capacidad.current(LeadSiNoNSNC.parse(self.lead["Capacidad entrada"]).value)
        self.cb_capacidad.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_avalistas = tk.Frame(self)
        self.frame_avalistas.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_avalistas, text="Avalistas:", width=VentanaDatosLead.LABEL_WITH,anchor="e").pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)
        self.cb_avalistas = tk.ttk.Combobox(self.frame_avalistas, values=LeadSiNoNSNC.values(),width=55)  # ON y OFF para var
        self.cb_avalistas.current(LeadSiNoNSNC.parse(self.lead["Avalistas"]).value)
        self.cb_avalistas.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_profesion = tk.Frame(self)
        self.frame_profesion.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        self.sv_profesion = tk.StringVar(value=self.lead["Profesión"])  # et es emailto
        tk.Label(self.frame_profesion, text="Profesión:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,pady=conf.PADY)
        self.en_profesion = tk.Entry(self.frame_profesion, textvariable=self.sv_profesion, width=55)  # en es entry
        self.en_profesion.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_contrato = tk.Frame(self)
        self.frame_contrato.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_contrato, text="Tipo de contrato:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,pady=conf.PADY)
        self.cb_contrato = tk.ttk.Combobox(self.frame_contrato, values=LeadTipoContrato.values(), width=55)
        # if not isinstance(self.lead["Tipo de contrato"],float) or not math.isnan(self.lead["Tipo de contrato"]):
        self.cb_contrato.current(LeadTipoContrato.parse(self.lead["Tipo de contrato"]).value)
        self.cb_contrato.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

        self.frame_ingresos = tk.Frame(self)
        self.frame_ingresos.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_ingresos, text="Ingresos mensuales familia:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,pady=conf.PADY)
        self.sv_ingresos = tk.IntVar(value=self.lead["Ingresos mensuales familia"])
        self.sb_ingresos = tk.Spinbox(self.frame_ingresos, from_=0, to=1000000, increment=1000, textvariable=self.sv_ingresos)
        self.sb_ingresos.pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)

        self.frame_endeudamiento = tk.Frame(self)
        self.frame_endeudamiento.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_endeudamiento, text="Endeudamiento:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,pady=conf.PADY)
        self.sv_endeudamiento = tk.DoubleVar(value=self.lead["Endeudamiento"])
        self.sb_endeudamiento = tk.Spinbox(self.frame_endeudamiento, from_=0, to=1, increment=0.05, textvariable=self.sv_endeudamiento)
        self.sb_endeudamiento.pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)

        self.frame_años = tk.Frame(self)
        self.frame_años.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_años, text="Años máximo hipoteca:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX,pady=conf.PADY)
        self.sv_años = tk.IntVar(value=self.lead["Años máximo hipoteca"])
        # self.sb_años = tk.Spinbox(self.frame_años, from_=0, to=50, increment=5,textvariable=var_años, format="%.f")
        self.sb_años = tk.Spinbox(self.frame_años, from_=0, to=50, increment=5, textvariable=self.sv_años)
        self.sb_años.pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)

        self.frame_comentarios = tk.Frame(self)
        self.frame_comentarios.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)
        tk.Label(self.frame_comentarios, text="Comentarios:", width=VentanaDatosLead.LABEL_WITH, anchor="e").pack(side=tk.LEFT, padx=conf.PADX, pady=conf.PADY)
        self.tx_comentarios = tk.scrolledtext.ScrolledText(self.frame_comentarios, height=7, width=40, wrap=tk.WORD)
        self.tx_comentarios.insert(tk.INSERT, self.lead["Comentarios"])
        # self.tx_comentarios["state"] = tk.DISABLED
        self.tx_comentarios.pack(side=tk.LEFT, fill=tk.X, padx=conf.PADX, pady=conf.PADY)

    def create_buttons(self):
        self.frame_botones = tk.Frame(self)
        self.bt_cancelar = tk.Button(self.frame_botones, text="Cancelar", command=self.destroy)
        self.bt_cancelar.pack(side=tk.RIGHT, padx=conf.PADX, pady=conf.PADY)
        self.bt_aceptar = tk.Button(self.frame_botones, text="Aceptar", command=self.cm_aceptar)
        self.bt_aceptar.pack(side=tk.RIGHT, padx=conf.PADX, pady=conf.PADY)
        self.frame_botones.pack(fill=tk.X, padx=conf.PADX, pady=conf.PADY)

    def cm_aceptar(self):
        lead = {"Nombre":self.sv_nombre.get(), "Email":self.sv_email.get(), "Teléfono":self.sv_telefono.get(), "Fecha captación":self.cl_fecha.get_date(),
                    "Modo captación":self.cb_modo.get(),"Tipología":self.cb_tipologia.get(),"Promoción de interés":self.cb_promocion.get(),
                    "Maduración":self.cb_maduracion.get(),"Capacidad entrada":(self.cb_capacidad.get()),"Profesión":self.sv_profesion.get(),"Tipo de contrato":self.cb_contrato.get(),
                "Ingresos mensuales familia":int(self.sv_ingresos.get()),"Endeudamiento":float(self.sv_endeudamiento.get()),"Años máximo hipoteca":int(self.sv_años.get()),
                "Avalistas":self.cb_avalistas.get(),"Comentarios":self.tx_comentarios.get("1.0",tk.END)}

        if lead["Email"] == "":
            tk.messagebox.showerror("Error Email","El campo email no puede estar vacío")
            self.lift()
            return


        if self.alta:
            LeadsController.get_instance().añadir_lead(lead)

        else:
            LeadsController.get_instance().modificarLead(lead,self.email_anterior)

        self.destroy()

