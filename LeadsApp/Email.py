# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 09:30:28 2020

@author: Usuario
"""
from envelopes import Envelope
import smtplib
import imaplib
import locale
import email
import os
import datetime
import html2text
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import basename #Obtener a través de la ruta el nombre del fichero
from email.header import decode_header
import webbrowser
import re
from GestorLeads import LeadMaduracion, LeadTipologia,LeadTipoContrato,LeadPromocion,LeadCaptacion,getDefaultLead

class EmailSender:
    def __init__(self,usuario,contraseña,server='smtp.gmail.com', puerto= 465):
        self.usuario = usuario
        self.contraseña = contraseña
        self.server = server
        self.puerto = puerto
        self.conexion = None
        self.logeado= False
        locale.setlocale(locale.LC_ALL,"esp")#Caracteres especiales en español
        
    def login(self):#Para probar la conexión al puerto sin tener que mandar correo
        try:
            self.conexion = smtplib.SMTP_SSL(self.server,self.puerto )# 465 es un puerto seguro
            self.conexion.ehlo()
            self.conexion.login(self.usuario,self.contraseña)
        except smtplib.SMTPException as e:#Queremos que nos diga la excepción concreta
            print ('Error conectando con el servidor...')
            print(e)
            return False
        return True
    
    def logout(self):
        self.conexion.close()
        self.conexion = None
        
    def sendEmail2(self,to,subject,body,adjuntos=[]):
        #for to_email in to: 
        envelope = Envelope(from_addr=(self.usuario),to_addr=[],subject=subject,text_body=body)
        for to_email in to:
            envelope.add_to_addr(to_email)
        print("to:",envelope.to_addr)
        for f in adjuntos:
            if f != None:
                envelope.add_attachment(f)
        try:
            resultado = envelope.send(self.server,login = self.usuario,password = self.contraseña,tls = True)#tls es la seguridad del transporte
            print(f"Email enviado {resultado[0].is_connected}")
            
        except Exception as e:
            print ('Error emviando email...')
            print(e)
            
        
        
    def sendEmail(self,to,subject,body,adjuntos=[]):
        if not self.logeado:
            self.logeado = self.login()
        if self.logeado:
            mensaje = MIMEMultipart('alternative')
            mensaje.set_charset("utf8")
            mensaje["FROM"] = self.usuario
            mensaje["Subject"] = Header(subject.encode("utf-8"),"UTF-8").encode()
            mensaje["To"] = ", ".join(to)#Convertimos la lista de receptores en una cadena de texto
            body = body.replace("\n","<br>")#Salto de linea en html
            cuerpo = MIMEText(body.encode("utf-8"),"html","UTF-8")
            mensaje.attach(cuerpo)
            for f in adjuntos:
                if f != None:
                    with open(f,"rb") as file:
                        adjunto = MIMEApplication(file.read(),Name=basename(f))
                    adjunto["Content-Disposition"]='attachment;filename="%s"' % basename(f)
                    mensaje.attach(adjunto)
        
        #body = body.encode("ascii","ignore").decode("ascii")
        #email_text = "From: " +self.usuario + "\nTo: " + ", ".join(to) + "\nSubject: " + subject \
        #+ "\n\n" + body
        #print(email_text)
        
            try:
                if not self.conexion:
                    self.login()
                self.conexion.sendmail(self.usuario, to, mensaje.as_string())
                
            
                print ('Email enviado!')
            except smtplib.SMTPException as e:#Queremos que nos diga la excepción concreta
                print ('Error emviando email...')
                print(e)

class EmailReader:
    #server = "mail.grupoedetica.com" alternativa "cpanel.grupoedetica.com"
    def __init__(self,usuario,contraseña,server, puerto= 993):#993 puerto IMAP (Protocolo para leer mail)
        self.usuario = usuario
        self.contraseña = contraseña
        self.server = server
        self.puerto = puerto
        locale.setlocale(locale.LC_ALL,"esp")#Caracteres especiales en español
        # create an IMAP4 class with SSL 
        self.bandeja = imaplib.IMAP4_SSL(self.server)
        # authenticate
        self.bandeja.login(self.usuario,self.contraseña)
    
    def formatearCaracteresEspeciales(body): # No le pongo self porque no necesita los atributos
        dUTF8 = {"=C3=81":"Á","=C3=89":"É","=C3=8D":"Í","=C3=93":"Ó","=C3=9A":"Ú","=C3=A1":"á",
                 "=C3=A9":"é","=C3=AD":"í","=C3=B3":"ó","=C3=BA":"ú","=C2=A1":"¡","=C2=BF":"¿",
                 "=C3=B1":"ñ","=C3=91":"Ñ","=E2=82=AC":"€","=E2=80=93":"-","=C2=BA":"º"}
        for clave,valor in dUTF8.items():
            body = body.replace(clave,valor)
        return body
        
        
   
    def obtenerMensajes(self,asunto="",remitente=""):# "" cadena vacía,  no filtra por ninguno de los dos
        mensajes = []
        fechas = []
        status, numero_mensajes = self.bandeja.select(readonly = False)
        (res,mensajes_no_leidos) = self.bandeja.search(None,"(UNSEEN)")
        print(status,numero_mensajes)
        # total number of emails
        if res != "OK":# Si no ha podido leerlos
            return mensajes,fechas

        for i in mensajes_no_leidos[0].split(): # Recorremo los mensajes no leidos
            res,mensaje = self.bandeja.fetch(i,"(RFC822)") # RFC822Formato para las direcciones de email
            msg = email.message_from_bytes(mensaje[0][1])
            # print(msg)
            subject, encoding = decode_header(msg["Subject"])[0]
            sender = msg["From"]
            # print(msg.keys())
            # print(f" From: {sender}")
            date = decode_header(msg["Date"])[0][0]
            if "," in date:
                date = date.split(", ")[1]
            # date = date.split(" +")[0]
            # date = datetime.datetime.strptime(date,"%-d %b %Y %-H:%M:%S")
            date = email.utils.parsedate_to_datetime(date)#Convertimos con la propia libreria email
            if isinstance(subject, bytes) and encoding:#Si son bytes y tenemos encodin lo decodificamos
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            #print(subject)
            if asunto in str(subject) and remitente in sender: # Cadena vacía en cualquier cadena es TRUE. Por defecto, no hay filtro
                mensajes.append(msg)
                fechas.append(date)
                typ,data = self.bandeja.store(i,"FLAGS",'\\Seen') # Marcamos el mensaje como leído
                # print(f"mensaje {i} marcado como leido typ = {typ} data= {data}")
            else:
                typ, data = self.bandeja.store(i, "-FLAGS", '\\Seen')
        return mensajes, fechas

    def get_conversor():
        conversor = html2text.HTML2Text()
        conversor.ignore_links = True
        conversor.unicode_snob = True
        conversor.ignore_anchors = True
        conversor.ignore_images = True
        conversor.ignore_tables = True
        conversor.single_line_break = True
        return conversor

    def limpiar_texto(texto):
        conversor = EmailReader.get_conversor()
        texto = conversor.handle(texto)
        texto = texto.replace("= ", "")
        texto = EmailReader.formatearCaracteresEspeciales(texto).strip()
        texto = re.sub("<[^>]*>", "", texto)
        return texto
    
    def obtenerClientesFormulario(self):
        clientes = []
        mensajes, fechas = self.obtenerMensajes(asunto = "Nuevo mensaje de grupoedetica.com",remitente = "mail@grupoedetica.com")
        for mensaje,fecha in zip(mensajes,fechas):
            cliente = getDefaultLead()
            cliente["Modo captación"] = str(LeadCaptacion.FACEBOOK_WEB)
            cliente["Fecha captación"] =fecha#.date()#Hemos quitado el punto date para mantanerlo como datetime y tener la hora
            # print(f"mensaje.get_payload: {mensaje.get_payload(decode = False)}")
            # print(f"tipo mensaje.get_payload: {type(mensaje.get_payload(decode = False))}")
            body = mensaje.get_payload(decode = False).strip()
            
            # print(body)
            # body = mensaje.get_body()
            datos = body.split("\r\n\r\n")[1:-3]
            for dato in datos : # Quitamos los str de la lista que no queremos
                #print("#######################################") - +-
                #print(dato)
                partes = dato.split(":\r\n")
                if len(partes) == 2:
                    cliente[partes[0]]=partes[1]
                else:
                    cliente["Mensaje"] = cliente["Mensaje"] + partes[0] # Para que no se líe con los saltos de línea del mensaje
            if "Email" in cliente and "no-reply" in cliente["Email"]:
                continue #Vuelvo arriba del bucle si veo que hay un no-reply y no hago el append posterior
                #Con el continue me quito correo basura
            if "Mensaje" not in cliente:
                cliente["Mensaje"] = body.split("Mensaje:")[1].split("Política de Privacidad")[0].strip()
            clientes.append(cliente)
            # clientes["Email"] = [clientes["Email"]]
        return clientes
    
    def obtenerMensajesDeCliente(self, leads_emails):
        mensajes = []
        for lead_email in leads_emails:
            mensajes_recibidos_lead, fechas_mensajes_recibidos = self.obtenerMensajes(remitente = lead_email)
            for mensaje_recibido, fecha in zip(mensajes_recibidos_lead,fechas_mensajes_recibidos):
                mensaje = {"Email":lead_email, "Fecha": fecha,"Lista adjuntos":[],"Recibido":True,"Enviado":False}
                if mensaje_recibido.is_multipart():
                    i = 0
                    for part in mensaje_recibido.walk():
                        print(f" {i}:{part.get_payload()}")
                        if i == 1:
                            mensaje["Mensaje"] = part.get_payload()
                        i += 1
                else:
                    mensaje["Mensaje"] = mensaje_recibido.get_payload(decode=False).strip()
                mensaje["Mensaje"] = EmailReader.formatearCaracteresEspeciales(mensaje["Mensaje"])

                mensaje["Asunto"] = mensaje_recibido["subject"]
                mensajes.append(mensaje)

        return mensajes
    
    def obtenerClientesIdealista(self):
        conversor = EmailReader.get_conversor()
        clientes = []
        mensajes, fechas = self.obtenerMensajes(asunto = "Nuevo mensaje", remitente = "noreply.pro.es@idealista.com")
        for mensaje,fecha in zip(mensajes,fechas):
            cliente = {}
            cliente["Modo Captación"] = "Idealista"
            cliente["Fecha Captación"] =fecha
            
            # print(f"mensaje.get_payload: {mensaje.get_payload(decode = False)}")
            # print(f"tipo mensaje.get_payload: {type(mensaje.get_payload(decode = False))}")
            body = mensaje.get_payload(decode = False)
            body = EmailReader.limpiar_texto(body)

            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print(body)
            
            if "Hay un nuevo mensaje de" in body: 
                body = body.split("Hay un nuevo mensaje de:")[1].strip()
                # body = body.replace("</tbody>  \n","")
                cliente["Nombre"] = body.split("\n")[0].strip()
                cliente["Email"] = body.split("\n")[1].strip()
                cliente["Teléfono"] = body.split("\n")[2].strip()
                cliente["Mensaje"] = "\n".join(body.split("Responder")[0].split("\n")[3:]).strip()
            elif "Nuevo mensaje de" in body:
                body = body.split("Nuevo mensaje de")[1]
                cliente["Mensaje"] = body.split('"')[1].strip()
                if len(body.split("**")) == 3:
                    cliente["Nombre"] = body.split("**")[1].strip()
                    body = body.split("**")[2]
                    cliente["Email"] = body.split("\n")[1].strip()
                    cliente["Teléfono"] = body.split("\n")[2].strip()
                else:
                    cliente["Nombre"] = body.split("**")[1].split("\n")[0].strip()
                    cliente["Email"] = (body.split("**")[1]).split("\n")[1].strip()
                    cliente["Teléfono"] = body.split("**")[1].split("\n")[2].strip()
                # print(body)
            else:
                continue #Vuelve al principio del bucle y no se para. El tema es que clientes con formato distinto no los añade

            if "Anuncio por el que has contactado  " in body:
                anuncio = body.split("Anuncio por el que has contactado  ")[1].strip()
            elif "Anuncio por el que contacta" in body:
                anuncio = body.split("Anuncio por el que contacta")[1].strip()
            elif "Anuncio por elque contacta" in body:
                anuncio  = body.split("Anuncio por elque contacta")[1].strip()
            else:
                anuncio = "" # Si el anuncio no tiene formato OK el programa no da error, te da ""
                
            if anuncio !="":
                anuncio = anuncio.split("idealista")[0].strip()
                anuncio = anuncio.replace("¿Problemas? Contacta con","").strip()
                if anuncio[-1] == "=":
                    anuncio = anuncio[:-1].strip()
                anuncio = anuncio.replace("\n"," ")
                anuncio = anuncio.replace("\xa0"," ")
                
                if "Ref" in anuncio:
                    datos_anuncio = anuncio.split("(Ref.")
                    anuncio = datos_anuncio[0].strip()
                    cliente["Referencia"] = datos_anuncio[1].split(")")[0].strip()
                    cliente["Precio"] = datos_anuncio[1].split(")")[1].replace("=","").strip()
                    
                if anuncio.startswith("Promoción"):
                    anuncio = anuncio.replace("Promoción","")
                    cliente["Promoción de interés"] = anuncio.split(",")[0].strip()
                else:
                    datos_anuncio = anuncio.split("-")
                    cliente["Piso"] =datos_anuncio[0].strip()
                    if len(datos_anuncio) >1: # Para que incluya anuncios antiguos sin guión
                        cliente["Promoción de interés"] = datos_anuncio[1].split(",")[0].replace("s\n","").strip() 
                        
                    
            # print(f"anuncio: '{anuncio}'")
            
            # cliente["Email"] = [cliente["Email"]]
            clientes.append(cliente)   
        return clientes
            
                
        """ Nombre = body.split("\n")[1].strip()
            email = body.split("\n")[2].strip()
            telefono = body.split("\n")[3].strip()
            print("----")
            print(body)
            print("----")
            mensaje = "\n".join(body.split("Responder")[0].split("\n")[4:])
            print(Nombre,email,telefono)
            print(mensaje)
            anuncio = body.split("Anuncio por el q= ue has contactado")[1].split("\n")[1]
            print(f"anuncio: {anuncio}")"""
def main():
    lectoremail = EmailReader("info@grupoedetica.com","QhnbFrQ34vXP","mail.grupoedetica.com")
    print("login ok")
    print(lectoremail.obtenerClientesFormulario())
    # print(lectoremail.obtenerClientesIdealista())
    # print(lectoremail.obtenerClientesFormulario())
    
    
    

if __name__ == "__main__":#Ejecuta lo que esta dentro de main
    main()  
    
        