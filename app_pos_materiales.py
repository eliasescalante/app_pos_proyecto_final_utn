from tkinter import *
from tkinter import ttk, filedialog
import sqlite3
import os
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk

"""
DEV = Elias Escalante
    App proyecto final API, practica con Tkinter.
    Aplicacion de escritorio que permite realizar un CRUD  en una base de datos SQLITE.
    Se puede agregar, eliminar o editar registros a la tabla "productos".
    Tambien permite exportar la base de datos en .txt asi como también la consulta.
    Tambien se puede cambiar el color de fondo de la aplicacion con el modo oscuro y volver a su modo clásico
    Intente realizar una interfaz intuitiva y facil de usar.
"""



#############################################################################################
# FUNCIONES
#############################################################################################

def crear_base_datos():
    # CREA LA BASE DE DATOS EN DONDE SE VA ALOJAR LA INFORMACION DE LOS MATERIALES

    #genero un print si ya existe la base con utilizo una estructura condicional
    if os.path.exists('basededatos.db'):
        print("la base ya existe")
        return
    
    # Conecto a la base de datos (si no existe, se crea)
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()

    # Creo tabla si no existe dentro de la base de datos
    cursor.execute('''CREATE TABLE IF NOT EXISTS materiales (
                        id INTEGER PRIMARY KEY,
                        material TEXT NOT NULL,
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
    # EXPORTA TODA LA BASE DE DATOS A UN ARCHIVO .TXT Y DEJA ELEGIR DONDE GUARDARLO

    #imprimo en consola a modo testing para ver si se ejecuta la funcion.
    print("Exportando base...")

    # Pido al usuario que seleccione la ubicación y el nombre del archivo
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
    
    #Utilizo una estructura condicional para verificar si el usuario selecciono un archivo para guardar.
    if file_path:
        # Conecto a la base de datos
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
    else:
        print("Exportación cancelada.")


def mostrar_ayuda():
    #MUESTRA UN MENSAJE EN UNA VENTANA EMERGENTE CON LAS ISNTRUCCIONES Y DESCRIPCION DEL PROGRAMA

    # Mensaje de ayuda 
    mensaje = """Esta es una aplicación realizada por ELIAS ESCALANTE  que muestra una maquetación básica de una interfaz gráfica utilizando Tkinter. 
    Puedes utilizar esta aplicación para gestionar una base de datos de materiales, donde puedes consultar, dar de alta, borrar y modificar registros.
    Asi como tambien exportar la base de datos actual y exportar las consultas que hagas. 
    Con respecto a la aplicacion podes cambiar a modo oscuro o bien al modo clasico.
    Además tenes acceso a una ventana de salida para visualizar todas las operaciones realizadas que son :

    1 - para borrar un registro debes conocer el numero de material por eso debes realizar un consulta primero para conocerlo y despues borrarlo
    2 - para consultar podes buscar o por material o por descripcion
    3 - para modificar debes conocer el numero de material y se debe completar todos los campos del registro. primero realizar una consulta
    4 - para el alta debes completar todos los campos.
    5 - para exportar una consulta debes de realizarla primero

    derechos reservados a:
    Elias Escalante
    deguelelias@gmail.com
    """
    # Muestro el mensaje de ayuda en una ventana emergente
    messagebox.showinfo("Ayuda", mensaje)

# funcion para que no detone los botones
def exportar_consulta():
    #EN BASE A UNA CONSULTA REALIZADA PREVIAMENTE ESTA FUNCION EXPORTA DICHA CONSULTA EN UN .TXT

    # Verifico si hay registros en el Treeview en caso que de true emite un mensaje si false continua
    if not tree.get_children():
        messagebox.showwarning("Exportar consulta", "Debes realizar una consulta primero antes de exportar.")
        return

    # Pido al usuario que seleccione la ubicación y el nombre del archivo con el metodo asksaveasfilename
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])

    
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
#INGRESA UN NUEVO REGISTRO A LA BASE DATOS
#TODOS LOS CAMPOS DEBEN SER LLENADOS.

    # capturo la información ingresada por el usuario
    material = entry1.get()
    descripcion = entry2.get()
    precio_venta = float(entry3.get())
    precio_costo = float(entry4.get())
    stock = int(entry5.get())
    proveedor = entry6.get()

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
    #REALIZA UNA CONSULTA  A LA TABLA MATERIALES PARA OBTENER TODOS LOS REGISTROS Y LOS AGREGA AL TREEVIEW

    # Obtengo el texto ingresado en los campos de entrada
    material = entry1.get()
    descripcion = entry2.get()

    # Conecto a la base de datos
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()

    # Realizo la consulta en función del texto ingresado
    if material:
        cursor.execute("SELECT * FROM materiales WHERE material LIKE ?", ('%' + material + '%',))
    elif descripcion:
        cursor.execute("SELECT * FROM materiales WHERE descripcion LIKE ?", ('%' + descripcion + '%',))
    else:
        messagebox.showwarning("Consulta", "Debe ingresar al menos un criterio de búsqueda (Material o Descripción).")
        return

    # Limpio el treeview antes de agregar nuevos datos
    for record in tree.get_children():
        tree.delete(record)

    # Inserto los resultados de la consulta en el treeview
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

    # Cierro la conexión
    conexion.close()

def borrar_registro():
    #BORRA UN REGISTRO DE LA BASE DE DATOS A PARTIR DE SU NUMERO DE MATERIAL INGRESADO

    # obtengo el material ingresado por el usuario
    material = entry1.get()

    # valido que se haya ingresado un material
    if not material:
        messagebox.showwarning("Borrar registro", "Debe ingresar el material del registro que desea borrar.")
        return

    # conecto la base de datos
    conexion = sqlite3.connect('basededatos.db')
    cursor = conexion.cursor()

    try:
        # intento borrar el registro con el material proporcionado
        cursor.execute("DELETE FROM materiales WHERE material = ?", (material,))
        conexion.commit()
        messagebox.showinfo("Borrar registro", f"Registro con material '{material}' eliminado correctamente.")
    except sqlite3.Error as e:
        # muestro un mensaje en caso de error
        messagebox.showerror("Error", f"No se pudo borrar el registro: {e}")
    finally:
        # cierro la conexión
        conexion.close()

    # borro los campo de entrada después de borrar el registro
    entry1.delete(0, END)

def modificar_registro():
    # MODIFICA UNO O VARIOS CAMPOS DE UN REGISTRO BASANDOSE EN EL NUMERO DE MATERIAL

    # obtengo el material ingresado por el usuario
    material = entry1.get()

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


def modo_oscuro():
    #CAMBIA EL FONDO DE LA APLICACION A GRIS
    app.configure(background="grey")


def modo_clasico():
    #CAMBIA EL FONDO DE LA APLICACION A SU COLOR ORIGINAL
    app.configure(background="white")

#############################################################################################
# MAQUETACION - arranque de la app contenedor
#############################################################################################
app = Tk()

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

# Añadir el menú "Archivo" al menú principal
menubar.add_cascade(label="Archivo", menu=filemenu)

# Menú de ayuda
helpmenu = Menu(menubar, tearoff=False)
helpmenu.add_command(label="Ayuda", command=mostrar_ayuda)

# Añadir el menú "Ayuda" al menú principal
menubar.add_cascade(label="Ayuda", menu=helpmenu)

# Configurar la barra de menú
app.config(menu=menubar)

#################################################################################################################
# MAQUETACION DE LOS WIDGET

# Creo y coloco los widgets Entry y Label uno por uno
label1 = Label(app, text="MATERIAL", background="white")
label1.place(x=260, y=20)

entry1 = Entry(app)
entry1.place(x=400, y=20)

label2 = Label(app, text="DESCRIPCION", background="white")
label2.place(x=260, y=50)

entry2 = Entry(app)
entry2.place(x=400, y=50)

label3 = Label(app, text="PRECIO DE VENTA", background="white")
label3.place(x=260, y=80)


entry3 = Entry(app, width=10)
entry3.place(x=400, y=80)
entry3.insert(0, "0.0")

label4 = Label(app, text="PRECIO DE COSTO", background="white")
label4.place(x=260, y=110)

entry4 = Entry(app, width=10)
entry4.place(x=400, y=110)
entry4.insert(0, "0.0")

label5 = Label(app, text="STOCK", background="white")
label5.place(x=260, y=140)

entry5 = Entry(app, width=10)
entry5.place(x=400, y=140)
entry5.insert(0, "0.0")

label6 = Label(app, text="PROVEEDOR", background="white")
label6.place(x=260, y=170)

entry6 = Entry(app)
entry6.place(x=400, y=170)

####################################################################################################################################
# BOTONES

# variables con las dimensiones
button_width = 10
button_height = 1

# botones
button1 = Button(app, text="Consultar",width=button_width, height=button_height , background="white",command=consultar_registro)
button1.place(x=200, y=200)

button2 = Button(app, text="Alta", width=button_width, height=button_height, background="white" ,command=alta_registro)
button2.place(x=300, y=200)

button3 = Button(app, text="Borrar", width=button_width, height=button_height, background="white" ,command=borrar_registro)
button3.place(x=400, y=200)

button4 = Button(app, text="Modificar", width=button_width, height=button_height, background="white" ,command=modificar_registro)
button4.place(x=500, y=200)

######################################################################################################################################
# TREEVIEW
# donde se va a mostrar la previsualizacion de los datos
tree = ttk.Treeview(app)
tree["columns"] = ("#0", "1", "2", "3", "4", "5", "6")
tree.column("#0", width=10, minwidth=150)  # Ajusté el ancho de las columnas
tree.column("1", width=150, minwidth=150)
tree.column("2", width=150, minwidth=150)
tree.column("3", width=150, minwidth=150)
tree.column("4", width=150, minwidth=150)
tree.column("5", width=150, minwidth=150)
tree.column("6", width=150, minwidth=150)
tree.heading("#0", text="ID", anchor=W)  # Cambié el texto de las cabeceras
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
