from functools import partial

from LeadsApp.MODEL.GestorEventos import EventoEstado, EventoTipo
from LeadsApp.VIEW.Iconos import get_photo_image_action, ACCION_EDITAR, ACCION_BORRAR, ACCION_ENVIAR_EMAIL, \
    ACCION_MARCAR_REALIZADO
import tkinter as tk
from LeadsApp.VIEW import ConfiguracionVentanas as conf

class TablaEventos(tk.Frame):
    """
    Creates a grid of labels that have their cells populated by content.
    """
    def __init__(self, master, content, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.content = content
        if len(content) == 0:
            self.content_size = (0,0)
        else:
            self.content_size = (len(content), len(content[0])) # Tupla len(content) son el número de filas,
        # len(content[0]) son número de columnas
        self.image_editar = get_photo_image_action(ACCION_EDITAR)
        self.image_borrar = get_photo_image_action(ACCION_BORRAR)
        self.image_enviar_email = get_photo_image_action(ACCION_ENVIAR_EMAIL)
        self.image_marcar_realizado = get_photo_image_action(ACCION_MARCAR_REALIZADO)
        self.master = master
        self._create_labels()# El guión bajo es método interno nuestro
        self._display_labels()


    def _create_labels(self):
        def __put_content_in_label(row, column):
            content = self.content[row][column]
            content_type = type(content).__name__
            if content_type in ('str', 'int'):
                self.labels[row][column]['text'] = content
            elif content_type == "tuple":#Si ponemos un else en lugar de elif, no haría nada cuando no sea
                # ni str, int,PhotoImage.Aquí no daría error
                self.labels[row][column]['image'] = content[0]


        self.labels = list()
        for i in range(self.content_size[0]):# Recorre las filas self.content_size[0]
            self.labels.append(list())
            for j in range(self.content_size[1]):# Recorre las columnas self.content_size[1]
                if i == 0:# Si es la primera fila
                    self.labels[i].append(tk.Label(self,font = "Helvetica 12 bold"))
                else:
                    if j == 2:
                        if self.content[i][j] == "Pendiente":
                            color = "#880"
                        elif self.content[i][j] == "Retrasado":
                            color = "#f00"
                        else:
                            color = "#6a6"
                        self.labels[i].append(tk.Label(self,fg = color))
                    else:
                        self.labels[i].append(tk.Label(self))

                __put_content_in_label(i, j)


        botones_editar = [None]*(self.content_size[0]-1) # Lista de Nones en lugar de lista vacía, porque
        #en None asigan un índice a cada posición de la Lista. Si la creo vacía y quiero acceder a la
        #posición i ,e daría error. También podía haber hecho lista vacía

        botones_realizar = [None]*(self.content_size[0]-1)
        botones_borrar = [None] * (self.content_size[0] - 1)

        for i in range(self.content_size[0]-1):#

            botones_editar[i] = tk.Button(self,image = self.image_editar, text = "Editar", command = partial(self.cm_editar_evento,i))
            #Pasamos i para que sepa que fila tiene que cm_editar_evento. Anteriormente pasamos un
            #lambda para meter parámetros pero no funciona.
            #Example:
            botones_editar[i].grid(row=i + 1,column =  1 )

            if self.content[i +1][0][1]  == str(EventoTipo.EMAIL):
                botones_realizar[i] = tk.Button(self,image =self.image_enviar_email, text = "Enviar", command = partial(self.cm_enviar_email,i))
            else:
                botones_realizar[i] = tk.Button(self, image=self.image_marcar_realizado, text="Marcar Realizado",
                                                command=partial(self.cm_realizar_evento, i))
            botones_realizar[i].grid(row=i + 1,column =  2 )
            if self.content[i+1][2] == str(EventoEstado.REALIZADO):
                botones_realizar[i]["state"] = tk.DISABLED


            botones_borrar[i] = tk.Button(self, image= self.image_borrar, text="Borrar",
                                          command=partial(self.cm_borrar_evento, i))
            botones_borrar[i].grid(row=i + 1, column= 3)




    def _display_labels(self):
        for i in range(self.content_size[0]):
            for j in range(self.content_size[1]):
                self.labels[i][j].grid(row=i, column=j + 4, padx = conf.PADX)

    def update_content(self,content):

        for i in range(self.content_size[0]):
            for j in range(self.content_size[1]):
                self.labels[i][j].destroy()

        self.content = content
        self.content_size = (len(content), len(content[0]))
        self._create_labels()
        self._display_labels()

    def cm_editar_evento(self,indice):
        self.master.cm_editar_evento(indice)

    def cm_enviar_email(self, indice):
        self.master.cm_enviar_email(indice)

    def cm_realizar_evento(self,indice):
        self.master.cm_realizar_evento(indice)

    def cm_borrar_evento(self,indice):
        self.master.cm_borrar_evento(indice)

