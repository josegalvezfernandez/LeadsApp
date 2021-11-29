from enum import Enum
from datetime import date


def getDefaultEvento(email):
    return {"Email":email,"Tipo":str(EventoTipo.getdefault()),"Fecha":date.today(),"Lugar":"","Estado":str(EventoEstado.getdefault()),"Comentarios":""}
 #"Tipo" lo pasamos a un metodo proprio __str__ porque es lo que maneja la ventana

class EventoTipo(Enum):

    LLAMADA = 0
    EMAIL = 1
    REUNION = 2
    SIN_DEFINIR = 3

    def __str__(self):  # Convierte de EventoTipologia a un str
        textos = EventoTipo.values()  # Textos que queremos aparezca al usuario
        return textos[self.value]

    def parse(texto):  # Convierte/Parsear a un Objeto (EventoTipo)
        textos = EventoTipo.values()
        index = textos.index(texto)
        return EventoTipo(index)

    @classmethod  # Recibimos la clase como argumento que es más cómodo que acceder a los atributos de otra forma
    def values(cls):
        # l = [str(v).replace("LeadTipologia.", "").replace("_", " ") for v in cls]
        return ["Llamada", "Email", "Reunión","Sin definir"]

    @classmethod
    def getdefault(cls):
        return EventoTipo.SIN_DEFINIR

class EventoEstado(Enum):

    PENDIENTE = 0
    RETRASADO = 1
    REALIZADO = 2

    def __str__(self):  # Convierte de EventoEstado a un str
        textos = EventoEstado.values()  # Textos que queremos aparezca al usuario
        return textos[self.value]

    def parse(texto):  # Convierte/Parsear a un Objeto (EventoTipo)
        textos = EventoEstado.values()
        index = textos.index(texto)
        return EventoEstado(index)

    @classmethod  # Recibimos la clase como argumento que es más cómodo que acceder a los atributos de otra forma
    def values(cls):
        # l = [str(v).replace("LeadTipologia.", "").replace("_", " ") for v in cls]
        return ["Pendiente", "Retrasado", "Realizado"]

    @classmethod
    def getdefault(cls):
        return EventoEstado.PENDIENTE