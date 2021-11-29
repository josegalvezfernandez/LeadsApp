# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 16:51:47 2020

@author: Usuario
"""
import datetime as dt
from distutils.util import strtobool
from os import system,path,remove


class bcolors:
    HEADER = '\033[95m'
    OKPINK = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WARNING = '\033[33m'
    
def elegirOpcionMenu(titulo,menu):#Menu va a ser lista de elementos (i.e. opciones)
    system("cls")
    print(f"{bcolors.HEADER}\n{titulo}\n{bcolors.ENDC}")
    n=1
    for opcion in menu:
        print("\t",n,". ",opcion,sep="")#Convierte todo a str y el sep dice el espacio entre 2 elementos
        #print("\t"+str(n)+". "+opcion)#Todos estos elementos los tengo que cambiar a str
        #print("\t%d. %s"%(n,opcion))#Más corta y más fácil configurar
        n += 1
    correcto = False
    while not correcto:
        eleccion = input(f"{bcolors.OKCYAN}\nElige una opción del menú:{bcolors.ENDC} ")
        try:#Intenta hacer algo y si sale un error haces algo en el except
            eleccion = int(eleccion)
            if eleccion >= 1 and eleccion < n:
                correcto = True
            else:
                print(f"{bcolors.WARNING}Error, debes introducir un número entre 1 y %d{bcolors.ENDC}"%(n-1))
        except ValueError:#Si no poner el ValueError se te cuelan todos los errores 
            print(f"{bcolors.WARNING}Error, debes introducir un número{bcolors.ENDC}")
            
    return eleccion

def esperarPulsacion():
    input(f"{bcolors.OKGREEN}\nPulsa enter para continuar:{bcolors.ENDC}")

def leerBooleano(mensaje):
    
    leido = False
    while not leido:
        respuesta = input(f"{bcolors.OKCYAN}\n{mensaje}: {bcolors.ENDC}")
        if len(respuesta) == 0:
            leido = True
            salida = None
        else:
            try:
                salida = strtobool(respuesta)
                leido = True
            except ValueError:
                print(f"{bcolors.WARNING}Valor no válido, introduce True, False o Enter para continuar{bcolors.ENDC}")
    return salida

def leerOpcion(listaOpciones,campo):
    opcion = elegirOpcionMenu(f"{bcolors.OKCYAN}\nSelecciona {campo}: ",listaOpciones)
    if opcion == len(listaOpciones):
        return None
    return listaOpciones[opcion-1]

def leerNombreFichero(mensaje,extension,ruta):
    correcto = False
    while not correcto:
         respuesta = input(f"{bcolors.OKCYAN}\n{mensaje}: {bcolors.ENDC}")    
         if not respuesta.endswith(extension):
             respuesta = respuesta + extension
         fichero = f"{ruta}\\{respuesta}"#Para meter espacios en blanco
         if path.isfile(fichero):
             borrar = preguntarSiNo("El fichero ya existe ¿Quieres eliminarlo antes de continuar?")
             if borrar:
                 try:
                     remove(fichero)
                     correcto = True
                 except PermissionError:
                     print(f"{bcolors.FAIL}Error, el fichero no se pudo borrar porque esta abierto{bcolors.ENDC}")

         else:
             correcto = True
    return fichero
                 
         

def leerEntero(mensaje,minimo=0,maximo=float("inf")):#Max representa el infinito por defecto y el minimo no puede ser negativo
    
    correcto = False
    while not correcto:
        respuesta = input(f"{bcolors.OKCYAN}\n{mensaje}: {bcolors.ENDC}")    
        try:
            numero = int(respuesta)
            if numero < minimo:
                print(f"{bcolors.WARNING}Error el minimo es {minimo}.{bcolors.ENDC}")
            elif numero > maximo:
                print(f"{bcolors.WARNING}Error el maximo es {maximo}.{bcolors.ENDC}")
            else:
                correcto = True
        except ValueError:
            print(f"{bcolors.WARNING}Error introduce sólo dígitos numéricos{bcolors.ENDC}")
        
    return numero        
        




def preguntarSiNo(mensaje):
    respuesta = input(f"{bcolors.OKCYAN}\n{mensaje} ('s' para si, 'n' para no):{bcolors.ENDC}").lower()#El input sólo recibe un parámetro tipo str. por eso
    # ponemos el + y no una coma
    while respuesta != "s" and respuesta != "n":
        respuesta = input(f"{bcolors.WARNING}Error, introduce 's' para sí, 'n' para no:{bcolors.ENDC}").lower()
    return respuesta == "s"#Este return devuelve True or False

def leerListaEmails():
    listaEmails = []
    if preguntarSiNo(f"{bcolors.OKCYAN}\nDeseas enviar un email con los datos de la operación{bcolors.ENDC}"):
        continuar = "s"
        while continuar == "s":
            email = input(f"{bcolors.OKCYAN}Introduzca un email: {bcolors.ENDC}")
            listaEmails.append(email)
            continuar = preguntarSiNo(f"{bcolors.OKCYAN}¿Quiéres introducir más emails? {bcolors.ENDC}")
    return listaEmails

def leerFecha(mensaje):
    leido = False
    while not leido:
        print(f"{bcolors.OKCYAN}\nPulsa Enter para usar la fecha de hoy {bcolors.ENDC}")
        fechastr = input(mensaje + " (DD/MM/AAAA): ")
        if len(fechastr) == 0:# Esto quiere decir que fechastr es como pulsar enter
            fecha = dt.datetime.now().date()
            leido = True
        else:
            try:
                fecha = dt.datetime.strptime(fechastr,"%d/%m/%Y").date()#date no tiene strptime por eso ponemos al final date()
                leido = True#Si no sabemos el Error podemos ejecutar la función e introducir entrada errónea para saber
                #que excepción nos salta
            except ValueError:
                print( f"{bcolors.WARNING}Error en el formato de la fecha {bcolors.ENDC}")
            
        
    return fecha
        
    