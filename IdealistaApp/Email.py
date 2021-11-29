# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 09:30:28 2020

@author: Usuario
"""
from envelopes import Envelope
import smtplib
import locale
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import basename #Obtener a través de la ruta el nombre del fichero

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