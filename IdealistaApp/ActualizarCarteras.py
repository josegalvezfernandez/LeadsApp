# -*- coding: utf-8 -*-
"""
Created on Mon Mar 22 13:45:19 2021

@author: Usuario
"""
from GestorCarteras import rutaPrincipal,cargarCarteras
from datetime import date,datetime
import os #Utilizo este en lugar de pathlñib porque es más estandar. Además devuelve un tipo que no tendría que cambiar
import time
from PisosIdealista import CarteraDePisos

DIAS_ACTUALIZACION = 7
def main():
    carteras = cargarCarteras()#Carga los nombres no los archivos
    hoy = date.today()
    for nombreCartera,datosCartera in carteras.items():
        rutacsv = f"{rutaPrincipal}\\{nombreCartera}\\Cartera {nombreCartera}.csv"
        print(rutacsv)
        try:
            fecha_modificacion = getFechaModificacion(rutacsv)
            #print(f"{cartera} fecha modificacion {fecha_modificacion.strftime('%d-%m-%Y')}")
            dias = (hoy-fecha_modificacion).days
            #print(f"Han transcurrido {dias} dias")
            if DIAS_ACTUALIZACION <= 7:
                 coordenadasCartera = datosCartera.split(";")[0]#En la posicion 0 tenemos lat y long
                 distancia = int(datosCartera.split(";")[1])
                 cartera = CarteraDePisos(nombreCartera,coordenadasCartera,distancia)#Crear una cartera vacía primero
                 pisos = CarteraDePisos.cargarCsv(rutacsv)
                 cartera.añadirPisos(pisos)
                 cartera.actualizarPisos(to=[],ruta = rutacsv)
                 CarteraDePisos.guardarEnCsv(cartera.pisos, rutacsv)
                 print(f"Se actualizó la cartera {nombreCartera}")
        except FileNotFoundError:
            print(f"No se encontró el archivo de la cartera {nombreCartera}")
        
        
def getFechaModificacion(ruta):
    modts = os.path.getmtime(ruta)#da un timestamp. (i.e. fecha desde 1970)
    fecha = datetime.fromtimestamp(modts).date()
    return fecha
    
    
    
    
           

if __name__ == "__main__":#Ejecuta lo que esta dentro de main
   main()