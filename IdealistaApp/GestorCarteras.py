#pip  -*- coding: utf-8 -*-1

"""
Created on Wed Jul 29 13:45:36 2020

@author: Usuario
"""
from PisosIdealista import CarteraDePisos
import csv
from geopy.geocoders import Nominatim
from os import path,mkdir
from statistics import mean
from IOUtils import elegirOpcionMenu,leerBooleano,leerOpcion,preguntarSiNo,leerListaEmails,leerFecha,leerEntero,esperarPulsacion,leerNombreFichero
from IOUtils import bcolors

rutaPrincipal = path.expanduser("~\\Documents\\Mis Carteras")# Sacamos  'C:\\Users\\Usuario\\Mis Carteras'
menuInicial = ["Abrir Cartera","Crear Nueva Cartera","Salir"]
menuCartera = ["Actualizar Cartera","Mostrar Pisos","Mostrar Estadísticas","Buscar Pisos","Cerrar Cartera"]
menuGeneralEstadisticas = ["Estadísticas por distrito","Estadísticas totales","Volver"] 
menuMostrar = ["Mostrar Todos","Mostrar por Distritos","Mostrar por ExternalReference","Mostrar Obra Nueva","Volver"]

def direccionACoordendas(direccion):
    localizador = Nominatim(user_agent="http")#Usamos por la web2
    print(localizador)
    localizacion = localizador.geocode(direccion)    
    return localizacion

def cargarCarteras():
    carteras = {}
    try:
        with open(f"{rutaPrincipal}\\carteras.txt","r") as fichero:
            for linea in fichero.readlines():
                datos = linea.split("#")#La linea es nombre de cartera#latitud,longitud,distancia (Ver en Pisos.py viene así)
                if len(datos) == 2:#Esta condición es por las lineas vacías
                    carteras[datos[0]]=datos[1]
    except FileNotFoundError:
        print("El sistema no encontró ninguna cartera, crea una cartera para empezar")
        esperarPulsacion()
    return carteras

def guardarCarteras(carteras):
    with open(f"{rutaPrincipal}\\carteras.txt","w") as fichero:
        for nombre,datos in carteras.items():
            fichero.write("%s#%s\n"%(nombre,datos))

def generarEstadisticas(campo,listaPisos):
    listaValores = [piso.__dict__[campo] for piso in listaPisos ]#Queremos acceder en piso al campo que
    #me indica el parámetro campo. Hemos convertido un objeto/clase en un dict.
    #La única manera es convertir el piso en un diccionario cuyas claves
    #son los nombres de atributo y los valores, son los valores del atributo, y usar el parámetro campo
    #como clave de dicho diccionario
    maximo = max(listaValores)
    minimo = min(listaValores)
    media = mean(listaValores)
    
    return minimo, media, maximo
    

def mostrarEstadisticas(listaPisos,listaCampos,nombreCartera):
    print(f"Total {len(listaPisos)} pisos")
    dictEstadisticas = {}
    for campo in listaCampos:    
        (minimo,media,maximo) = generarEstadisticas(campo,listaPisos)
        dictEstadisticas[campo]=(maximo,minimo,media)
        print(f"{campo} : max = {maximo} min = {minimo} media = {media:.2f}")
    if preguntarSiNo("Quieres guardar las estadísticas en un fichero? "):
        ruta = leerNombreFichero("Introduce el nombre del fichero",".csv",f"{rutaPrincipal}\\{nombreCartera}\\Estadisticas")
        try:
            guardarEstadisticasEnCsv(dictEstadisticas,ruta)
            print("Archivo guardado correctamente")
        except:
            print("Se produjo un error guardando el archivo")#ojo si pones except generico no ves los errores. Ideal saber el error y luego capturarlo
        
    esperarPulsacion()
                  
def guardarEstadisticasEnCsv(dictEstadisticas,ruta):
    if not ruta.endswith(".csv"):
        ruta = ruta + ".csv"
        
    with open(ruta,"w",newline="") as fichero:
        
        csv_columns = ["Campo","max","min","media"]
                       
        writer = csv.DictWriter(fichero,fieldnames=csv_columns,delimiter=";",quotechar = '"')
        writer.writeheader()
        for clave,(maximo,minimo,media) in dictEstadisticas.items():
            writer.writerow({"Campo":clave,"max":maximo,"min":minimo,"media":str(round(media,2))})
    
    
                          
def ejecutarMenuGeneralEstadisticas(listaPisos,nombreCartera):
    opcion = elegirOpcionMenu("Selecciona tipo de estadística: ",menuGeneralEstadisticas)
    if opcion == 1:
        listaDistritos = dameListaDistritos(listaPisos)
        listaDistritos.append("Volver")
        opcionDistrito = elegirOpcionMenu("Selecciona un distrito: ",listaDistritos)
        if opcionDistrito != len(listaDistritos):
            listaPisos =[p for p in listaPisos if p.district == listaDistritos[opcionDistrito-1]]
            mostrarEstadisticas(listaPisos,["priceByArea","size","price","rooms"],nombreCartera)
            
    elif opcion == 2:
        mostrarEstadisticas(listaPisos, ["priceByArea","size","price","rooms"],nombreCartera)
        
        
def leerCriteriosBusqueda(listaPisos):
    
    camposExcluidos = ["propertyCode","thumbnail","numPhotos","address","province","municipality","url","title","operation","latitude","longitude","distance"
                       ,"hasVideo","hasLift","title","hasPlan","has3DTour","has360","fechaAnuncio","fechaBajaAnuncio"]
    criteriosDeBusqueda = {}
    pisoRef = listaPisos[0]#Tomo el piso 0 (i.e. [0] )para sacar los atributos de un piso
    listaCampos= list(pisoRef.__dict__.keys())
    for campo in listaCampos:
        if campo not in camposExcluidos:
            tipoCampo = type(pisoRef.__dict__[campo])
            if tipoCampo == int or tipoCampo == float:
                minimo = input(f"Introduce el valor mínimo para {campo} (Enter para continuar): ")
                if len(minimo) == 0:
                    minimo = -1
                else:
                    minimo = float(minimo)
                maximo = input(f"Introduce el valor máximo para {campo} (Enter para continuar): ")
                if len(maximo) == 0:
                    maximo = -1
                else:
                    maximo = float(maximo)
                if minimo != -1 or maximo != -1:
                    criteriosDeBusqueda[campo] = (minimo,maximo)
            elif tipoCampo == bool:
            
                valor = leerBooleano(f"Introduce el valor para {campo} (True,False,Enter para continuar): ")
                if valor != None:
                    criteriosDeBusqueda[campo] = valor
            else:
                if campo == "propertyType":
                    valor = leerOpcion(["chalet","flat","duplex","Todos"],campo)
                    if valor != None:
                        criteriosDeBusqueda[campo] = valor
                elif campo == "district":
                    listaDistritos = dameListaDistritos(listaPisos)
                    listaDistritos.append("Todos")
                    valor = leerOpcion(listaDistritos,campo)
                    if valor != None:
                        criteriosDeBusqueda[campo] = valor
                else:
                    valor = input(f"Introduce el valor para el {campo} y (Enter para continuar): ")
                    if len(valor) != 0:
                        criteriosDeBusqueda[campo] = valor
    return criteriosDeBusqueda 

def dameListaDistritos(listaPisos):
    listaDistritos=[]
    for piso in listaPisos:
        if piso.district not in listaDistritos:
            listaDistritos.append(piso.district)
    listaDistritos.sort()
    return listaDistritos
                  
                    
def buscarPisos(listaPisos):
    if len(listaPisos) == 0:
        print("Error la cartera no tiene pisos con esas características")
        return [],{}
    
    criterios = leerCriteriosBusqueda(listaPisos)
    #BUSCAR Y MOSTRAR RESULTADOS
    #print(criterios) se puso para ver los criterios de búsqueda antes de seguir programando. Si sigues no sabes que 
    # te falla ¿Es la función buscarPisos la que esta mal o es leerCriteriosBusqueda?
    listaResultados = []
    for piso in listaPisos:
        diccionarioPiso = piso.__dict__
        cumpleCriterios = True
        for (campo,valor) in criterios.items():#items devuelve tupla, por eso ponemos (campo,valor) y no campo,valor
            tipoCampo = type(diccionarioPiso[campo])
            #if len(valor) == 2:Lo cambiamos porque valor puede ser bool y no tiene longitud
            #No podemos poner if type(valor) == tuple xq son tipos de datos no básicos lo hacemos con isinstance
            if isinstance(valor,tuple):
                if diccionarioPiso[campo] == None:
                    cumpleCriterios = False
                    break
                if valor[0] != -1 and diccionarioPiso[campo] < valor[0]:
                    cumpleCriterios = False
                    break
                elif valor[1] != -1 and diccionarioPiso[campo] > valor[1]:
                    cumpleCriterios = False
                    break
            elif tipoCampo == bool:
                if diccionarioPiso[campo] != valor:
                    cumpleCriterios = False
                    break
            else:
                if valor not in diccionarioPiso[campo]:
                    cumpleCriterios = False
                    break
        if cumpleCriterios:
            listaResultados.append(piso)
    return listaResultados,criterios
                
                

def leerNombreCartera(carteras):
    listaCarteras = list(carteras.keys())
    listaCarteras.append("Volver")
    opcion = elegirOpcionMenu("Seleccionar Cartera: ",listaCarteras)
    if opcion != len(carteras) + 1:
        nombreCartera = listaCarteras[opcion-1]
    else:
        nombreCartera = None
    return nombreCartera
    
def mostrarCartera(cartera):
    opcion = elegirOpcionMenu(f"Menu: Mostrar Cartera {cartera.nombre}",menuMostrar)
    if opcion == 1:
        escribirListaPisos(cartera.pisos.values())
    elif opcion == 2:
        listaDistritos = dameListaDistritos(cartera.pisos.values())
        opcion = elegirOpcionMenu(f"{bcolors.OKCYAN}\nSelecciona distrito: ",listaDistritos)
        valor = listaDistritos[opcion-1]
        pisosdistrito = [piso for piso in cartera.pisos.values() if piso.district == valor]
        escribirListaPisos(pisosdistrito)
    elif opcion == 3:
        listaExternalReference = dameListaExternalReference(cartera.pisos.values())
        opcion = elegirOpcionMenu(f"{bcolors.OKCYAN}\nSelecciona externalReference: ",listaExternalReference)
        valor = listaExternalReference[opcion-1]
        pisosexternalReference = [piso for piso in cartera.pisos.values() if piso.externalReference == valor]
        escribirListaPisos(pisosexternalReference)
    elif opcion == 4:
        listaObraNueva = [piso for piso in cartera.pisos.values() if piso.newDevelopment]
        escribirListaPisos(listaObraNueva)
    
def dameListaExternalReference(listaPisos):
    listaExternalReference=[]
    for piso in listaPisos:
        if piso.externalReference not in listaExternalReference:
            listaExternalReference.append(piso.externalReference)
    if None in listaExternalReference:
        listaExternalReference.remove(None)
        listaExternalReference.sort()
        listaExternalReference.append(None)
    else:
        listaExternalReference.sort()
    
    return listaExternalReference
                                  
def gestionarCartera(nombreCartera,datosCartera):
    coordenadasCartera = datosCartera.split(";")[0]#En la posicion 0 tenemos lat y long
    distancia = int(datosCartera.split(";")[1])
    cartera = CarteraDePisos(nombreCartera,coordenadasCartera,distancia)#Crear una cartera vacía primero
    rutacsv = f"{rutaPrincipal}\\{nombreCartera}\\Cartera {nombreCartera}.csv"
    if not path.exists(rutacsv):
        print("No se encontró el fichero. La cartera está vacía")
        esperarPulsacion()
    else:
        pisos = CarteraDePisos.cargarCsv(rutacsv)
        cartera.añadirPisos(pisos)
        
    guardado = True    
    opcion = -1
    while opcion != len(menuCartera):
        opcion = elegirOpcionMenu(f"Menu: Cartera {nombreCartera} ",menuCartera)
        if opcion == 1:
            print("DESTINATARIOS: ")
            
            to = leerListaEmails()
            pisosAñadidos, pisosActualizados = cartera.actualizarPisos(to,f"{rutaPrincipal}\\{nombreCartera}")
            print(f"Pisos actualizados correctamente, añadidos {len(pisosAñadidos)}, actualizados {len(pisosActualizados)}")
            esperarPulsacion()
        
            try:
                CarteraDePisos.guardarEnCsv(cartera.pisos.values(),rutacsv)
                guardado = True
            except PermissionError:
                print("Error no se pudieron guardar los datos del archivo csv porque está abierto")
                esperarPulsacion()
                guardado = False
                
        elif opcion == 2:
            mostrarCartera(cartera)
            
        elif opcion == 3:
            listaPisos = list(cartera.pisos.values())
            listaPisos = filtrarPisosPorFecha(listaPisos)
            ejecutarMenuGeneralEstadisticas(listaPisos,nombreCartera)
            
        elif opcion == 4:
            listaPisos = list(cartera.pisos.values())
            listaPisos = filtrarPisosPorFecha(listaPisos)#Machacas listaPisos y la nueva vble listaPisos será filtrada
            resultados,criterios = buscarPisos(listaPisos)
            print()
                 

            if len(resultados) != 0:
                escribirCriterios(criterios)
                print()
                print(" Se encontraron", len(resultados), "pisos")
                print()
                escribirListaPisos(resultados)
                
            
                if preguntarSiNo("Quieres guardar los resultados en un fichero? "):
                    ruta = leerNombreFichero("Introduce el nombre del fichero",".csv",f"{rutaPrincipal}\\{nombreCartera}\\Busquedas")
                    try:
                        CarteraDePisos.guardarEnCsv(resultados,ruta)
                        print("Archivo guardado correctamente")
                    except:
                        print("Se produjo un error guardando el archivo")
                        
            esperarPulsacion()
            
        elif opcion == 5:
            if not guardado:
                try:
                    CarteraDePisos.guardarEnCsv(cartera.pisos.values(),rutacsv)
                    guardado = True#¿Por qué lo ponemos en True?
                except PermissionError:
                    print("Error guardando los datos en el archivo csv. Cierre el archivo abierto csv de la Cartera")
                    opcion = 0# Para no dejarle salir sin haber guardado el archivo
                    esperarPulsacion()
                    
def filtrarPisosPorFecha(listaPisos):
    fechaInicio = leerFecha("Introduce la fecha de inicio para los anuncios")
    fechaFin = leerFecha("Introduce la fecha de fin para los anuncios")
    """listaPisosFiltrados = []
    for piso in listaPisos:
        if fechaInicio <= piso.fechaAnuncio <= fechaFin:
            listaPisosFiltrados.append(piso)"""
    listaPisosFiltrados = [piso for piso in listaPisos if piso.anuncioEnIntervalo(fechaInicio,fechaFin)]
    return listaPisosFiltrados
    
    
def escribirListaPisos(pisos):
    print(f"{bcolors.OKCYAN}Total {len(pisos)} pisos:\n{bcolors.ENDC}")
    numero = 1
    for piso in pisos:
        print(f"{bcolors.OKGREEN}PISO {numero}: {bcolors.ENDC} ")
        print(piso)
        numero += 1
        print(f"{bcolors.OKGREEN}\n-----------------------------------------------------\n{bcolors.ENDC}")
    esperarPulsacion()
             
def escribirCriterios(criterios):
    print(" Criterios de Búsqueda: ")
    for clave,valor in criterios.items():
        texto = f"\t{clave}: "

        #if len(valor) == 2: Ver línea 180
        if isinstance(valor,tuple):
            if valor[0] != -1:
                texto += f"Mínimo = {valor[0]} "
            if valor[1] != -1:
                texto += f"Máximo = {valor[1]} "
        #elif type(valor) == bool: El bool lo guarda como un entero 1 o bien 0, luego en realidad es un int.
        #Esto lo hemos visto en el explorador de variables al debugear y aparece valor como int.
        
        elif type(valor) == int :
            if valor == 1:
                texto += "Cierto"
            else:
                texto += "Falso"
        else:
            texto += valor# Acuérdate += concatena
        print(texto)
        
def crearCartera(carteras):
    nombre = input("Introduce el nombre de la Cartera: ").strip()
    if nombre in carteras.keys():
        print("Error ya existe una cartera con ese nombre ")
        esperarPulsacion()
        nombre = None
        
    else:
        calle = input("Introduce la calle: ").strip()
        numero = input("Introduce el numero: ").strip()
        ciudad = input("Introduce la ciudad: ").strip()
        direccion = "calle %s, %s, %s, España"%(calle,numero,ciudad)
        localizacion = direccionACoordendas(direccion)
        if localizacion == None:
            print(" No se ha encotrado la dirección, prueba con alguna calle cercana")
            esperarPulsacion()
            nombre = None
        else:
            distancia = leerEntero("Introduce la distancia máxima en metros",minimo=50)
            carteras[nombre]="%f,%f;%d"%(localizacion.latitude,localizacion.longitude,distancia)
            guardarCarteras(carteras)
            try:
                mkdir(f"{rutaPrincipal}\\{nombre}")
                mkdir(f"{rutaPrincipal}\\{nombre}\\Estadisticas")
                mkdir(f"{rutaPrincipal}\\{nombre}\\Busquedas")
            except FileExistsError:
                pass
            print("Se creó la cartera correctamente")
            esperarPulsacion()
    return nombre
#def obtenerRutaCarteras():
#    if path.isfile("rutaCarteras.txt"):
#        with open("rutaCarteras.txt","r") as f:
#            return f.read()
#    else:
#        leido = False
#        while not leido:
#            ruta = input("Introduce la ruta donde guardar la información de tus carteras: ")
#            leido = path.isdir(ruta)
#            if not leido:
#                print("Error ruta no válida")
#        return ruta
        
def main():
    if not path.exists(rutaPrincipal):
        mkdir(rutaPrincipal)
        
    carteras = cargarCarteras()
    opcion = -1
    while opcion != len(menuInicial):
        opcion = elegirOpcionMenu("Menu: Inicial",menuInicial)
        if opcion == 1:
            nombre = leerNombreCartera(carteras)
            print(f"Este {nombre} es el nombre")
            gestionarCartera(nombre,carteras[nombre])
        elif opcion == 2:
            nombre = crearCartera(carteras)
            if nombre != None:
                gestionarCartera(nombre,carteras[nombre]) #carteras[nombre] son las coordenadas
        elif opcion == 3:
            print("Adiós")
            esperarPulsacion()
            
    
if __name__ == "__main__":#Ejecuta lo que esta dentro de main
   main()