import pandas as pd
import os
from LeadsApp.CONTROLLER.Email import EmailReader
from LeadsApp.MODEL.GestorEventos import EventoEstado
from datetime import datetime



class _LeadsController:#Clase privada no puede ser utilizada desde fuera

    RUTA_LEADS = r"LeadsApp\Datos\Leads.csv"
    COLUMNAS_LEADS = ["Nombre", "Email", "Teléfono", "Fecha captación",
                      "Modo captación", "Tipología", "Promoción de interés",
                      "Maduración", "Capacidad entrada", "Profesión", "Tipo de contrato", "Ingresos mensuales familia",
                      "Endeudamiento", "Años máximo hipoteca", "Avalistas", "Comentarios"]
    RUTA_MENSAJES = r"LeadsApp\Datos\Mensajes.csv"
    COLUMNAS_MENSAJES = ["Email", "Fecha", "Asunto", "Mensaje", "Lista adjuntos", "Recibido", "Enviado"]
    RUTA_EVENTOS = r"LeadsApp\Datos\Eventos.csv"
    COLUMNAS_EVENTOS = ["Email", "Tipo", "Fecha", "Lugar", "Estado", "Comentarios"]
    ACTUALIZAR_DESDE_EMAIL = False

    def __init__(self):
        self.observadores_eventos = []
        self.observadores_mensajes = []
        self.observadores_leads = []# La Ventana Principal necesita ser avisada
        self.cargar()

    def suscribir_eventos(self,obsevador):
        self.observadores_eventos.append(obsevador)

    def suscribir_mensajes(self,observador):
        self.observadores_mensajes.append(observador)

    def suscribir_leads(self,observador):
        self.observadores_leads.append(observador)


    def __avisar_observadores_mensajes(self):
        for observador in self.observadores_mensajes:
            observador.actualizar()

    def __avisar_observadores_eventos(self):#Métodos que empiezan por __ son privados
        for observador in self.observadores_eventos:
            observador.actualizar()

    def __avisar_observadores_leads(self):
        for observador in self.observadores_leads:
            observador.actualizar()


    def cargar(self):
        # print("Estamos en comando abrir")
        def abrir_tabla(ruta, columnas):
            if os.path.isfile(ruta):
                return pd.read_csv(ruta)
            else:
                print(os.getcwd())
                return pd.DataFrame(columns=columnas)

        self.df_leads = abrir_tabla(_LeadsController.RUTA_LEADS, _LeadsController.COLUMNAS_LEADS)
        self.df_leads["Fecha captación"] = pd.to_datetime(self.df_leads["Fecha captación"])
        self.df_leads['Fecha captación'] = [time.date() for time in self.df_leads['Fecha captación']]
        # self.df['Teléfono']= self.df['Teléfono'].map(str)
        self.df_leads = self.df_leads.fillna("")

        self.df_mensajes = abrir_tabla(_LeadsController.RUTA_MENSAJES, _LeadsController.COLUMNAS_MENSAJES)
        self.df_mensajes["Fecha"] = pd.to_datetime(self.df_mensajes["Fecha"])
        self.df_eventos = abrir_tabla(_LeadsController.RUTA_EVENTOS, _LeadsController.COLUMNAS_EVENTOS)
        self.df_eventos["Fecha"] = pd.to_datetime(self.df_eventos["Fecha"])
        if _LeadsController.ACTUALIZAR_DESDE_EMAIL:# TODO(developer) ahora mismo esta en False porque no conectamos con email
            self.actualizarLeadsDesdeEmail()  # ARREGLAR DESCARGAS CON CARLOS

        self.__avisar_observadores_mensajes()
        self.__avisar_observadores_eventos()
        self.__avisar_observadores_leads()

    def guardar(self):
        self.df_leads.to_csv(_LeadsController.RUTA_LEADS, index=False)
        self.df_mensajes.to_csv(_LeadsController.RUTA_MENSAJES, index=False)
        self.df_eventos.to_csv(_LeadsController.RUTA_EVENTOS, index=False)


    def actualizarLeadsDesdeEmail(self):
        def añadirLeads(self,leads):
            for lead in leads:
                mensaje = {"Email":lead["Email"],"Fecha":lead["Fecha captación"],"Asunto":"Primer contacto, mediante formulario","Mensaje":lead["Mensaje"],"Lista adjuntos":[] ,"Recibido":True,"Enviado":False}
                self.df_mensajes = self.df_mensajes.append(mensaje, ignore_index=True)
                del lead["Mensaje"]
                if lead["Email"] not in self.df["Email"].tolist():# Si el lead no existe:
                    self.df = self.df.append(lead,ignore_index=True)#Porque no tenemos indice porque es un diccionario sin indice

        lectoremail = EmailReader("info@grupoedetica.com", "QhnbFrQ34vXP", "mail.grupoedetica.com")
        leadsFormulario = lectoremail.obtenerClientesFormulario()
        # leadsIdealista = lectoremail.obtenerClientesIdealista()
        añadirLeads(leadsFormulario)
        # self.añadirLeads(leadsIdealista)
        mensajes_lead = lectoremail.obtenerMensajesDeCliente(
            self.df_leads["Email"].to_list())  # Convertimos una serie de un panda en una lista para poder recorrerlo
        self.df_mensajes = self.df_mensajes.append(mensajes_lead, ignore_index=True)

        self.__avisar_observadores_leads()

    def get_leads(self):
        return self.df_leads

    def get_leads_columns(self):
        return self.df_leads.columns.values

    def get_mensajes(self):
        return self.df_mensajes

    def get_mensajes_lead(self,email):
        return self.df_mensajes.loc[self.df_mensajes["Email"] == email]

    def get_eventos(self):
        return self.df_eventos

    def get_eventos_lead(self,email):
        return self.df_eventos.loc[self.df_eventos["Email"] == email]

    def get_eventos_dia(self,dia):

        dia_inicio = datetime.fromordinal(dia.toordinal())
        dia_inicio = dia_inicio.replace(hour=0,minute=0)
        dia_fin = datetime.fromordinal(dia.toordinal())
        dia_fin = dia_fin.replace(hour=23,minute=59)

        return self.df_eventos.loc[(self.df_eventos["Fecha"] >= dia_inicio) & (self.df_eventos["Fecha"] <= dia_fin)]

    def añadir_lead(self,lead):
        self.df_leads = self.df_leads.append(lead, ignore_index=True)
        self.df_leads.to_csv(_LeadsController.RUTA_LEADS, index=False)
        self.__avisar_observadores_leads()

    def borrar_lead(self,email):
        indice_borrar = self.df_leads.loc[self.df_leads["Email"] == email].index
        self.df_leads = self.df_leads.drop(indice_borrar,axis=0)  # Borrar filas a través del indice con axis = 0, aunque los podíamos haber evitado
        self.df_leads.to_csv(_LeadsController.RUTA_LEADS, index=False)
        self.__avisar_observadores_leads()

    def modificarLead(self, lead, email_borrar):
        indice_borrar =self.df_leads.loc[self.df_leads["Email"] == email_borrar].index
        self.df_leads = self.df_leads.drop(indice_borrar, axis=0)  # Borrar filas a través del indice con axis = 0, aunque los podíamos haber evitado
        self.df_leads = self.df_leads.append(lead, ignore_index=True)
        self.df_leads = self.df_leads.sort_values(by="Fecha captación")
        self.df_leads.to_csv(_LeadsController.RUTA_LEADS, index=False)
        self.__avisar_observadores_leads()

    def añadirEvento(self, evento):
        self.df_eventos = self.df_eventos.append(evento, ignore_index=True)
        self.df_eventos.to_csv(_LeadsController.RUTA_EVENTOS, index=False)
        self.__avisar_observadores_eventos()

    def borrarEvento(self,indice):
        self.df_eventos = self.df_eventos.drop(indice)
        self.df_eventos.to_csv(_LeadsController.RUTA_EVENTOS, index=False)
        self.__avisar_observadores_eventos()

    def modificarEvento(self, evento, evento_anterior):
        self.df_eventos = self.df_eventos.drop(evento_anterior["index"])
        self.df_eventos = self.df_eventos.append(evento, ignore_index=True)
        self.df_eventos.to_csv(_LeadsController.RUTA_EVENTOS, index=False)
        self.__avisar_observadores_eventos()

    def realizarEvento(self,indice):
        self.df_eventos.at[indice, "Estado"] = str(EventoEstado.REALIZADO)
        """at es para modificar 
        row by index"""
        self.df_eventos.to_csv(_LeadsController.RUTA_EVENTOS, index=False)
        self.__avisar_observadores_eventos()

    def añadirMensaje(self, mensaje, indice_evento=-1):
        self.df_mensajes = self.df_mensajes.append(mensaje, ignore_index=True)
        self.df_mensajes.to_csv(_LeadsController.RUTA_MENSAJES, index=False)
        self.__avisar_observadores_mensajes()
        if indice_evento != -1:
            self.realizarEvento(indice_evento)

    def get_lead_by_email(self,email):
        return self.df_leads.loc[self.df_leads["Email"]==email].iloc[0].to_dict()

class LeadsController:
    _instance = None

    @staticmethod
    def get_instance():#Como es estático no recibe self QUEREMOS SABER CUANTAS INSTANCIAS SE HAN CREADO
        # NO HACE FALTA SELF
        if LeadsController._instance == None:#Si no existe la instancia única
            LeadsController._instance = _LeadsController()#La creamos por primera y única vez
        return LeadsController._instance






