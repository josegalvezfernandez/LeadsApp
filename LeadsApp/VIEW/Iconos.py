from MODEL.GestorEventos import EventoTipo
import tkinter as tk
from PIL import Image, ImageTk

ACCION_ENVIAR_EMAIL = "Enviar Email"
ACCION_MARCAR_REALIZADO = "Marcar Realizado"
ACCION_BORRAR = "Borrar"
ACCION_EDITAR = "Editar"
ACCION_AÑADIR = "Añadir"
ACCION_FILTRAR = "Filtrar"
ACCION_VER_EVENTOS = "Ver Eventos"

ICONOS = {ACCION_ENVIAR_EMAIL:r"LeadsApp\Iconos\ICON_SendEmail.png",
                 ACCION_MARCAR_REALIZADO: r"LeadsApp\Iconos\ICON_Check.png",
                 ACCION_BORRAR: r"LeadsApp\Iconos\ICON_Delete.png",
                 ACCION_EDITAR: r"LeadsApp\Iconos\ICON_Edit.png",
                 ACCION_AÑADIR: r"LeadsApp\Iconos\ICON_Add.png",
                 ACCION_FILTRAR: r"LeadsApp\Iconos\ICON_Filter.png",
                 ACCION_VER_EVENTOS: r"LeadsApp\Iconos\ICON_Event.png"}

ICONOS_TIPO_EVENTO = {str(EventoTipo.LLAMADA):r"LeadsApp\Iconos\ICON_Phone.png",
                                   str(EventoTipo.REUNION):r"LeadsApp\Iconos\ICON_Meeting.png",
                                   str(EventoTipo.SIN_DEFINIR):r"LeadsApp\Iconos\ICON_Event.png",
                                   str(EventoTipo.EMAIL):r"LeadsApp\Iconos\ICON_Email.png"}


def get_photo_image_evento(tipo_evento, width = 25,height = 25):
    path = ICONOS_TIPO_EVENTO[str(tipo_evento)]
    return get_photo_image(path,width,height)

def get_photo_image_action(tipo_accion, width = 25,height = 25):
    path = ICONOS[tipo_accion]
    return get_photo_image(path,width,height)

def get_photo_image(path, width = 25,height = 25):
    image = Image.open(path)
    resize_image = image.resize((width, height))
    return ImageTk.PhotoImage(resize_image)
