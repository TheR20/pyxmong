
from optparse import Values
from tkinter import *
from tkinter import ttk
import pymongo

MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_TIEMPO_FUERA = 1000

MONGO_URI = "mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

MONGO_BASEDATOS="escuela"
MONGO_COLECCION="alumnos"

def mostrar_datos(tabla):
    try:
        cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS =MONGO_TIEMPO_FUERA)
        baseDatos=cliente[MONGO_BASEDATOS]
        coleccion = baseDatos[MONGO_COLECCION]
        for documento in coleccion.find():
            tabla.insert('',0,text=documento["_id"], values = documento["nombre"])
       # print(documento)
        #cliente.server_info()
        print("Coneccion a mongo exitosa")
        cliente.close()
    except pymongo.errors.ServerSelectionTimeoutError as error_tiempo:
        print("Tiempo exedido" + error_tiempo)
    except pymongo.errors.ConnectionFailure as error_conexion:
        print("Fallo la conexion" + error_conexion)

#crea una ventana con un grid y cabezeras
ventana = Tk()
tabla = ttk.Treeview(ventana, columns=2)
tabla.grid(row=1,column=0,columnspan=2)
tabla.heading("#0",text="ID")
tabla.heading("#1",text="Nombre")
#mandamos llamara los datos desde la conexion a la BD
mostrar_datos(tabla)
ventana.mainloop()