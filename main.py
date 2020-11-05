#Version de PROTEC Ver 5.2
import kivy  
from functools import partial
import os.path
from kivy.app import App
#from kivy.app import MDApp
from kivy.lang import Builder
from kivy.config import Config
from kivy.properties import ObjectProperty
from kivy.garden.navigationdrawer import NavigationDrawer
from kivy.uix.dropdown import DropDown
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
from database import DataBase
from datetime import datetime
from BDD import *
import threading
import socket
import time

kivy.require('1.9.0') 
Config.set('graphics', 'resizable', False) 
Window.size = (1080, 650)
# Config.set('graphics', 'width', '200')
# Config.set('graphics', 'height', '200')
band = True
bandL = True
bandB = True
bandE = True
admin = False
UserNow = ""

root = 'no'
host = '192.168.0.58'
port = 2055


# ClientMultiSocket = socket.socket()
# try:
#     ClientMultiSocket.connect((host, port))
#     print("CONEXION TCP/IP EXITOSA")
# except socket.error as e:
#     print("ERROR EN TCP/IP ") #+ str(e)
            
class Create(Screen, BoxLayout):    #Clase para registrar usuarios
    global admin
    admin = False
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    area = ObjectProperty(None)
        
    def submit(self):
        # Otorga permisos de Administrador
        if self.ids['chk'].active == True:
            admin = True
            Admin = 'Si'
            print("Check True")
        else:
            admin = False
            Admin = 'No'
            print("Check False")
            
            #Funcion-Comprueba que los campos tengan informacion para el registro
        if self.namee.text != "" and self.password != "" and self.email != "":
            #Funcion para insertar datos en una BD, le pasa argumentos
            insert(self.namee.text, self.email.text, self.password.text, self.area.text, Admin)   
            #Limpia las entradas de texto
            self.reset()
            sm.current = "login"         ### Screen Manager llama a ventana de login
        else:
            invalidi()                  ### Muestra ventana emergente de error
    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):                       ### Limpia entradas de texto 
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""
        self.area.text = ""
####################################################################################        
####################################################################################
class Login(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    
    def loginBtn(self):
        if existe(self.email.text, self.password.text) == self.email.text :
            
            global root, UserNow
            root = Permisos(self.email.text)
            UserNow = self.email.text
            print("Usuario Actual: " + UserNow)
            print("Permisos: " + root)
            Main.current = self.email.text ## PARA QUE PUTAS MADRES SERVIA ESTA MADRE ???
            self.reset()
            sm.current = "main"
        else:
            invalidi()              ### Muestra ventana emergente de error
            self.reset()
    def createBtn(self):           ### Screen Manager llama a ventana de login
        self.reset()
        sm.current = "create"

    def reset(self):                ### Limpia entradas de texto 
        self.email.text = ""
        self.password.text = "" 
####################################################################################
class Main(Screen, BoxLayout):
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    detiene = ObjectProperty(None)
    current = ""      
    def WgoD(self):
        seccion = DtsNav(UserNow)
        if seccion[2] == 'Si':
            sm.current = "borrar"         ### Screen Manager - ventana para Borrar
        else:
            sm.current = "confirma"         ### Screen Manager - ventana para confirmar
        
    def WgoC(self):
        seccion = DtsNav(UserNow)
        if seccion[2] == 'Si':
            sm.current = "create"         ### Screen Manager - ventana para Registrar
        else:
            sm.current = "confirma2"         ### Screen Manager - ventana para confirmar
    
    #____________________________________________________
    # Herencia de atributos a Objetos de otra clase
    def herencia(*args):
        Borrar.imp()
    #Variables de estado - Bandera
    #Comunicacion entre ventanas
    #_____________________________________________________
    
    def on_enter(self, *args):
        self.ids['boton'].disabled = False
        self.ids['detiene'].disabled = True

        self.ids['dato_t'].text = "0"
        self.ids['dato_p'].text = "0"
        self.ids['dato_v'].text = "0"
        self.ids['dato_a'].text = "0"
        self.ids['dato_b'].text = "0"
        
        global root
        if root != 'Si':
            self.ids['boton'].disabled = True
            self.ids['detiene'].disabled = True
            
    def inicio(self):
        global band
        self.ids['boton'].disabled = True
        self.ids['detiene'].disabled = False

        SimPLC()######################################################
        tup = MostrarBD()#############################################
        self.ids['dato_t'].text = tup [0]
        self.ids['dato_p'].text = tup [1]
        self.ids['dato_v'].text = tup [2]
        self.ids['dato_b'].text = tup [3]
        self.ids['dato_a'].text = tup [4]

        if band:
            self.ids['boton'].disabled = True
            self.ids['detiene'].disabled = False

            t = threading.Timer(1, self.inicio)
            t.start()
        else:
            self.ids['boton'].disabled = False
            self.ids['detiene'].disabled = True
            t = threading.Timer(1, self.inicio)
            t.cancel()

    def cambio_f(self):
        global band
        band = False
        print("Band - False")   
        
    def cambio_t(self):
        global band
        band = True
        print("Band - True") 
            
    def Scom(self):
        Input = "I 1 1 1 1 1 1 1"
        ClientMultiSocket.send(Input.encode('utf-8'))
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))

    def Dcom(self):
        Input = "I 0 1 1 1 1 1 1"
        ClientMultiSocket.send(Input.encode('utf-8'))
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))
    
    def NavDrawer(self):
        global UserNow
        dts = DtsNav(UserNow)
        now = datetime.now()
        fecha = str(now.day) + " / " + str(now.month) + " / " + str(now.year)
        tiempo = str(now.hour) + ":" + str(now.minute)
        if dts[2] == 'Si':
            permiso = "Administrador"
        else:
            permiso = "Usuario"
            
        self.ids['nombre'].text = dts[0] 
        self.ids['area'].text = dts[1]
        self.ids['permisos'].text = permiso
        self.ids['fecha'].text = tiempo + " - " + fecha
        #self.ids['hora'].text = tiempo
        
####################################################################################  
class Borrar(Screen, BoxLayout):        #BORRA USUARIOS Y VALIDA INFORMACION
    def quitar(self):
        if self.dele.text != "":
            if revisa(self.dele.text) == self.dele.text:
                exito()
                borrar(self.dele.text)
            else:
                NotExist()
                self.reset()
        else:
            invalidi()
            self.reset()
    def reset(self):
        self.dele.text = ""
    #--------------------------------------------------
    def imp():
        print("si heredo")
    #--------------------------------------------------
####################################################################################
class Confirma(Screen, BoxLayout):      #CONFIRMA QUE ES UN ADMINISTRADOR PARA BORRAR

    # def on_enter(self, *args):
    #     global root
    #     if root != 'No':
    #         sm.current="borrar"
    #     else:
    #         self.confirma()
          
    def confirma(self):
        if acceso_R(self.contra.text):
            sm.current="borrar"
        elif self.contra.text != "":
            self.reset()
            incorrect()   
        else:
            self.reset()

    def reset(self):
        self.contra.text = ""
####################################################################################
class Confirma2(Screen, BoxLayout):     #CONFIRMA QUE ES UN ADMINISTRADOR PARA REGISTRAR

    def on_enter(self, *args):
        global root
        if root != 'No':
            sm.current="create"
        else:
            self.confirma2()
            
    def confirma2(self):
        if acceso_R(self.contra.text):
            sm.current="create"
        elif self.contra.text != "":
            self.reset()
            incorrect() 
        else:            
            self.reset()
            
    def reset(self):
        self.contra.text = ""
####################################################################################
class Lavadora(Screen, BoxLayout):      #CONTROL Y MONITOREO LAVADORA

    def on_enter(self, *args):
        self.ids['boton'].disabled = False
        self.ids['detiene'].disabled = True
        
        self.ids['dato_t'].text = "0"
        self.ids['dato_v'].text = "0"
        self.ids['dato_a'].text = "0"
        
        global root
        if root != 'Si':
            self.ids['boton'].disabled = True
            self.ids['detiene'].disabled = True 
            
    def inicio(self):
        global bandL
        self.ids['boton'].disabled = True
        self.ids['detiene'].disabled = False
        
        SimPLC()######################################################
        tup = MostrarBD()#############################################
        self.ids['dato_t'].text = tup [0]
        self.ids['dato_v'].text = tup [2]
        self.ids['dato_a'].text = tup [4]

        if bandL:
            self.ids['boton'].disabled = True
            self.ids['detiene'].disabled = False
            t = threading.Timer(1, self.inicio)
            t.start()
        else:
            self.ids['boton'].disabled = False
            self.ids['detiene'].disabled = True
            t = threading.Timer(1, self.inicio)
            t.cancel()

    def cambio_f(self):
        global bandL
        bandL = False
        print("Band_L - False")   
        
    def cambio_t(self):
        global bandL
        bandL = True
        print("Band_L - True")
        
    def Scom(self):
        Input = "I L 1 1 1 1 1 1"
        ClientMultiSocket.send(Input.encode('utf-8'))
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))

    def Dcom(self):
        Input = "I L 0 1 1 1 1 1"
        ClientMultiSocket.send(Input.encode('utf-8'))
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))
####################################################################################
class Emplaye(Screen, BoxLayout):       #CONTROL Y MONITOREO EMPLAYADORA
    
    def on_enter(self, *args):
        self.ids['boton'].disabled = False
        self.ids['detiene'].disabled = True
        
        self.ids['dato_r'].text = "0"
        
        global root
        if root != 'Si':
            self.ids['boton'].disabled = False
            self.ids['detiene'].disabled = True
    
    def inicio(self):
        global bandE
        self.ids['boton'].disabled = True
        self.ids['detiene'].disabled = False
        
        SimPLC()######################################################
        tup = MostrarBD()#############################################
        self.ids['dato_r'].text = tup [0]

        if bandE:
            self.ids['boton'].disabled = True
            self.ids['detiene'].disabled = False
            t = threading.Timer(1, self.inicio)
            t.start()
        else:
            self.ids['boton'].disabled = False
            self.ids['detiene'].disabled = True
            t = threading.Timer(1, self.inicio)
            t.cancel()

    def cambio_f(self):
        global bandE
        bandE = False
        print("Band_E - False")   
        
    def cambio_t(self):
        global bandE
        bandE = True
        print("Band_E - True")
                    
    def Scom(self):
        Input = "I E 1 1 1 1 1 1"
        ClientMultiSocket.send(Input.encode('utf-8'))
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))

    def Dcom(self):
        Input = "I E 0 1 1 1 1 1"
        ClientMultiSocket.send(Input.encode('utf-8'))
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))
####################################################################################
class Bobina(Screen, BoxLayout):        #CONTROL Y MONITOREO REBOBINADO
    
    def on_enter(self, *args):
        self.ids['boton'].disabled = False
        self.ids['detiene'].disabled = True
        
        self.ids['dato_b'].text = "0"
        self.ids['dato_v'].text = "0"
        
        global root
        if root != 'Si':
            self.ids['boton'].disabled = True
            self.ids['detiene'].disabled = True 
        
    def inicio(self):
        global bandB
        self.ids['boton'].disabled = True
        self.ids['detiene'].disabled = False
        
        SimPLC()######################################################
        tup = MostrarBD()#############################################
        self.ids['dato_v'].text = tup [2]
        self.ids['dato_b'].text = tup [3]
        if bandB:
            self.ids['boton'].disabled = True
            self.ids['detiene'].disabled = False
            t = threading.Timer(1, self.inicio)
            t.start()
        else:
            self.ids['boton'].disabled = False
            self.ids['detiene'].disabled = True
            t = threading.Timer(1, self.inicio)
            t.cancel()

    def cambio_f(self):
        global bandB
        bandB = False
        print("Band_B - False")   
        
    def cambio_t(self):
        global bandB
        bandB = True
        print("Band_B - True")
        
    def Scom(self):
        Input = "I B 1 1 1 1 1 1"
        ClientMultiSocket.send(Input.encode('utf-8'))
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))

    def Dcom(self):
        Input = "I B 0 1 1 1 1 1"
        ClientMultiSocket.send(Input.encode('utf-8'))
        res = ClientMultiSocket.recv(1024)
        print(res.decode('utf-8'))
####################################################################################
class Informa(Screen, BoxLayout):       #VENTANA DE INFORMACION EXTRA
    def info():
        sm.current = "informa"
####################################################################################
class menu(ScreenManager):
    pass
####################################################################################
def invalidi():                         #VENTANAS EMERGENTES
    pop = Popup(title='Error :(',
                  content=Label(text='Revisa la informacion.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()
def incorrect():
    pop = Popup(title='Error :(',
                  content=Label(text='Clave erronea.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()
def exito():
    pop = Popup(title='Hecho :)',
                  content=Label(text='Accion realizada con exito.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open()
def NotExist():
    pop = Popup(title='Fallo :)',
                  content=Label(text='Este usuario no existe.'),
                  size_hint=(None, None), size=(400, 400))
    pop.open() 
####################################################################################
class WindowManager(ScreenManager):
    pass    
####################################################################################
        #Configuracion de frontend
kv = Builder.load_file("my.kv")
sm = WindowManager()
db = DataBase("users.txt")

        #Nombre de todas las ventanas en la aplicacion
screens = [Login(name="login"), 
           Create(name="create"),
           Main(name="main"), 
           Lavadora(name="lava"), 
           Emplaye(name="emp"), 
           Bobina(name="bob"), 
           Borrar(name="borrar"), 
           Confirma(name="confirma"), 
           Confirma2(name="confirma2"), 
           Informa(name="informa")]

for screen in screens:
    sm.add_widget(screen)
sm.current = "login"    #Ventana de inicio

class MyMainApp(App):
    title="PROTEC"
    def build(self):
        return sm
    
if __name__ == "__main__":
    MyMainApp().run()
