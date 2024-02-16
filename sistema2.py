from tkinter import *
from tkinter import messagebox, ttk, Label
import tkinter as tk
import sqlite3
import time
from docx import Document
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from time import strftime


#COLORES
colorVerde = "#92C463"
colorVerde2 = "#77AB47"
colorGris = "#A0A0A0"
colorGris2 = "#50514E"
colorBase = "#FBFAF7"
colorBase2 = "#EEEDEB"
#conexion 
conexion = sqlite3.connect("finalprog.db")
conexion.row_factory=sqlite3.Row
tabla=conexion.cursor

#ventana
ventana = Tk()
ventana.title("Sistema Ventas")
ventana.config(bg=colorBase2)
ventana.geometry("800x500")
ventana.resizable(0,0)
#frames
frame1 = Frame(ventana,bg=colorGris)
frame1.pack(side=TOP,fill=X,ipady=10)
frameBotones = Frame(ventana, bg=colorVerde)
frameBotones.pack(side=LEFT,fill=Y)
frameBase = Frame(ventana, bg=colorBase2)
frameBase.pack(fill=BOTH,expand=1)

frameInicio = Frame(frameBase,bg=colorBase)
frameInicio.pack(fill=BOTH,expand=1)
frameVentas = Frame(frameBase,bg=colorBase)
frameVentas.pack(fill=BOTH,expand=1)
frameCambios = Frame(frameBase,bg=colorBase)
frameCambios.pack(fill=BOTH,expand=1)
frameLista = Frame(frameBase,bg=colorBase)
frameLista.pack(fill=BOTH,expand=1)

#BORRAR FRAMES
def limpiarFrames():
    frameInicio.pack_forget()
    frameVentas.pack_forget()
    frameCambios.pack_forget()
    frameLista.pack_forget()
###INICIO### 
def verInicio():
    limpiarFrames()
    frameInicio.pack(fill=BOTH,expand=1)
    #reloj
    def reloj():
        hora = strftime('%H:%M:%S')
        dia = strftime('%A')
        fecha = strftime('%d - %m - %y')
        if dia =='Monday':
            dia = 'Lunes'
        elif dia =='Tuesday':
            dia = 'Martes'
        elif dia =='Wednesday':
            dia = 'Miercoles'
        elif dia =='Thursday':
            dia = 'Jueves'
        elif dia =='Friday':
            dia = 'Viernes'
        elif dia =='Saturday':
            dia = 'Sábado'
        elif dia =='Sunday':
            dia = 'Domingo'
        labelHora.config(text=hora)
        labelDia.config(text=dia)
        labelFecha.config(text=fecha)
        labelHora.after(1000,reloj)
    labelHora = Label(frameInicio, font=("DS-Digital",70),
                          bg=colorBase, fg=colorVerde2)
    labelHora.place(x=220, y=5)
    labelDia = Label(frameInicio, font=("Calibri",30),
                          bg=colorBase, fg=colorGris2)
    labelDia.place(x=310, y=90)
    labelFecha = Label(frameInicio, font=("Calibri",20),
                          bg=colorBase, fg=colorGris2)
    labelFecha.place(x=300, y=138)
    reloj()
verInicio()
###VENTA### 
def verVentas():
    limpiarFrames()
    frameVentas.pack(fill=BOTH,expand=1)
    def venta():
        #frames
        frameArticulos = Frame(frameVentas,bg=colorBase)
        frameArticulos.place(x=0,y=0)
        frameCarrito = Frame(frameVentas,bg=colorBase2)
        frameCarrito.place(x=400,y=0)
        frameCarrito.config(width=400,height=500)
        frameArticulos.config(width=400,height=500)
        #litbox
        listaArticulos = Listbox(frameArticulos,font=("Microsoft New Tai Lue",12),
                                 width=42,height=17)
        listaArticulos.place(x=10,y=34)
        listaCarrito = Listbox(frameCarrito, font=("Microsoft New Tai Lue",12),
                               width=35,height=17)
        listaCarrito.place(x=5,y=34)
        #label
        labelCarrito = Label(frameCarrito,text="Carrito",
                            font=("Swis721 BT",15),fg=colorVerde2)
        labelCarrito.place(x=150,y=1)
        labelArticulos = Label(frameArticulos,text="Articulos",
                               font=("Swis721 BT",15),fg=colorVerde2,bg=colorBase)
        labelArticulos.place(x=160,y=1)
        #conexion base de datos
        tabla = conexion.cursor()
        tabla.execute("SELECT tipo, precio FROM articulos")
        conexion.commit()
        datos = tabla.fetchall()
        tabla.close()
        listaArticulos.delete(0,END)
        for dato in datos:
            listaArticulos.insert(END,str(dato[0])+"              "+str(dato[1]))
        #funciones para botones
        def seleccionarProducto():
            seleccionar = listaArticulos.curselection()
            if seleccionar:
                articulo = listaArticulos.get(seleccionar)
                listaCarrito.insert(tk.END,articulo)
        def sacarArticulo():
            seleccionar = listaCarrito.curselection()
            if seleccionar:
                listaCarrito.delete(seleccionar)
        ##TICKET##
        def ticket():
            horaActual = time.strftime("%H%M%S")
            fechaActual = time.strftime("%d%m%Y")
            fechaHoy = time.strftime("%d/%m/%Y")
            nombreArchivo = f"ticket{fechaActual}{horaActual}.pdf"
            nuevoPdf = canvas.Canvas(nombreArchivo,pagesize = A4)
            #print(nuevoPdf.getAvailableFonts())
            ##Lineas X 
            nuevoPdf.line(20, 820, 570, 820)
            nuevoPdf.line(20, 20, 570, 20)
            nuevoPdf.line(20, 720, 570, 720)
            #Lineas Y
            nuevoPdf.line(20, 20, 20, 820)
            nuevoPdf.line(570, 20, 570, 820)
            nuevoPdf.line(480, 720, 480, 820)
            #conexion tabla para el ticket
            tabla = conexion.cursor()
            tabla.execute("SELECT tipo,precio FROM articulos")
            conexion.commit()
            conexion.close()
            #que imprima los productos del carrito 
            articulosSeleccionados = listaCarrito.get(0,tk.END)
            nuevoPdf.setFont("Times-Roman", 20)
            nuevoPdf.drawString(50,780, "Ticket")
            nuevoPdf.setFont("Times-Roman", 20)
            nuevoPdf.drawString(350, 780, fechaHoy)
            nuevoPdf.drawString(100, 650, "Productos:")
            imagenLogo = "imagenes/sublime.jpg"  
            nuevoPdf.drawImage(imagenLogo,485, 730, width=80, height=80)
            yArticulos = 600
            #suma de los precios
            totalPrecio = 0
            for articulo in articulosSeleccionados:
                nuevoPdf.drawString(100, yArticulos, articulo)
                yArticulos -= 30
                precio = float(articulo.split()[-1]) #split para tomar el precio en cadena
                totalPrecio += precio
            #posicion del total
            nuevoPdf.setFont("Times-Roman", 20)
            nuevoPdf.drawString(400,100, "Total: $" + str(totalPrecio))
            nuevoPdf.save()
            listaCarrito.delete(0,tk.END)
            messagebox.showinfo("Venta realizada", "La venta se ha realizado correctamente.")
        #botones
        botonAgregarCarrito = Button(frameArticulos,text="Agregar Producto al Carrito",
                                     font=("Microsoft New Tai Lue",12),bg=colorGris,
                                     fg=colorBase2,command=seleccionarProducto)
        botonAgregarCarrito.place(x=100,y=420)
        botonEliminarCarrito = Button(frameCarrito,text="Sacar del Carrito",
                                      font=("Microsoft New Tai Lue",12),fg=colorBase,bg=colorVerde,
                                      command=sacarArticulo)
        botonEliminarCarrito.place(x=160,y=420)
        botonVender = Button(frameCarrito,text="Vender",
                             font=("Microsoft New Tai Lue",12), fg=colorBase,bg=colorVerde,
                             width=10,command=ticket)
        botonVender.place(x=40,y=420)
        
    venta()
###CAMBIOS### 
def verCambios():
    limpiarFrames()
    frameCambios.pack(fill=BOTH,expand=1)
    def cambios():
        #entrys y labels
        entryBuscador = Entry(frameCambios,font=("Swis721 BT",12),
                            bg=colorBase2, fg=colorVerde2,
                            width=50)
        
        labelCodigo = Label(frameCambios, 
                        text="Codigo",font=("Swis721 BT",12),
                        bg=colorBase,fg=colorGris2)
        entryCodigo = Entry(frameCambios,
                             font=("Swis721 BT",12),width=10,
                            bg=colorGris,fg=colorBase)

        labelTipo = Label(frameCambios, 
                        text="Tipo",font=("Swis721 BT",12),
                        bg=colorBase,fg=colorGris2)
        entryTipo = Entry(frameCambios, font=("Swis721 BT",12),
                bg=colorBase, fg=colorVerde2,width=30)

        labelPrecio = Label(frameCambios, 
                        text="Precio",font=("Swis721 BT",12),
                        bg=colorBase,fg=colorGris2)
        entryPrecio = Entry(frameCambios, font=("Swis721 BT",12),
                bg=colorBase, fg=colorVerde2,width=15)

        labelStock = Label(frameCambios, 
                        text="Stock",font=("Swis721 BT",12),
                        bg=colorBase,fg=colorGris2)
        entryStock = Entry(frameCambios, font=("Swis721 BT",12),
                bg=colorBase, fg=colorVerde2,width=15)
        #posicion
        entryBuscador.place(x=15,y=60)
        labelCodigo.place(x=25,y=150)
        entryCodigo.place(x=10,y=180)
        labelTipo.place(x=240,y=150)
        entryTipo.place(x=120,y=180)
        labelPrecio.place(x=453,y=150)
        entryPrecio.place(x=410,y=180)
        labelStock.place(x=610,y=150)
        entryStock.place(x=565,y=180)
       # BOTONES Y FUNCIONES
        def buscar():
            if(entryBuscador.get() != ""):
                datoBuscar = (entryBuscador.get(),)
                tabla=conexion.cursor()
                tabla.execute("SELECT * FROM articulos WHERE tipo=?",(datoBuscar))
                datosBuscados = tabla.fetchall()
                tabla.close()
                entryTipo.delete(0,END)
                entryPrecio.delete(0,END)
                entryStock.delete(0,END)
                entryCodigo.delete(0,END)
                entryBuscador.delete(0,END)
            else:
                messagebox.showerror("ERROR", "Producto no encontrado.")

            for fila in datosBuscados:
                entryCodigo.insert(END,fila[0])
                entryTipo.insert(END,fila[1])
                entryPrecio.insert(END,fila[2])
                entryStock.insert(END,fila[3])
        botonBuscar = Button(frameCambios, text="Buscar",
                             command=buscar, font=("Swis721 BT",11),
                             bg=colorVerde2, fg=colorBase2,
                             relief="ridge",width=25)
        botonBuscar.place(x=480,y=55)
        def guardar():
            datos = (entryTipo.get(),
                     entryPrecio.get(),
                     entryStock.get(),)
            tabla = conexion.cursor()
            tabla.execute("INSERT INTO articulos(tipo, precio, stock) VALUES(?,?,?)",datos)
            conexion.commit()
            tabla.close()
            messagebox.showinfo("Sistema Ventas", "Articulo  guardado correctamente.")
            #borrar texto
            entryTipo.delete(0,END)
            entryPrecio.delete(0,END)
            entryStock.delete(0,END)
        botonGuardar = Button(frameCambios, text="Guardar",
                             command=guardar, font=("Swis721 BT",11),
                             bg=colorVerde2, fg=colorBase2,
                             relief="ridge",width=24)
        botonGuardar.place(x=20,y=300)
        def modificar():
            #no entradas vacias otra vez
            if(entryTipo.get() == "" or
               entryPrecio.get() == "" or
               entryStock.get() == ""):
                messagebox.showwarning("Sistema Ventas",
                                        "Complete todos los campos")
            else:
                datos = (entryTipo.get(),
                         entryPrecio.get(),
                         entryStock.get(),
                         entryCodigo.get())
                tabla = conexion.cursor()
                tabla.execute("UPDATE articulos SET tipo=?, precio=?, stock=? WHERE codigo=?",
                              datos)
                conexion.commit()
                tabla.close()
                messagebox.showinfo("Sistema Ventas","El articulo se ha modificado correctamente")
                entryTipo.delete(0,END)
                entryPrecio.delete(0,END)
                entryStock.delete(0,END)
                entryCodigo.delete(0,END)
                entryBuscador.delete(0,END)
        botonModificar = Button(frameCambios, text="Modificar",
                             command=modificar, font=("Swis721 BT",11),
                             bg=colorVerde2, fg=colorBase2,
                             relief="ridge",width=24)
        botonModificar.place(x=255,y=300)
        def eliminar():
            eliminarProductos = messagebox.askquestion("Sistema Ventas","Seguro que desea eliminar?")
            if(eliminarProductos == "yes"):
                tabla = conexion.cursor()
                datosEliminar = (entryCodigo.get(),)
                tabla.execute("DELETE FROM articulos WHERE codigo=?",datosEliminar)
                conexion.commit()
                tabla.close()
                entryCodigo.delete(0,END)
                entryTipo.delete(0,END)
                entryPrecio.delete(0,END)
                entryStock.delete(0,END)
                messagebox.showinfo("Sistema Ventas", "El articulo se ha eliminado correctamente")
        botonEliminar = Button(frameCambios, text="Eliminar",
                             command=eliminar, font=("Swis721 BT",11),
                             bg=colorVerde2, fg=colorBase2,
                             relief="ridge",width=24)
        botonEliminar.place(x=490,y=300)           
    cambios()
###LISTA###  
def verLista():
    limpiarFrames()
    frameLista.pack(fill=BOTH,expand=1)
    #LISTA PRINCIPAL
    def lista():
        #treeview?
        listaArticulos = ttk.Treeview(frameLista)
        listaArticulos.place(x=10,y=10,width=600,height=400)
        
        listaArticulos["columns"] = ("tipo","precio","stock")
        listaArticulos.column("#0",width=0)
        listaArticulos.column("tipo",width=300)
        listaArticulos.column("precio",width=100)
        listaArticulos.column("stock",width=100)

        listaArticulos.heading("#0")
        listaArticulos.heading("tipo",text="Tipo de Producto")
        listaArticulos.heading("precio",text="Precio de Venta")
        listaArticulos.heading("stock",text="Stock Disponible")
        #LISTA SECUNDARIA
        def listaVentana2():
            #otra ventana
            lista2 = Toplevel()
            lista2.title("Lista de Articulos")
            lista2.geometry("700x800")
            lista2.config(bg=colorBase2)
            lista2.resizable(0,0)
            listaArticulos = ttk.Treeview(lista2)
            
            listaArticulos["columns"] = ("tipo","precio","stock")
            listaArticulos.column("#0",width=0)
            listaArticulos.column("tipo",width=300)
            listaArticulos.column("precio",width=100)
            listaArticulos.column("stock",width=100)

            listaArticulos.heading("#0")
            listaArticulos.heading("tipo",text="Tipo de Producto")
            listaArticulos.heading("precio",text="Precio de Venta")
            listaArticulos.heading("stock",text="Stock Disponible")
            #conexion a la otra ventana
            def conexionBD():
                conexion = sqlite3.connect("finalprog.db")
                tabla = conexion.cursor()
                tabla.execute("SELECT tipo, precio, stock FROM articulos")
                datos = tabla.fetchall()
                tabla.close()
                conexion.close()
                return datos
            datos = conexionBD()
            for dato in datos:
                listaArticulos.insert("","end",values=(dato[0],dato[1],dato[2]))
            listaArticulos.place(x=10,y=10,width=680,height=780)
        #boton lista 2
        botonLista2 = Button(frameLista,font=("Swis721 BT",12),
                             bg=colorGris,fg=colorVerde,text="Lista",
                             command=listaVentana2,width=10)
        botonLista2.place(x=620,y=20)
        #conexion 1
        def conexionBD():
            conexion = sqlite3.connect("finalprog.db")
            tabla = conexion.cursor()
            tabla.execute("SELECT tipo, precio, stock FROM articulos")
            datos = tabla.fetchall()
            tabla.close()
            conexion.close()
            return datos
        datos = conexionBD()
        for dato in datos:
            listaArticulos.insert("","end",values=(dato[0],dato[1],dato[2]))
        listaArticulos.place(x=10,y=10,width=600,height=400)
    lista()

#BOTONES PRINCIPALES
imagenGuardar1 = PhotoImage(file="imagenes/inicio3.png")
botonInicio = Button(frameBotones, bg=colorVerde,text="Inicio",
                     command=verInicio
                     ,image=imagenGuardar1)
botonInicio.pack(side=TOP)
imagenGuardar2 = PhotoImage(file="imagenes/ventas3.png")
botonVentas = Button(frameBotones, bg=colorVerde,text="Ventas",
                     command=verVentas
                     ,image=imagenGuardar2)
botonVentas.pack(side=TOP)
imagenGuardar3 = PhotoImage(file="imagenes/cambios3.png")
botonCambios = Button(frameBotones, bg=colorVerde,text="Cambios",
                      command=verCambios
                      ,image=imagenGuardar3)
botonCambios.pack(side=TOP)
imagenGuardar4 = PhotoImage(file="imagenes/lista3.png")
botonLista = Button(frameBotones, bg=colorVerde,text="Lista",
                    command=verLista
                    ,image=imagenGuardar4)
botonLista.pack(side=TOP)


ventana.mainloop()
