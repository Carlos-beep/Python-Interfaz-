# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 21:27:33 2020

@author: Charlie
"""
from random import randrange
import pymysql    
conexion = pymysql.connect("localhost","root","repoio","protec")    #Parametros para conexion con base de datos
cursor = conexion.cursor()

def cerrar():
    
    conexion.close()  
def DtsNav(UN):
    sql="SELECT Nombre, Area, Admin FROM users WHERE User = %s;"
    try:
        cursor.execute(sql,(UN))
        Coinsidencias = cursor.fetchall()
        for row in Coinsidencias:
            dato0 = row[0]
            dato1 = row[1]
            dato2 = row[2]

            return dato0, dato1, dato2    
    except:
        return print("Error en modulo BDD - funcion DtsNav")
    
def acceso_R(R):
    sql="SELECT Claves FROM accesos WHERE Claves = %s;"
    try:
        cursor.execute(sql,(R))
        Coinsidencias = cursor.fetchall()
        for row in Coinsidencias:
            dato0 = row[0]
            return True #'si' #dato0        
    except:
        return print("Error en modulo BDD - funcion Acceso_R")
        
def Permisos(U):
    sql="SELECT Admin FROM users WHERE User = %s;"
    try:
        cursor.execute(sql,(U))
        Coinsidencias = cursor.fetchall()
        for row in Coinsidencias:
            dato0 = row[0]
            return dato0        
    except:
        return print("Error en modulo BDD - funcion existe")

def existe(U, P):
    sql="SELECT User, Password FROM users WHERE User = %s && password = %s;"
    try:
        cursor.execute(sql,(U, P))
        Coinsidencias = cursor.fetchall()
        for row in Coinsidencias:
            dato0 = row[0]
            return dato0        
    except:
        return print("Error en modulo BDD - funcion existe")
        
    #conexion.close() 
def CNombre(N):
    sql="SELECT Nombre FROM users WHERE Nombre = %s;"
    try:
        cursor.execute(sql,(N))
        Coinsidencias = cursor.fetchall()
        for row in Coinsidencias:
            dato0 = row[0]
            return dato0        
    except:
        return print("Error en modulo BDD - funcion CNombre")
        
    #conexion.close() 

def revisa(U):
    sql="SELECT User FROM users WHERE User = %s;"
    try:
        cursor.execute(sql,(U))
        Coinsidencias = cursor.fetchall()
        for row in Coinsidencias:
            dato0 = row[0]
            return dato0        
    except:
        return print("Error en modulo BDD - funcion existe")
        
    #conexion.close() 
    
def insert(N, U, P, A, Ad):
    consulta = "INSERT INTO users (Nombre, User, Password, Area, Admin) VALUES (%s, %s, %s, %s, %s);"
    try:
        cursor.execute(consulta,(N, U, P, A, Ad))
        conexion.commit()
    except:
        conexion.rollback()
        return print("Error en modulo BDD - funcion insert")
    #conexion.close() 
    
def borrar(D):
    consulta = "DELETE FROM users WHERE user = %s;"
    try:
        cursor.execute(consulta,(D))
        conexion.commit()
    except:
        conexion.rollback()
        return print("Error en modulo BDD - funcion Borrar")
    #conexion.close()   
    
def MostrarBD():
    sql="SELECT Temperatura, Presion, Vibracion, Bolsas, Agua FROM datos2 order by id DESC LIMIT 1;"
    try:
        cursor.execute(sql)
        Coinsidencias = cursor.fetchall()
        for row in Coinsidencias:
            temp = row[0]    
            pres = row[1]
            vib = row[2]
            bol = row[3]
            agu = row[4]
            print("Mostro")
            return temp, pres, vib, bol, agu
    except:
        return print("Error en modulo BDD - funcion mostrarBD")
 
def ChangeS():
    te = randrange(100)
    te = str(te)
    pre = randrange(100)
    pre = str(pre)
    vi = randrange(100)
    vi = str(vi)
    bo = randrange(100)
    bo = str(bo)
    ag = randrange(100)
    ag = str(ag)
    return te, pre, vi, bo, ag
        
def SimPLC():
    consulta = "INSERT INTO datos2 (Temperatura, Presion, Vibracion, Bolsas, Agua) VALUES (%s, %s, %s, %s, %s);"
    try:
        tup = ChangeS()
        cursor.execute(consulta,(tup[0], tup[1], tup[2], tup[3], tup[4],))
        conexion.commit()
    except:
        conexion.rollback()
        return print("Error en modulo BDD - funcion SimPLC")
    #conexion.close() 
    