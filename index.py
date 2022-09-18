
from optparse import Values
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo

MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_TIEMPO_FUERA = 1000

MONGO_URI = "mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

MONGO_BASEDATOS="escuela"
MONGO_COLECCION="alumnos"
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS =MONGO_TIEMPO_FUERA)
baseDatos=cliente[MONGO_BASEDATOS]
coleccion = baseDatos[MONGO_COLECCION]
def mostrar_datos():
    try:
        registros=tabla.get_children()
        #Borro los registros de la tabla cada que inicio para que no se muestre duplicados
        for registro in registros:
            tabla.delete(registro)
            #Consigo todos los reistros que hay en la BD 
        for documento in coleccion.find():
         tabla.insert('',0,text=documento["_id"], values = documento["nombre"])
       # print(documento)
        #cliente.server_info()
        print("Coneccion a mongo exitosa")      
    except pymongo.errors.ServerSelectionTimeoutError as error_tiempo:
        print("Tiempo exedido" + error_tiempo)
    except pymongo.errors.ConnectionFailure as error_conexion:
        print("Fallo la conexion" + error_conexion)

def crear_registro():
    if len(nombre.get())!=0 and len (calificacion.get())!=0 and len(sexo.get())!=0 :
        try:
            documento= {"nombre": nombre.get(),"calificacion":calificacion.get(), "sexo":sexo.get()}
            coleccion.insert_one(documento)
            nombre.delete(0,END)
            sexo.delete(0,END)
            calificacion.delete(0,END)
        except pymongo.errors.ConnectionFailure as identifier:
            print(identifier)
    else:
        messagebox.showerror(message="Los campos estan vacios")
    mostrar_datos()

#crea una ventana con un grid y cabezeras
ventana = Tk()
tabla = ttk.Treeview(ventana, columns=2)
tabla.grid(row=1,column=0,columnspan=2)
tabla.heading("#0",text="ID")
tabla.heading("#1",text="Nombre")
#Nombre
Label(ventana, text="Nombre").grid(row=2,column=0)
nombre = Entry(ventana)
nombre.grid(row=2,column=1)
#Sexo
Label(ventana, text="Sexo").grid(row=3,column=0)
sexo = Entry(ventana)
sexo.grid(row=3,column=1)
#Calificacion
Label(ventana, text="Calificacion").grid(row=4,column=0)
calificacion = Entry(ventana)
calificacion.grid(row=4,column=1)
#boton crear
crear =Button(ventana, text="Crear alumno", command=crear_registro,bg="green",fg="white")
crear.grid(row=5,columnspan=2)
#mandamos llamara los datos desde la conexion a la BD
mostrar_datos()
ventana.mainloop()