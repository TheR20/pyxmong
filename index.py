
from optparse import Values
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson.objectid import ObjectId

MONGO_HOST = "localhost"
MONGO_PUERTO = "27017"
MONGO_TIEMPO_FUERA = 1000

MONGO_URI = "mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

MONGO_BASEDATOS="escuela"
MONGO_COLECCION="alumnos"
ID_ALUMNO = ""
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS =MONGO_TIEMPO_FUERA)
baseDatos=cliente[MONGO_BASEDATOS]
coleccion = baseDatos[MONGO_COLECCION]

def mostrar_datos(nombre="",sexo="",calificacion=""):
    #revisa si estamos enviando datos en estos campos y si nos da el dato 
    objetoBuscar={}
    if len(nombre)!=0:
        objetoBuscar["nombre"]=nombre
    if len(sexo)!=0:
        objetoBuscar["sexo"]=sexo
    if len(calificacion)!=0:
        objetoBuscar["calificacion"]=calificacion
    #intenta obtener los datos de la BD
    try:
        registros=tabla.get_children()
        #Borro los registros de la tabla cada que inicio para que no se muestre duplicados
        for registro in registros:
            tabla.delete(registro)
            #Consigo todos los reistros que hay en la BD 
        for documento in coleccion.find(objetoBuscar):
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

def doble_click_tabla(event):
    global  ID_ALUMNO
    ID_ALUMNO =str(tabla.item(tabla.selection())["text"])
    #print( ID_ALUMNO)
    documento=coleccion.find({"_id":ObjectId(ID_ALUMNO)})[0]
    #print(documento)
    nombre.delete(0,END)
    nombre.insert(0,documento["nombre"])
    sexo.insert(0,documento["sexo"])
    calificacion.insert(0,documento["calificacion"])
    crear["state"]="disabled"
    editar["state"]="normal"
    borrar["state"]="normal"
def editar_registro():
    global ID_ALUMNO
    if len(nombre.get())!=0 and len (calificacion.get())!=0 and len(sexo.get())!=0 :
        try:
            idBuscar={"_id":ObjectId(ID_ALUMNO)}
            nuevosValores={"$set":{"nombre":nombre.get(),"sexo":sexo.get(),"calificacion":calificacion.get()}}
            print(nuevosValores)
            print(idBuscar)
            coleccion.update_one(idBuscar,nuevosValores)
            nombre.delete(0,END)
            sexo.delete(0,END)
            calificacion.delete(0,END)
        except pymongo.errors.ConnectionFailure as error:
            print(error)
       
    else:messagebox.showerror("toy vacio")
    mostrar_datos()
    crear["state"]="normal"
    editar["state"]="disabled"
    borrar["state"]="disabled"
def borrar_registro():
    global ID_ALUMNO
    try:
        idBuscar={"_id":ObjectId(ID_ALUMNO)}
        print(idBuscar)
        coleccion.delete_one(idBuscar)
        nombre.delete(0,END)
        sexo.delete(0,END)
        calificacion.delete(0,END)
    except pymongo.errors.ConnectionFailure as error:
            print(error)
    mostrar_datos()
    crear["state"]="normal"
    editar["state"]="disabled"
    borrar["state"]="disabled"

def buscar_registro():
    mostrar_datos(Bnombre.get(),Bsexo.get(),Bcalificacion.get())
#crea una ventana con un grid y cabezeras
ventana = Tk()
tabla = ttk.Treeview(ventana, columns=2)
tabla.grid(row=1,column=0,columnspan=2)
tabla.heading("#0",text="ID")
tabla.heading("#1",text="Nombre")
tabla.bind("<Double-Button-1>",doble_click_tabla)
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
#Buscar Nombre
Label(ventana, text="Buscar por Nombre").grid(row=8,column=0)
Bnombre = Entry(ventana)
Bnombre.grid(row=8,column=1)
#Buscar Sexo
Label(ventana, text="Buscar por Sexo").grid(row=9,column=0)
Bsexo = Entry(ventana)
Bsexo.grid(row=9,column=1)
#Buscar Calificacion
Label(ventana, text="Buscar por Calificacion").grid(row=10,column=0)
Bcalificacion = Entry(ventana)
Bcalificacion.grid(row=10,column=1)
#boton crear
crear =Button(ventana, text="Crear alumno", command=crear_registro,bg="green",fg="white")
crear.grid(row=5,columnspan=2,sticky=W+E)
#boton editar
editar=Button(ventana, text="Editar Alumno", command=editar_registro,bg="yellow")
editar.grid(row=6,columnspan=2,sticky=W+E)
editar["state"]="disabled"
#boton borrar
borrar=Button(ventana, text="Borrar Alumno", command=borrar_registro,bg="red",fg="white")
borrar.grid(row=7,columnspan=2,sticky=W+E)
borrar["state"]="disabled"
#boton buscar
buscar =Button(ventana, text="Buscar alumno", command=buscar_registro,bg="green",fg="white")
buscar.grid(row=11,columnspan=2,sticky=W+E)
#mandamos llamara los datos desde la conexion a la BD
mostrar_datos()
ventana.mainloop()