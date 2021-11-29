# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 12:42:49 2021

@author: Usuario
"""
from enum import Enum

def getDefaultLead():
    return {"Nombre":"","Email":"","Teléfono":"","Tipología":str(LeadTipologia.getdefault()),"Maduración":str(LeadMaduracion.getdefault()),"Fecha captación":"",
                         "Modo captación":str(LeadCaptacion.getdefault()),
                         "Capacidad entrada":str(LeadSiNoNSNC.getdefault()),"Profesión":"","Tipo de contrato":str(LeadTipoContrato.getdefault()),"Ingresos mensuales familia":0,"Endeudamiento":0,
                         "Años máximo hipoteca":0,"Avalistas":str(LeadSiNoNSNC.getdefault()),"Comentarios":"","Promoción de interés":str(LeadPromocion.getdefault())}
class LeadTipologia(Enum):

    BAJO_1DORMITORIO = 0
    BAJO_2DORMITORIO = 1
    BAJO_3DORMITORIO = 2
    BAJO_4DORMITORIO = 3
    VIVIENDA_TIPO_1DORMITORIO = 4
    VIVIENDA_TIPO_2DORMITORIO = 5
    VIVIENDA_TIPO_3DORMITORIO = 6
    VIVIENDA_TIPO_4DORMITORIO = 7
    VIVIENDA_ATICO_1DORMITORIO = 8
    VIVIENDA_ATICO_2DORMITORIO = 9
    VIVIENDA_ATICO_3DORMITORIO = 10
    VIVIENDA_ATICO_4DORMITORIO = 11
    NINGUNA = 12


    def __str__(self): #Convierte de LeadTipologia a un str
        textos = ["Bajo 1 Dormitorio", "Bajo 2 Dormitorios", "Bajo 3 Dormitorios", "Bajo 4 Dormitorios",
            "Vivienda Tipo 1 Dormitorio", "Vivienda Tipo 2 Dormitorios", "Vivienda Tipo 3 Dormitorios"
            , "Vivienda Tipo 4 Dormitorios", "Vivienda Atico 1 Dormitorio", "Vivienda Atico 2 Dormitorios"
            , "Vivienda Atico 3 Dormitorios", "Vivienda Atico 4 Dormitorios",
            "Ninguna"]  # Textos que queremos aparezca al usuario
        return textos[self.value]

    def parse(texto):  # Convierte/Parsear a un Objeto (LeadTipología)
        textos = ["Bajo 1 Dormitorio","Bajo 2 Dormitorios","Bajo 3 Dormitorios","Bajo 4 Dormitorios",
                  "Vivienda Tipo 1 Dormitorio", "Vivienda Tipo 2 Dormitorios","Vivienda Tipo 3 Dormitorios"
                  ,"Vivienda Tipo 4 Dormitorios","Vivienda Atico 1 Dormitorio","Vivienda Atico 2 Dormitorios"
            ,"Vivienda Atico 3 Dormitorios","Vivienda Atico 4 Dormitorios",
                  "Ninguna"]
        index = textos.index(texto)
        return LeadTipologia(index)

    @classmethod  # Recibimos la clase como argumento que es más cómodo que acceder a los atributos de otra forma
    def values(cls):
        # l = [str(v).replace("LeadTipologia.", "").replace("_", " ") for v in cls]
        return ["Bajo 1 Dormitorio","Bajo 2 Dormitorios","Bajo 3 Dormitorios","Bajo 4 Dormitorios",
                  "Vivienda Tipo 1 Dormitorio", "Vivienda Tipo 2 Dormitorios","Vivienda Tipo 3 Dormitorios"
                  ,"Vivienda Tipo 4 Dormitorios","Vivienda Atico 1 Dormitorio","Vivienda Atico 2 Dormitorios"
            ,"Vivienda Atico 3 Dormitorios","Vivienda Atico 4 Dormitorios",
                  "Ninguna"]


    @classmethod
    def getdefault(cls):
        return LeadTipologia.NINGUNA


class LeadMaduracion(Enum):
    SIN_CLASIFICAR = 0
    SIN_ZONA = 1
    SIN_TIPO = 2
    VIVO = 3
    VIVO_MAS = 4
    VENDIDO = 5

    def __str__(self): #Convierte de LeadMaduracion a un str
        textos = ["Sin clasificar","Sin zona","Sin tipo","Vivo","Vivo mas","Vendido"]  # Textos que queremos aparezca al usuario
        return textos[self.value]

    def parse(texto):  # Convierte/Parsear a un Objeto (LeadMaduracion)
        textos = ["Sin clasificar","Sin zona","Sin tipo","Vivo","Vivo mas","Vendido"]
        index = textos.index(texto)
        return LeadTipologia(index)

    def getcolor(self):
        colores = ["white","yellow","grey","orange","brown","green"]
        return colores[self.value]

    def getdescripcion(self):
        descripciones = ["No definido","No gusta la zona","No tenemos producto","Contactado una vez",
                         "contactado más de una vez","Vendido"]
        return descripciones[self.value]

    @classmethod # Recibimos la clase como argumento que es más cómodo que acceder a los atributos de otra forma
    def values(cls):
        # l = [str(v).replace("LeadMaduracion.","").replace("_"," ") for v in cls]
        return ["Sin clasificar","Sin zona","Sin tipo","Vivo","Vivo mas","Vendido"]

    @classmethod
    def getdefault(cls):
        return LeadMaduracion.SIN_CLASIFICAR

    @classmethod
    def getnumberbyname(cls,name):
        return LeadMaduracion.values().index(name)



    
class LeadTipoContrato(Enum):
    
    FIJO = 0
    TEMPORAL = 1
    FUNCIONARIO = 2
    AUTONOMO = 3
    EMPRESARIO = 4
    OTROS = 5
    SIN_DEFINIR = 6


    def __str__(self): #Convierte de LeadCaptacion a un str
        textos = ["Fijo","Temporal","Funcionario","Autónomo","Empresario","Otros","Sin definir"]  # Textos que queremos aparezca al usuario
        return textos[self.value]

    def parse(texto):  # Convierte/Parsear a un Objeto (LeadTipología)
        textos = ["Fijo","Temporal","Funcionario","Autónomo","Empresario","Otros","Sin definir"]
        index = textos.index(texto)
        return LeadTipologia(index)


    @classmethod  # Recibimos la clase como argumento que es más cómodo que acceder a los atributos de otra forma
    def values(cls):
        # l = [str(v).replace("LeadTipoContrato.", "").replace("_", " ") for v in cls]
        return  ["Fijo","Temporal","Funcionario","Autónomo","Empresario","Otros","Sin definir"]

    @classmethod
    def getdefault(cls):
        return LeadTipoContrato.SIN_DEFINIR

class LeadCaptacion(Enum):

    FACEBOOK_WEB = 0
    IDEALISTA = 1
    TELEFONO = 2
    OTROS = 3
    SIN_CLASIFICAR = 4


    def __str__(self): #Convierte de LeadCaptacion a un str
        textos = ["Facebook/web", "Idealista", "Teléfono", "Otros",
                  "Sin clasificar"]  # Textos que queremos aparezca al usuario
        return textos[self.value]

    def parse(texto): # Convierte/Parsear a un Objeto (LeadCaptacion)
        textos = ["Facebook/web", "Idealista", "Teléfono", "Otros", "Sin clasificar"]#Textos que queremos aparezca al usuario
        index = textos.index(texto)
        return LeadCaptacion(index)

    # @classmethod  # Recibimos la clase como argumento que es más cómodo que acceder a los atributos de otra forma
    # def values(cls):
    #     return LeadCaptacion.TEXTOS


    @classmethod  # Recibimos la clase como argumento que es más cómodo que acceder a los atributos de otra forma
    def values(cls):
        # l = [str(v).replace("LeadCaptacion.", "").replace("_", " ") for v in cls]
        return ["Facebook/web", "Idealista", "Teléfono", "Otros", "Sin clasificar"]


    @classmethod
    def getdefault(cls):
        return LeadCaptacion.SIN_CLASIFICAR


class LeadPromocion(Enum):

    IFEBA = 0
    RESIDENCIAL_CUARTON_CUARTA_FASE= 1
    RESIDENCIAL_DOÑA_BLANCA = 2
    NINGUNA = 3


    # def __str__(self): #Convierte de LeadCaptacion a un str
        # return LeadCaptacion.TEXTOS[int(self)]
    def __str__(self): #Convierte de LeadCaptacion a un str
        textos = ["Solar viejo (IFEBA)", "Residencial Parque Universidad 4", "Residencial Doña Blanca","Ninguna"]  # Textos que queremos aparezca al usuario
        return textos[self.value]

    def parse(texto): # Convierte/Parsear a un Objeto (LeadPromocion)
        textos = ["Solar viejo (IFEBA)", "Residencial Parque Universidad 4", "Residencial Doña Blanca","Ninguna"]
        index = textos.index(texto)
        return LeadPromocion(index)#tiene los metodos (Enum) que son el value o el name

    # @classmethod  # Recibimos la clase como argumento que es más cómodo que acceder a los atributos de otra forma
    # def values(cls):
    #     return LeadCaptacion.TEXTOS


    @classmethod  # Recibimos la clase como argumento que es más cómodo que acceder a los atributos de otra forma
    def values(cls):
        # l = [str(v).replace("LeadPromocion.", "").replace("_", " ") for v in cls]
        return ["Solar viejo (IFEBA)", "Residencial Parque Universidad 4", "Residencial Doña Blanca","Ninguna"]

    @classmethod
    def getdefault(cls):
        return LeadPromocion.NINGUNA


class LeadSiNoNSNC(Enum):
    NO = 0
    SI = 1
    NSNC = 2

    def __str__(self):  # Convierte de LeadTipologia a un str
        textos = LeadSiNoNSNC.values()  # Textos que queremos aparezca al usuario
        return textos[self.value]

    def parse(texto):  # Convierte/Parsear a un Objeto (LeadSiNoNSNC)
        textos = LeadSiNoNSNC.values()
        index = textos.index(texto)
        return LeadSiNoNSNC(index)

    @classmethod  # Recibimos la clase como argumento que es más cómodo que acceder a los atributos de otra forma
    def values(cls):
        # l = [str(v).replace("LeadTipologia.", "").replace("_", " ") for v in cls]
        return ["No","Sí","No Preguntado"]

    @classmethod
    def getdefault(cls):
        return LeadSiNoNSNC.NSNC

    def getcolor(self):
        colores = ["red","green","white"]
        return colores[self.value]



