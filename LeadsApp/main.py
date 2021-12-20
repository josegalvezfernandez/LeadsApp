# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


import tkinter as tk
from VIEW.VentanaPrincipal import VentanaPrincipal


def main():
    root = tk.Tk()  # Iniciamos el sistema de ventanas y creamos la ventana principal
    app = VentanaPrincipal(master=root)

    # ruta = "DatosClientes.xlsx" #De la línea 405 a la 409 me salto ventanas para rellenar y hago pruebas más rápidas
    # datosClientes = leerExcel(ruta)
    # email_sender = EmailSender("Pepe","Pepe",server = "cpanel.grupoedetica.com")
    # app = VentanaNuevoEmail(master=root,email_sender=email_sender,df=datosClientes.iloc[:2,:])
    # launch the app
    try:
        app.mainloop()
    except Exception as e:  # Captura cualquier tipo de excepcion y cualquier error cierro las imágenes
        print(e)
        app.cm_salir()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
