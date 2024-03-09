from tkinter import *
from tkinter import ttk, filedialog
import sqlite3
import os
import tkinter.messagebox as messagebox
from tkinter.messagebox import showerror
import re
from PIL import Image, ImageTk

"""
DEV = Elias Escalante

Descripcion:
    App proyecto final UTN.BA DIPLOMATURA, practica con Tkinter.
    Aplicacion de escritorio que permite realizar un CRUD  en una base de datos SQLITE.
    Tambien permite exportar la base de datos en .txt asi como también la consulta.
    Tambien se puede cambiar el color de fondo de la aplicacion con el modo oscuro y volver a su modo clásico
    Intente realizar una interfaz intuitiva y facil de usar.
"""



#############################################################################################
# FUNCIONES
#############################################################################################

def crear_base_datos():
    """
    CREA LA BASE DE DATOS EN DONDE SE VA ALOJAR LA INFORMACION DE LOS MATERIALES.
    SI LA BASE DE DATOS YA EXISTE IMPRIME UN MENSAJE POR CONSOLA Y TERMINA LA FUNCION.
    POR EL CONTRARIO NO EXISTE, ENTONCES CONECTA A LA BASE DE DATOS "basededatos.db" Y LA CREA
    DENTRO DE LA MISMA CREA LA TABLA MATERIALES SI NO EXISTE CON SUS CAMPOS QUE NO PUEDEN SER NULOS
    """

    #genero un print si ya existe la base Y utilizo una estructura condicional para chequear esto
    if os.path.exists('basededatos.db'):
        print("la base ya existe")
        return
    
    # Conecto a la base de datos (si no existe, se crea)
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()

    # Creo tabla si no existe dentro de la base de datos con sus campos
    cursor.execute('''CREATE TABLE IF NOT EXISTS materiales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        material INTEGER NOT NULL,
                        descripcion TEXT NOT NULL,
                        precio_venta REAL NOT NULL,
                        precio_costo REAL NOT NULL,
                        stock INTEGER NOT NULL,
                        proveedor TEXT NOT NULL)''')

    # guardo los cambios y despues cierro la conexión
    conexion.commit()
    conexion.close()

    # genero un print para chequear en consola que se creo la base
    print("base creada")


def exportar_base():
    """
    EXPORTA TODA LA BASE DE DATOS A UN ARCHIVO 
    .TXT Y DEJA ELEGIR DONDE GUARDARLO MEDIANTE  UNA VENTANA EMERGENTE.
    IMPRIME EN CONSOLA LA ACCION SI SE EXPORTA CORRECTAMENTE 
    ADEMAS DE MOSTRAR CON UN SHOWINFO UNA VENTANA EMERGENTE 
    CON EL MISMO MENSAJE.
    EN CASO CONTRARIO SE CANCELA Y SE IMPRIME POR CONSOLA
    Y CON UN SHOWERROR PARA MOSTRAR EL MENSAJE DE CANCELACION.
    """


    #imprimo en consola a modo testing para ver si se ejecuta la funcion.
    print("Exportando base...")

    # Pido al usuario que seleccione la ubicación y el nombre del archivo
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])

    #Utilizo una estructura condicional para verificar si el usuario selecciono un archivo para guardar.
    if file_path:
        # si da true entonces Conecto la base de datos
        conexion = sqlite3.connect('basededatos.db')
        cursor = conexion.cursor()

        # Obtengo todos los registros de la tabla materiales
        cursor.execute("SELECT * FROM materiales")
        registros = cursor.fetchall()

        # Cierro la conexión
        conexion.close()

        # Escribo los registros en el archivo de texto seleccionado por el usuario
        with open(file_path, 'w') as file:
            for registro in registros:
                file.write(str(registro) + '\n')
        
        print("Base de datos exportada correctamente.")
        messagebox.showinfo("Exportacion", "La Base de datos fue exportada...")
    else:
        print("Exportación cancelada.")
        showerror("Exportacion", "Exportacion cancelada")


def mostrar_ayuda():
    """
    MUESTRA UN MENSAJE EN UNA VENTANA EMERGENTE CON LAS ISNTRUCCIONES Y DESCRIPCION DEL PROGRAMA
    """

    # Mensaje de ayuda 
    mensaje = """Esta es una aplicación realizada por ELIAS ESCALANTE  que muestra una maquetación básica de una interfaz gráfica utilizando Tkinter. 
    Puedes utilizar esta aplicación para gestionar una base de datos de materiales, donde puedes consultar, dar de alta, borrar y modificar registros.
    Asi como tambien exportar la base de datos actual y exportar las consultas que hagas. 
    Con respecto a la aplicacion podes cambiar a modo oscuro o bien al modo clasico.
    Además tenes acceso a una ventana de salida para visualizar todas las operaciones realizadas. A tener en cuenta:

    1 - para borrar un registro debes realizar un consulta primero luego seleccionarlo en el treeview y luego presionar el boton de borrar.
    2 - para consultar podes buscar por descripcion y luego presionar el boton consultar.
    3 - para modificar debes conocer el numero de material y se debe completar todos los campos del registro. primero realizar una consulta para conocer el numero de material
    4 - para el alta debes completar todos los campos, respetando los criterios de cada uno. Luego presionas el boton de Alta
    5 - para exportar una consulta debes de realizarla primero y luego ir al menu y elegir "exportar consulta".
    6 - para exportar la base solo ve al menu y haz click en "exportar base"

    derechos reservados a:
    Elias Escalante
    deguelelias@gmail.com
    git del proyecto:
    https://github.com/eliasescalante/app_proyecto_final_utn.git
    """
    # Muestro el mensaje de ayuda en una ventana emergente
    messagebox.showinfo("Ayuda", mensaje)


def exportar_consulta():
    """
    EXPORTA LA CONSULTA REALIZADA E IMPRESA EN EL TREEVIEW EN UN ARCHIVO .TXT
    MUESTRA EN UNA VENTANA EMERGENTE SI LA ACCION SI REALIZO CORRECTAMENTE.
    EN CASO QUE NO HAYA UNA CONSULTA REALIZADA PREVIAMENTE MUESTRA 
    UN MENSAJE EN UN SHOWWARNING INDICANDO QUE NO HAY REGISTROS.
    SI SE CANCELA LA OPERACION TAMBIEN SE MUESTRA POR PANTALLA CON UN SHOWWARNING.
    """


    # Verifico si hay registros en el Treeview en caso de que de TRUE emite un mensaje si da FALSE continua
    if not tree.get_children():
        messagebox.showwarning("Exportar consulta", "Debes realizar una consulta primero antes de exportar.")
        return

    # Pido al usuario que seleccione la ubicación y el nombre del archivo con el metodo asksaveasfilename
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])

    # utilizo una estructura condicional if para validar que se haya ingresado  correctamente el nombre del archivo
    if file_path:
        # Obtengo todos los registros mostrados en el Treeview
        registros = []
        for item in tree.get_children():
            registros.append(tree.item(item)['values'])

        if registros:
            # Escribo los registros en el archivo de texto seleccionado por el usuario
            with open(file_path, 'w') as file:
                for registro in registros:
                    file.write(str(registro) + '\n')

            messagebox.showinfo("Exportar consulta", "Consulta exportada correctamente.")
        else:
            messagebox.showwarning("Exportar consulta", "No hay registros para exportar.")
    else:
        messagebox.showwarning("Exportar consulta", "Operación cancelada.")



def alta_registro():
    """
    INGRESA UN NUEVO REGISTRO A LA BASE DE DATOS.
    SI NO SE COMPLETAN TODOS LOS CAMPOS EMITE UN MENSAJE DE ERROR  Y NO GUARDA NINGUN DATO.
    SI SE COMPLETAN TODOS LOS CAMPOS Y SE HACE CLICK 
    EN EL BOTÓN ALTA INSERTA EL REGISTRO EN LA BASE DE DATOS.
    AL DARSE EL ALTA MUESTRA UN MENSAJE DE EXITO E INSERTA EN EL TREEVIEW DICHO REGISTRO
    UTILIZANDO EXPRESIONES REGULARES (REGEX) VALIDO LOS CAMPOS A INGRESAR.
    SI ALGO FALLA EN EL PROCESO DE ALTA EMITE UN MENSAJE 
    DE ERROR Y NO GUARDA NI UNO DE LOS DATOS INTRODUCIDOS.
    """

#TODOS LOS CAMPOS DEBEN SER LLENADOS.
# obtengo la información ingresada por el usuario
    material = material_var.get()
    descripcion = descripcion_var.get()
    precio_venta = precio_venta_var.get()
    precio_costo = precio_costo_var.get()
    stock = stock_var.get()
    proveedor = proveedor_var.get()

    # valido si todos los campos están completos
    if not material or not descripcion or not precio_venta or not precio_costo or not stock or not proveedor:
        messagebox.showerror("Error", "Por favor completa todos los campos")
        return

    #defino los patrones en variables para tipiar menos codigo
    # No utilizo validacion para descripcion porque las diferentes marcas o nombres utilizan cualquier caracter
    patron_precio = "^\d+(\.\d+)?$"
    patron_entero = "^\d+$"

    # valido los campos uno por uno utilizando expresiones regulares pasando como argumentos las variables declaradas anteriormente:
    if not re.match(patron_entero, material):
        showerror("Error", "El material debe ser un número entero.")
        return
    if not descripcion:
        showerror("Error", "La descripción no puede estar vacía.")
        return
    if not re.match(patron_precio, precio_venta):
        showerror("Error", "El precio de venta debe ser un número flotante.")
        return
    if not re.match(patron_precio, precio_costo):
        showerror("Error", "El precio de costo debe ser un número flotante.")
        return
    if not re.match(patron_entero, stock):
        showerror("Error", "El stock debe ser un número entero.")
        return
    if not proveedor:
        showerror("Error", "El proveedor no puede estar vacío.")
        return

    # conecto a la base de datos
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()

    #utilizo el try  except para manejar posibles errores
    try:
        # Inserto el nuevo registro en la tabla materiales
        cursor.execute("INSERT INTO materiales (material, descripcion, precio_venta, precio_costo, stock, proveedor) VALUES (?, ?, ?, ?, ?, ?)",
                    (material, descripcion, precio_venta, precio_costo, stock, proveedor))

        # guardo los cambios
        conexion.commit()

        # muestro el mensaje de éxito
        messagebox.showinfo("Alta de registro", "Registro agregado correctamente.")
        print("Registro agregado correctamente.")

        # obtengo el registro recién insertado
        cursor.execute("SELECT * FROM materiales WHERE material = ?", (material,))
        nuevo_registro = cursor.fetchone()

        # limpio el Treeview
        for record in tree.get_children():
            tree.delete(record)

        # inserto el nuevo registro en el Treeview
        tree.insert('', 'end', values=nuevo_registro)
    # si hay un error se captura en la variable e y se muestra por mensaje en la pantalla
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo agregar el registro: {e}")

    finally:
        # cierro la conexión
        conexion.close()

    # Limpio los campos de entrada después de agregar el registro
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)

def consultar_registro():
    """
    REALIZA UNA CONSULTA  A LA TABLA DE MATERIALES EN LA BASE 
    DE DATOS PARA OBTENER TODOS LOS REGISTROS Y LOS AGREGA AL TREEVIEW
    SI NO SE COMPLETA LOS CAMPOS REQUERIDOS PARA REALIZAR LA CONSULTA 
    EMITE UN MENSAJE EN UN SHOWWARNING PARA QUE SE COMPLETE ALGUN CRITERIO DE BUSQUEDA
    EL CRITERIO DE BUSQUEDA VA A SER LA DESCRIPCION.
    """

    # Obtengo el texto ingresado en el campo de entrada
    descripcion = descripcion_var.get()

    # Conecto la base de datos
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()

    # Realizo la consulta en función del texto ingresado con una estructura condicional elif
    if descripcion:
        cursor.execute("SELECT * FROM materiales WHERE descripcion LIKE ?", ('%' + descripcion + '%',))
    else:
        messagebox.showwarning("Consulta", "Debe ingresar un criterio de búsqueda (Descripción).")
        return

    # Limpio el treeview antes de agregar los nuevos datos
    for record in tree.get_children():
        tree.delete(record)

    #agrego los resultados a la variable registro
    registro =  cursor.fetchall()

    if registro:
        # Inserto los resultados de la consulta en el treeview
        for row in registro:
            tree.insert('', 'end', values=row)
    else:
        messagebox.showinfo("Consulta sin resultados","No se encontraron coincidencias.")

    # Cierro la conexión
    conexion.close()


def borrar_registro():
    """
    BORRA UN REGISTRO DE LA BASE DE DATOS.
    SE DEBE SELECCIONAR EL REGISTRO DESDE EL TREEVIEW Y LUEGO PRESIONAR EL BOTON BORRAR.
    ES NECESARIO REALIZAR UNA CONSULTA PRIMERO. EN CASO DE NO REALIZARLO EMITE UN MENSAJE DE WARNING 
    """

    #  Obtengo el material del registro seleccionado en el treeview
    # Si no se proporciona material emite un mensaje de error
    selection = tree.selection()
    if not selection:
        messagebox.showwarning("Borrar registro", "Selecciona un registro para eliminar.")
        return

    #obtengo el elemento id del registro a borrar que fue seleccionado
    # luego lo guardo en una variable el campo material del registro a borrar
    item = tree.item(selection[0])
    material_a_borrar = item['values'][1]

    # contecto a la base de datos
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()

    try:
        # intento borrar el registro de la base de datos
        cursor.execute("DELETE FROM materiales WHERE material = ?", (material_a_borrar,))
        conexion.commit()

        # Borro el registro del treeview
        for item in tree.selection():
            tree.delete(item)

        messagebox.showinfo("Borrar registro", f"Registro con material '{material_a_borrar}' eliminado correctamente.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo borrar el registro: {e}")
    finally:
        # Cerrar la conexión a la base de datos
        conexion.close()

    # borro los campo de entrada después de borrar el registro
    entry1.delete(0, END)

def modificar_registro():
    """
    MODIFICA UNO O VARIOS CAMPOS DE UN REGISTRO BASANDOSE EN EL NUMERO DE MATERIAL
    SE DEBE COMPLETAR TODOS LOS CAMPOS
    EMITE UN MENSAJE  SI NO SE HA SELECCIONADO NINGUN REGISTRO Y PARA MODIFICAR
    EMITE UN MENSAJE SI SE MODIFICO EL REGISTRO
    EMITE MENSAJE SI OCURRE UN ERROR DEL TIPO NO EXISTE EL REGISTRO O  CAMPOS INCOMPLETOS
    """

    # obtengo el material ingresado por el usuario
    material = material_var.get()

    # obtengo los valores ingresados por el usuario para los otros campos
    descripcion = entry2.get()
    precio_venta = entry3.get()
    precio_costo = entry4.get()
    stock = entry5.get()
    proveedor = entry6.get()

    # valido que se haya ingresado un material
    if not material:
        messagebox.showwarning("Modificar registro", "Debe ingresar el material del registro que desea modificar.")
        return

    # conecto a la base de datos
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()
    print("conectando base de dato...")

    try:
        # verifico si el registro con el material proporcionado existe
        cursor.execute("SELECT * FROM materiales WHERE material = ?", (material,))
        registro = cursor.fetchone()

        if registro:
            # realizo la consulta SQL para actualizar el registro
            sql = "UPDATE materiales SET"
            values = []

            # agrego los campos que se van a modificar
            if descripcion:
                sql += " descripcion = ?,"
                values.append(descripcion)
            if precio_venta:
                sql += " precio_venta = ?,"
                values.append(float(precio_venta))
            if precio_costo:
                sql += " precio_costo = ?,"
                values.append(float(precio_costo))
            if stock:
                sql += " stock = ?,"
                values.append(float(stock))
            if proveedor:
                sql += " proveedor = ?,"
                values.append(proveedor)

            # elimino la última coma y cierro la consulta
            sql = sql.rstrip(',') + " WHERE material = ?"
            values.append(material)

            # ejecuto la consulta para actualizar el registro
            cursor.execute(sql, tuple(values))
            conexion.commit()

            #muestro un mensaje por pantalla si la modificacion del registro se realizo sin problemas
            messagebox.showinfo("Modificar registro", f"Registro con material '{material}' modificado correctamente.")

            # obtengo el registro modificado de la base de datos
            cursor.execute("SELECT * FROM materiales WHERE material = ?", (material,))
            registro_modificado = cursor.fetchone()

            # limpio el Treeview
            for record in tree.get_children():
                tree.delete(record)

            # inserto el registro modificado en el Treeview
            tree.insert('', 'end', values=registro_modificado)
        else:
            messagebox.showerror("Error", f"No se encontró ningún registro para el material '{material}'.")
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo modificar el registro: {e}")
    finally:
        # cierro la conexión
        conexion.close()

    # limpio los campos de entrada después de modificar el registro
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)

def limpiar_tree():
    """
    LIMPIA EL TREEVIEWW DE TODA LA INFO QUE ESTE EN EL MOMENTO
    """

    # Limpio el Treeview utilizando una estructura repetitiva  For que recorre todos los hijos del nodo raiz
    for record in tree.get_children():
        tree.delete(record)

    # limpio los campos de entrada
    entry1.delete(0, END)
    entry2.delete(0, END)
    entry3.delete(0, END)
    entry4.delete(0, END)
    entry5.delete(0, END)
    entry6.delete(0, END)



def modo_oscuro():
    """
    CAMBIA EL FONDO DE LA APLICACION A GRIS
    """
    app.configure(background="grey")


def modo_clasico():
    """
    CAMBIA EL FONDO DE LA APLICACION A BLANCO QUE ES EL MODO ORIGINAL
    """
    app.configure(background="white")



#############################################################################################
# MAQUETACION - arranque de la app contenedor
#############################################################################################
app = Tk()

#VARIABLES
material_var = StringVar(value="0")
descripcion_var = StringVar()
precio_venta_var = StringVar(value="0")
precio_costo_var = StringVar(value="0")
stock_var = StringVar(value="0")
proveedor_var = StringVar()


#############################################################################################
# Incluyo dentro del loop de la app la funcion de crear base de datos
crear_base_datos()
#############################################################################################

# Titulo de la ventana
app.title("POS base de materiales")
# seteo del tamaño de la ventana
app.geometry("1100x400")
#Seteo el fondo de la app
modo_clasico()

#################################################################################################################
# MAQUETACION DEL MENU
# inserto el menu
menubar = Menu(app)
filemenu = Menu(menubar, tearoff=False) # tearoff=False para que no se pueda arrastrar por fuera del menú

# Submenú de "Exportar base"
filemenu.add_command(label="Exportar base", command=exportar_base)
# Submenú de "exportar consulta"
filemenu.add_command(label="Exportar consulta", command=exportar_consulta)
# Submenú de "tema"
tema_menu = Menu(filemenu, tearoff=False)
# Submenu modo oscuro
tema_menu.add_command(label="Modo Oscuro", command=modo_oscuro)
#submenu modo clasico
tema_menu.add_command(label="Modo Clásico", command=modo_clasico)
#agrego los elementos  al submenu "Tema" y lo agrego a mi barra de menus
filemenu.add_cascade(label="Tema", menu=tema_menu)

# Ítem "Salir"
filemenu.add_command(label="Salir", command=app.quit)

# Agrego el menú "Archivo" al menú principal
menubar.add_cascade(label="Archivo", menu=filemenu)

# Menú de ayuda
helpmenu = Menu(menubar, tearoff=False)
helpmenu.add_command(label="Guia", command=mostrar_ayuda)

# Agrego el menú "Ayuda" al menú principal
menubar.add_cascade(label="Ayuda", menu=helpmenu)

# Configuro la barra de menú
app.config(menu=menubar)


#################################################################################################################  
# MAQUETACION DE LOS WIDGET

# Creo y coloco los widgets Entry y Label uno por uno
#MATERIAL
label1 = Label(app, text="MATERIAL", background="white")
label1.place(x=260, y=20)
entry1 = Entry(app, textvariable=material_var)
entry1.place(x=400, y=20)

#DESCRIPCION
label2 = Label(app, text="DESCRIPCION", background="white")
label2.place(x=260, y=50)
entry2 = Entry(app ,textvariable=descripcion_var)
entry2.place(x=400, y=50)

#PRECIO DE VENTA
label3 = Label(app, text="PRECIO DE VENTA", background="white")
label3.place(x=260, y=80)
entry3 = Entry(app, width=10, textvariable=precio_venta_var)
entry3.place(x=400, y=80)

#PRECIOS DE COSTO
label4 = Label(app, text="PRECIO DE COSTO", background="white")
label4.place(x=260, y=110)
entry4 = Entry(app, width=10,textvariable=precio_costo_var)
entry4.place(x=400, y=110)

#STOCK
label5 = Label(app, text="STOCK", background="white")
label5.place(x=260, y=140)
entry5 = Entry(app, width=10,textvariable=stock_var)
entry5.place(x=400, y=140)

#PROVEEDOR
label6 = Label(app, text="PROVEEDOR", background="white")
label6.place(x=260, y=170)
entry6 = Entry(app, textvariable=proveedor_var)
entry6.place(x=400, y=170)


####################################################################################################################################
# BOTONES

# variables con las dimensiones para simplificar la edicion de los tamaños
button_width = 10
button_height = 1

# boton Consultar
button1 = Button(app, text="Consultar",width=button_width, height=button_height , background="white",command=consultar_registro)
button1.place(x=200, y=200)

#boton alta
button2 = Button(app, text="Alta", width=button_width, height=button_height, background="white" ,command=alta_registro)
button2.place(x=300, y=200)

#boton borrar
button3 = Button(app, text="Borrar", width=button_width, height=button_height, background="white" ,command=borrar_registro)
button3.place(x=400, y=200)

#boton modificar
button4 = Button(app, text="Modificar", width=button_width, height=button_height, background="white" ,command=modificar_registro)
button4.place(x=500, y=200)

#boton limpiar
button5 = Button(app, text="Limpiar", width=button_width, height=button_height, background="white" ,command=limpiar_tree)
button5.place(x=600, y=200)


######################################################################################

# TREEVIEW
# donde se va a mostrar la previsualizacion de los datos
tree = ttk.Treeview(app)

# Columnas del Treeview
tree["columns"] = ("0","1", "2", "3", "4", "5", "6")
tree.column("0", width=50, anchor=W)
tree.column("1", width=150, minwidth=150)
tree.column("2", width=150, minwidth=150)
tree.column("3", width=150, minwidth=150)
tree.column("4", width=150, minwidth=150)
tree.column("5", width=150, minwidth=150)
tree.column("6", width=150, minwidth=150)

# Encabezados del Treeview
tree.heading("0", text="ID")
tree.heading("1", text="MATERIAL", anchor=W)
tree.heading("2", text="DESCRIPCION", anchor=W)
tree.heading("3", text="PRECIO DE VENTA", anchor=W)
tree.heading("4", text="PRECIO DE COSTO", anchor=W)
tree.heading("5", text="STOCK", anchor=W)
tree.heading("6", text="PROVEEDOR", anchor=W)
tree.place(relx=0.5, y=480, anchor=S, relwidth=1)

#############################################################################################
#IMAGENES

# cargo la imagen y la agrego a una etiqueta
image = Image.open("1.JPG")
image = image.resize((200, 150))
photo = ImageTk.PhotoImage(image)
image_label = Label(app, image=photo)
image_label.image = photo 
image_label.place(x=580, y=25)

# cargo el logo en cada label
#label 1
image = Image.open("1.JPG")
image = image.resize((20, 20))
photo = ImageTk.PhotoImage(image)
image_label = Label(app, image=photo)
image_label.image = photo  
image_label.place(x=220, y=20)

# label 2
image = Image.open("1.JPG")
image = image.resize((20, 20))
photo = ImageTk.PhotoImage(image)
image_label = Label(app, image=photo)
image_label.image = photo 
image_label.place(x=220, y=50)

# label 3
image = Image.open("1.JPG")
image = image.resize((20, 20))
photo = ImageTk.PhotoImage(image)
image_label = Label(app, image=photo)
image_label.image = photo  
image_label.place(x=220, y=80)

# label 4
image = Image.open("1.JPG")
image = image.resize((20, 20))
photo = ImageTk.PhotoImage(image)
image_label = Label(app, image=photo)
image_label.image = photo  
image_label.place(x=220, y=110)

# label 5
image = Image.open("1.JPG")
image = image.resize((20, 20))
photo = ImageTk.PhotoImage(image)
image_label = Label(app, image=photo)
image_label.image = photo  
image_label.place(x=220, y=140)

# label 6
image = Image.open("1.JPG")
image = image.resize((20, 20))
photo = ImageTk.PhotoImage(image)
image_label = Label(app, image=photo)
image_label.image = photo  
image_label.place(x=220, y=170)

# cierre de la app
app.mainloop()
