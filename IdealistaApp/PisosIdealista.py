
from Email import EmailSender
import json
from json import JSONEncoder
from json import JSONDecodeError
import requests
from requests.auth import HTTPBasicAuth
import csv
import os.path
from os import path
import sys
from datetime import datetime,date
import httplib2
from fake_useragent import UserAgent #Como importamos una clase es con mayúscula
#El fake-useragent es para acceder a internet desde diferentes navegadores para engañar al servidor



class Piso:
    def __init__(self,propertyCode,externalReference,floor,
                 price,propertyType,size,rooms,bathrooms,address,
                 municipality,district,latitude,longitude,url,
                 distance,newDevelopment,hasLift,priceByArea,
                 topNewDevelopment,fechaAnuncio=date.today()):
        self.propertyCode = propertyCode
        self.externalReference = externalReference
        self.floor = floor
        self.price = price
        self.propertyType = propertyType
        self.size = size
        self.rooms = rooms
        self.bathrooms =bathrooms
        self.address = address
        self.municipality = municipality
        self.district = district
        self.latitude = latitude
        self.longitude = longitude
        self.url = url
        self.distance = distance
        self.newDevelopment = newDevelopment
        self.hasLift = hasLift
        self.priceByArea = priceByArea
        self.topNewDevelopment = topNewDevelopment
        #self.fechaAnuncio = date.today()#No lo meto en el __init__ en sus parámetros porque no me tienen que dar el valor
        self.fechaAnuncio = fechaAnuncio
        
        
        
    # Ejemplo de piso (PropertyCode: Ref4563, ExternalReference: Extr23fc
    # Dirección: Avda de Elvas, Superficie: 145 m2, 
    # Precio: 140.000 euros, Preciom2: 950 euros/m2  )   
    def __str__(self):
        salida = "PropertyCode: " + self.propertyCode + ", ExternalReference: " +\
    str(self.externalReference) + "\nDirección: " +self.address
        if self.floor != None:
            salida += " Planta " + str(self.floor)
        
        salida += "\nDistrito: " + self.district + "\nSuperficie: " +\
    str(self.size) + "m2,\nPrecio: " +str(self.price) + " euros, Preciom2: " +\
    str(self.priceByArea) + " euros\m2\nTipo de inmueble: " + self.propertyType
       
        #if self.hasVideo:
            #salida += " Tiene video."
        if self.newDevelopment:
            salida += " Nueva Construcción. "
        if self.hasLift:
            salida += " Tiene ascensor. "
        #if self.hasPlan:
            #salida += " Tiene planos. "
        #if self.has360:
            #salida += " Tiene Tour 360. "
        #if self.has3DTour:
            #salida += " Tiene Tour 3D. "
        if self.topNewDevelopment:
            salida += " Piso promocionado de Obra Nueva. "
        salida += "\n" + self.url
        return salida
    def __eq__(self,other):
        if not isinstance(other,Piso):
            return False
        else:
            return self.propertyCode == other.propertyCode
        #Implementar hash??????
    def __hash__(self):#Entra una clave y devuelve un número. 
        return hash(self.propertyCode)
    
    def anuncioEnIntervalo(self,fechaInicio,fechaFin):
        if isinstance(self.fechaAnuncio,datetime):
            self.fechaAnuncio = self.fechaAnuncio.date()
        if isinstance(fechaInicio,datetime):
            fechaInicio= fechaInicio.date()
        if isinstance(fechaFin,datetime):
            fechaFin = fechaFin.date()
        return fechaInicio <= self.fechaAnuncio <= fechaFin
    
    def getCambios(self,otropiso):
        cambios = {}
        selfd = self.__dict__
        otrod = otropiso.__dict__
        for atributo in selfd.keys():
            if atributo != "fechaAnuncio" and selfd[atributo] != otrod[atributo]:
                cambios[atributo] = (selfd[atributo],otrod[atributo])
        return cambios
    
    def JsonToPiso(piso):
        """ jsontext = str(jsontext)
        print("Convirtiendo:",jsontext)
        jsontext = jsontext.replace("'","\"") 
        try:
            piso = json.loads(jsontext) 
        except JSONDecodeError as e:
            print(e) """
        try:
            floor = (piso["floor"])
            if floor == "bj":
                floor = 0 #Convertimos bj en el número 0 ¿xq? Para las búsquedas por piso tiene que ser un entero
            elif floor =="en":
                floor == 0
            elif floor == "st":
                floor == -1
            
            else:
                floor = int(floor)
        except KeyError:
            floor = None
        except ValueError:
            floor = None
        
        try:
            hasLift = bool(piso["hasLift"])
        except KeyError:
            hasLift = False
        
        try:
            externalReference = piso["externalReference"]
        except KeyError:
            externalReference = None
            
            
        return Piso(piso['propertyCode'],
                    externalReference,floor,
                    int(piso['price']),piso['propertyType'],
                    int(piso['size']),int(piso['rooms']),int(piso['bathrooms']),piso['address'],
                    piso['municipality'],piso['district'],
                    str(piso['latitude']),str(piso['longitude']),piso['url'],
                    int(piso['distance']),bool(piso['newDevelopment']),
                    hasLift,int(piso['priceByArea']),
                    bool(piso['topNewDevelopment'])) 
        
"""class PisoJsonEncoder(JSONEncoder):
    def default(self,p):
        return p.__dict__"""

class IdealistaScraping:
    #coordenadasCiudades = {"Badajoz":'38.890891,-6.999911'}
    
    
    def __init__(self,apikey,secret):
        self.apikey = apikey
        self.secret = secret
        self.token = self.getToken()
    
    def getToken(self):
        auth_url = "https://api.idealista.com/oauth/token"
        
        
        auth = HTTPBasicAuth(self.apikey, self.secret)
        headers = {'Content-Type': ('application/'
                                    'x-www-form-urlencoded;charset=UTF-8')}
        payload = {'grant_type': 'client_credentials',
                   'scope': 'read'}
        response = requests.post(auth_url,
                                 headers=headers,
                                 data=payload,
                                 auth=auth)
        response_data = response.json() # nos quedamos con el JSON de response
       # seconds = response_data["expires_in"]
        token = response_data['access_token']
        return token#Cómo sabe el programa si no ha caducado el token?

    def obtenerListaPisos(self,coordenadas,distancia=5000,maxItems=50,
                          order='publicationDate',sort="desc"):
        
        #1. Configuro los datos de la búsqueda
        data = {
            'center': coordenadas,
            'distance': distancia, # en metros
            'operation': 'sale', # sale o rent
            'propertyType': 'homes', # homes, offices, premises, garages, bedrooms
            'locale': 'en', # es, it, pt, en, ca
            'maxItems': maxItems,
            'order': order,
            'numPage': 0,  # cambiar para diferenciar peticiones
            'sort': sort }

        #2. Pido la búsqueda al portal de Idealista
        url = "https://api.idealista.com/3.5/es/search"
        headers = {'Authorization': 'Bearer ' + self.token, 'Content-Type':('application/'
                                    'x-www-form-urlencoded;charset=UTF-8') }
        
        #request.post envía una petición al servidor
        #devuelve la respuesta del servidor (response_post)
        response_post = requests.post(url,
                         headers=headers,
                         data=data) # data = dictionario de datos/filtros
        
        #3 .Obtengo la respuesta en formato json
        pisos = []
        try:
            jsontext = response_post.json()
            print(f"Jsontext ; {jsontext}")
            jsonlist = jsontext["elementList"] #json en lista
            print("lista json obtenida")
    
            #4. Convierto la búsqueda en formato json en una lista de objetos Piso
    
            for pisoJson in jsonlist: #recorrer la lista json
                print("\n\nConvirtiendo:",pisoJson)
                pisos.append(Piso.JsonToPiso(pisoJson))
                print("Piso creado:",pisos[-1])
        except:
            print("La búsqueda en idealista no se pudo realizar: ",sys.exc_info())
        
        return pisos
    
    def existeAnuncio(url):
        return True
        
        
        
        
class CarteraDePisos():
    def __init__(self,nombre,coordenadas,distancia):
        self.nombre = nombre
        self.coordenadas = coordenadas
        self.distancia = distancia
        self.pisos ={}#Tengo un poco de lío con los pisos como dic o lista
    
    def estaVacia(self):
        return len(self.pisos) == 0
        
    def añadirPiso(self,piso):
        self.pisos[piso.propertyCode]=piso# Si pisos es lista porque accede
        #como diccionario
        
    def existePiso(self,piso):
        return piso.propertyCode in self.pisos.keys()
    
    def añadirPisos(self,listaPisos):
        for piso in listaPisos:
            self.añadirPiso(piso)
            
    def inicializarCartera(self,maxItems=200):
        buscador = IdealistaScraping('zv3u0zzhv10ojbnnrzm1rhc4rnxpjcv5','L4z1zpuu1LKH')
        pisos = buscador.obtenerListaPisos(self.coordenadas,maxItems=maxItems)
        self.añadirPisos(pisos) 
    
    def __str__(self):
        salida = "cartera de pisos (Total:" + str(self.getNumPisos()) + "): \n\n "
        for piso in self.pisos.values():
            salida += str(piso) + "\n\n"
        return salida
    
    def getNumPisos(self):
        return len(self.pisos)    
    
    def dameListaDistritos(self):
        """listaDistritos = []
        for piso in self.pisos.values():
            if piso.district not in listaDistritos:
                listaDistritos.append(piso.district)"""
        listaDistritos = list(set([piso.district for piso in self.pisos.values()]))
        listaDistritos.sort()
        return listaDistritos
    
    def damePisosDistrito(self,distrito):
        """listaPisosDistrito = []
        for piso in self.pisos.values():
            if piso.district == distrito:
                listaPisosDistrito.append(piso)"""
        listaPisosDistrito = [piso for piso in self.pisos.values() if piso.district == distrito]
        return listaPisosDistrito 
    

    
    #Método estático (de clase, no usa atributos del objeto)
    #que guarda una lista de pisos (pisos) en un csv (ruta)
    def guardarEnCsv(pisos,ruta):
        if not ruta.endswith(".csv"):
            ruta = ruta + ".csv"
        
        with open(ruta,"w",newline="") as fichero:
            
            csv_columns = ["propertyCode","externalReference",
                           "floor","price","propertyType","size","rooms",
                           "bathrooms","address","municipality","district",
                           "latitude","longitude","url","distance",
                           "newDevelopment","hasLift","priceByArea",
                           "topNewDevelopment","fechaAnuncio"
                           ]#Error: iterable expected, not Piso por eso hemos metido 191
            writer = csv.DictWriter(fichero,fieldnames=csv_columns,delimiter=";",quotechar = '"')
            writer.writeheader()
            for piso in pisos:

                writer.writerow({"propertyCode": piso.propertyCode,
                                 "externalReference": str(piso.externalReference),
                                 "floor": str(piso.floor),
                                 "price": str(piso.price),"propertyType": piso.propertyType,
                                 "size": str(piso.size),
                                 "rooms": str(piso.rooms),"bathrooms": str(piso.bathrooms),
                                 "address": piso.address,
                                 "municipality": piso.municipality,"district": piso.district,
                                 "latitude": str(piso.latitude),"longitude": str(piso.longitude),
                                 "url": piso.url,"distance": str(piso.distance),
                                 "newDevelopment": str(piso.newDevelopment),
                                 "hasLift": str(piso.hasLift),"priceByArea": str(piso.priceByArea),
                                 "topNewDevelopment": str(piso.topNewDevelopment),
                                 "fechaAnuncio": piso.fechaAnuncio.strftime("%Y/%m/%d")})
            
        
    #Método estático que devuelve una lista de pisos leídos de un fichero csv    
    def cargarCsv(ruta):
        def str2bool(b):
            return b.lower()=="true"
        pisos = []

        with open(ruta,"r",newline = "") as fichero:
            
            reader = csv.DictReader(fichero,delimiter=";",quotechar = '"')
            for row in reader:
                #print(row)
                try:
                    floor = int(row["floor"])
                except ValueError:
                    floor = None
                    
                if row["externalReference"] == "None":
                   row["externalReference"] = None
                   
                  
                try:
                    fechaAnuncio = datetime.strptime(row["fechaAnuncio"],"%Y/%m/%d").date()
                except ValueError:
                    fechaAnuncio = datetime.strptime(row["fechaAnuncio"],"%d/%m/%Y").date()
                    
                piso = Piso(row["propertyCode"],row["externalReference"],floor,
             int(row["price"]),row["propertyType"],int(row["size"]),int(row["rooms"]),int(row["bathrooms"]),row["address"],
             row["municipality"],row["district"],str(row["latitude"]),str(row["longitude"]),row["url"],
             int(row["distance"]),str2bool(row["newDevelopment"]),str2bool(row["hasLift"]),int(row["priceByArea"]),
             str2bool(row["topNewDevelopment"]),fechaAnuncio)
                pisos.append(piso)

        return pisos
          
    def actualizarPisos(self,to,ruta): 
        buscador = IdealistaScraping('zv3u0zzhv10ojbnnrzm1rhc4rnxpjcv5','L4z1zpuu1LKH')
        pisosNuevos = []
        for distancia in [self.distancia,0.66*self.distancia,0.4*self.distancia,0.2*self.distancia,0.1*self.distancia]:
            pisosNuevos = pisosNuevos + buscador.obtenerListaPisos(self.coordenadas,distancia=distancia)#Sobrecarga el operador + para sumar listas 
        pisosNuevos = list(set(pisosNuevos))
        pisosAñadidos, pisosActualizados = self.clasificarNuevos(pisosNuevos)
        informeAñadidos,csvAñadidos = self.cargarAñadidos (pisosAñadidos,ruta)
        informeActualizados,csvActualizados = self.cargarActualizados(pisosActualizados,ruta)
        #Enviar por email los informes y los csv
        #print("NUEVOS PISOS")
        #print(informeAñadidos)
        #print("PISOS ACTUALIZADOS")
        #print(informeActualizados)
        
        #to = ["luisgarciaf@gmail.com","jg123423@gmail.com","cbarbero@grupoedetica.com"] Ahora lo pasamos
        #fuera como parámetro
        fecha = date.today().strftime("%Y-%m-%d")
        with open(f"{ruta}\\Informe Actualización {fecha}.txt","w") as f_informe:
            f_informe.write("PISOS NUEVOS: \n")
            f_informe.write(informeAñadidos + "\n\n")
            f_informe.write("PISOS ACTUALIZADOS: \n")
            f_informe.write(informeActualizados + "\n\n")
        
        if len(to) != 0:
            subject = "Actualizaciones desde IDEALISTA"
            body = "<h1>Pisos Nuevos</h1> \n" + informeAñadidos + \
            "\n\n\n<h1>Pisos Actualizados</h1>\n" + informeActualizados 
            #h1 Abre cabecera de tamaño 1 y la cierra con </h1>
            emailsender = EmailSender("buscadoridealista@gmail.com","BUSCADORIDEALISTA123")
            emailsender.sendEmail(to,subject,body,[csvAñadidos,csvActualizados])
        return pisosAñadidos,pisosActualizados
       
    def hayCambio (piso1, piso2):
        return len(piso1.getCambios(piso2)) > 0


    def clasificarNuevos(self, pisosNuevos):
        pisosActualizados = []
        pisosAñadidos = []

        #Comprobar si diccionario contiene clave:
        #   if key in d.keys()

        #Obtener el valor de una clave del diccionario
        #   d[key]

        for pisoNuevo in pisosNuevos:
            #Comprobar si en el diccionario self.pisos no existe la clave pisoNuevo.propertyCode
            if not self.existePiso(pisoNuevo):
                pisosAñadidos.append(pisoNuevo)
            else: #existe el piso en mi diccionario self.pisos
                #comparo el nuevo anuncio con los datos guardados en mi diccionario de pisos
                if CarteraDePisos.hayCambio(pisoNuevo, self.pisos[pisoNuevo.propertyCode]):
                    pisosActualizados.append(pisoNuevo)
                #else: el piso ya existía y no ha cambiado ningún dato (NO HACER NADA)
        return pisosAñadidos, pisosActualizados

    def cargarAñadidos(self, pisos,ruta):

        #Guardar en el csv
        now = datetime.now() #obtener la fecha actual
        dateStr = now.strftime("%Y-%m-%d %H-%M-%S")
        if len(pisos) != 0:
            rutacsv = f"{ruta}/Cartera {self.nombre} nuevos {dateStr}.csv"
            CarteraDePisos.guardarEnCsv(pisos,rutacsv)
        else:
            rutacsv = None
        #Actualizar la cartera (self.pisos) y generar informe para email
        añadidosEmail = ""
        

        for piso in pisos:
            self.añadirPiso(piso)
            #añadir datos a añadidosEmail
            añadidosEmail += "Dirección : " + piso.address + "\n" + "url : " \
            + piso.url + "\n\n"

        return añadidosEmail,rutacsv
    

    def cargarActualizados(self, pisos,ruta):
        
        def cambiosToStr(cambios,piso):
            
            salida = "Dirección : " + piso.address + "\n"
            salida += "url : " + piso.url + "\n"
            for atributo,(valoranterior,valornuevo) in cambios.items():
                salida += "\t" + atributo + " : valoranterior = " + str(valoranterior) \
                + " : valornuevo = " + str(valornuevo) + "\n"
            salida += "\n"
            return salida
            
                
            
        #Guardar en el csv
        now = datetime.now() #obtener la fecha actual
        dateStr = now.strftime("%Y-%m-%d %H-%M-%S")
        if len(pisos) != 0:
            rutacsv = f"{ruta}/Cartera {self.nombre} actualizados {dateStr}.csv"
            CarteraDePisos.guardarEnCsv(pisos, rutacsv)
        else:
            rutacsv = None
        #Actualizar la cartera (self.pisos) y generar informe para email
        actualizadosEmail = ""
        

        for pisoActualizado in pisos:
            pisoAntiguo = self.pisos[pisoActualizado.propertyCode]
            cambios = pisoAntiguo.getCambios(pisoActualizado)
            actualizadosEmail += cambiosToStr(cambios,pisoActualizado)
            pisoActualizado.fechaAnuncio = now
            self.añadirPiso(pisoActualizado)
            #añadir datos a actualizadosEmail

        return actualizadosEmail,rutacsv


                
"""
def main():# Sin opciones, abría la cartera y la actualizaba
    rutacsv = "CarteraBadajoz.csv"
    cartera = CarteraDePisos()
    if not path.exists(rutacsv):
        print("No se encontró el fichero",rutacsv)
        respuesta = input( "Quieres inicializar una cartera nueva desde idealista (s/n) : ")
        if respuesta =="s" or respuesta == "S":
            cartera.inicializarCartera()
            print(cartera)
        else:    
            while rutacsv != "-" and not path.exists(rutacsv):
                print("No se encontró el fichero",rutacsv)
                rutacsv = input("Introduce una nueva ruta del fichero o - para cancelar : ")
                if rutacsv[0] == "-":
                    sys.exit(0)
            pisos = CarteraDePisos.cargarCsv(rutacsv)
            cartera.añadirPisos(pisos)
            cartera.actualizarPisos()
    else:
        pisos = CarteraDePisos.cargarCsv(rutacsv)
        cartera.añadirPisos(pisos)
        cartera.actualizarPisos()
        #actualiar pisos y enviar emails
       
    #Llamada al método estático (a través de la clase, no del objeto) 
    CarteraDePisos.guardarEnCsv(cartera.pisos.values(),rutacsv)
    
if __name__ == "__main__":#Ejecuta lo que esta dentro de main
    main()
""" 
    
    
    
