# -*- coding: utf-8 -*-
"""
Created on Sun Aug  8 15:14:53 2021

@author: donat
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import pickle
import os
from tkinter import ttk
from tkinter import filedialog
from tkinter import *
from tkinter import messagebox
from datetime import datetime
from tkinter import filedialog
import functools
from pandastable import Table, TableModel
from PIL import ImageTk,Image
print('Iniciando Super Programa Gestion v1')
print('Carpeta de trabajo:',os.getcwd())
path_Productos='Bases de datos/Productos.csv'
path_Ventas='Bases de datos/Ventas.csv'
path_Despachos='Bases de datos/Despachos.csv'
path_Lista_Ventas = "Bases de datos/ListaVentas.pkl"
path_Ofertas="Bases de datos/Ofertas.pkl"
path_Lista_Eventos="Bases de datos/ListaEventos.csv"
path_Eventos="Bases de datos/Events.pkl"
####Hay que definir los siguientes eventos
#1 Creacion de producto.
#2 Creacion de oferta.
#3 Modificación de producto.
#4 Modificación de oferta.
#5 Creación de una venta.
#6 Eliminación de una venta.
#7 Generacion guia de despachos.
class Evento:
    """
    Cada evento tiene asociado un tipo que pueden ser
    1 Creacion de producto.
    2 Creacion de oferta.
    3 Modificación de producto.
    4 Modificación de oferta.
    5 Creación de una venta.
    6 Eliminación de una venta.
    """
    def __init__(self,tipo,id_evento,fecha):
        self.tipo=tipo
        self.id_evento=id_evento
        self.fecha=fecha
class EventoProducto(Evento):
    def __init__(self,tipo,id_evento,fecha,id_prod,precio_old=None,precio_new=None,
                 cantidad_old=None,cantidad_new=None):
        super().__init__(tipo,id_evento,fecha)
        self.precio_old=precio_old
        self.precio_new=precio_new
        self.cantidad_old=cantidad_old
        self.cantidad_new=cantidad_new
        self.id_prod=id_prod
class EventoOferta(Evento):
    def __init__(self,tipo,id_evento,fecha,id_prod,nombre_old=None,nombre_new=None):
        super().__init__(tipo,id_evento,fecha)
        self.nombre_old=nombre_old
        self.nombre_new=nombre_new
        self.id_prod=id_prod
class EventoVenta(Evento):
    def __init__(self,tipo,id_evento,fecha,id_venta):
        super().__init__(tipo,id_evento,fecha)
        self.id_venta=id_venta

try:
    ListaEventos=pd.read_csv(path_Lista_Eventos, encoding='utf-8')
    ListaEventos.set_index('ID_EVENTO',inplace=True)
except:
    print('No se encontro base de datos de Lista eventos.')
    ListaEventos=pd.DataFrame(columns=['ID_EVENTO','FECHA','TIPO'])
    ListaEventos.set_index('ID_EVENTO',inplace=True)
    ListaEventos.to_csv(path_Lista_Eventos, encoding='utf-8')
    
if os.path.exists(path_Eventos):
    with open(path_Eventos, 'rb') as file:
        Eventos=pickle.load(file)
else:
    print('Listas de ventas no existen.')
    with open(path_Eventos, 'wb') as file:
        Eventos={}
        pickle.dump(Eventos, file)
try:
    Productos=pd.read_csv(path_Productos, encoding='utf-8')
    Productos.set_index('ID_PROD',inplace=True)
except:
    print('No se encontro base de datos de Productos.')
    Productos=pd.DataFrame(columns=['PRODUCTO','ID_PROD','DESCRIPCIÓN','CANTIDAD_DISPONIBLE','PRECIO'])
    Productos.set_index('ID_PROD',inplace=True)
    Productos.to_csv(path_Productos, encoding='utf-8')
try:
    Ventas=pd.read_csv(path_Ventas, encoding='utf-8')
    Ventas.set_index('ID_VENTA',inplace=True)
except:
    print('No se encontro base de datos de Ventas.')
    Ventas=pd.DataFrame(columns=['ID_VENTA','FECHA','MONTO_PRODUTOS','ID_DESPACHO','MONTO_TOTAL','ID_COMPRADOR(RUT)',
                                 'TELEFONO',
                                'DESCUENTO'])
    Ventas.set_index('ID_VENTA',inplace=True)
    Ventas.to_csv(path_Ventas, encoding='utf-8')
try:
    Despachos=pd.read_csv(path_Despachos, encoding='utf-8')
    Despachos.set_index('ID_DESPACHO',inplace=True)
except:
    print('No se encontro base de datos de Despachos.')
    Despachos=pd.DataFrame(columns=['ID_DESPACHO','FECHA','ID_VENTA','CALLE','NUMERO','DEPTO-OTROS','COMUNA','FECHA_ENTREGA',
                                   'ESTADO'])
    Despachos.set_index('ID_DESPACHO',inplace=True)
    Despachos.to_csv(path_Despachos, encoding='utf-8')
    
if os.path.exists(path_Lista_Ventas):
    with open(path_Lista_Ventas, 'rb') as file:
        Lista_Ventas=pickle.load(file)
else:
    print('Listas de ventas no existen.')
    with open(path_Lista_Ventas, 'wb') as file:
        Lista_Ventas={}
        pickle.dump(Lista_Ventas, file)
if os.path.exists(path_Ofertas):
    with open(path_Ofertas, 'rb') as file:
        Ofertas=pickle.load(file)
else:
    print('Listas de ofertas no existen.')
    with open(path_Ofertas, 'wb') as file:
        Ofertas={}
        pickle.dump(Ofertas, file)
        
### Diccionario que guarda los productos comprados en cada venta.
def crear_evento(tipo,id_prod=None,precio_old=None,precio_new=None,
                 cantidad_old=None,cantidad_new=None,nombre_old=None,nombre_new=None):
    id_evento=len(ListaEventos)+1
    fecha=pd.Timestamp(datetime.now())
    if tipo not in ['Nueva venta','Eliminar venta','Modificacion producto','Creacion producto',
                    'Creacion oferta','Modificacion oferta']:
        raise Exception('Tipo de evento:'+tipo+' no implementado.')
    if tipo in ['Nueva venta','Eliminar venta']:
        evento=EventoOferta(tipo, id_evento, fecha, id_prod)
    elif tipo in ['Modificacion producto','Creacion producto']:
        evento=EventoProducto(  tipo,id_evento,fecha,id_prod,precio_old,precio_new,
                              cantidad_old,cantidad_new)
    elif tipo in ['Creacion oferta','Modificacion oferta']:
        evento=EventoOferta(tipo, id_evento, fecha, id_prod,nombre_old,nombre_new)
    Eventos[id_evento]=evento
    ListaEventos.loc[id_evento,'TIPO']=tipo
    ListaEventos.loc[id_evento,'FECHA']=fecha
    ListaEventos.to_csv(path_Lista_Eventos, encoding='utf-8')
    with open(path_Eventos, 'wb') as file:
        pickle.dump(Eventos, file)
def crear_oferta(nombre_oferta,dic_productos,precio):
    """
    nombre_oferta:  Nombre de la oferta.
    dic_productos: Diccionario que tiene como clave el nombre de los productos de la oferta y como valor su cantidad.
    precio: Precio de la oferta.
    """
    for prod in dic_productos:
        if prod not in Productos['PRODUCTO'].values:
            print('Producto: '+prod+' no existe.')
    Ofertas[nombre_oferta]=dic_productos.copy()
    with open(path_Ofertas, 'wb') as file:
        pickle.dump(Ofertas, file)
    ####Agregamos la oferta como producto:
    descripcion='Oferta: '

    for prod in dic_productos:
        descripcion=descripcion+prod+'('+str(dic_productos[prod])+')'+' '
    cantidad=np.infty
    for prod in dic_productos:
        cantidad_aux=Productos.loc[Productos['PRODUCTO']==prod,'CANTIDAD_DISPONIBLE'].values[0]
        cantidad=min(cantidad,cantidad_aux //dic_productos[prod])
    crear_evento('Creacion oferta',len(Productos),None,precio)
    crear_producto(nombre_oferta,descripcion,cantidad,precio)
def crear_producto(producto,descripcion,cantidad,precio):
    """
    producto: Nombre del producto.
    descripcion: Descripción del producto.
    cantidad: Cantidad inicial del producto.
    precio: Precio inicial del producto.
    """
    ###Verificar si el producto existe:
    if producto in Productos['PRODUCTO'].values:
        print('Producto existente.')
        return 
    id_prod_new=len(Productos)
    crear_evento('Creacion producto',id_prod_new,None,precio,None,cantidad)
    Productos.loc[id_prod_new,'PRODUCTO']=producto
    Productos.loc[id_prod_new,'DESCRIPCIÓN']=descripcion
    Productos.loc[id_prod_new,'CANTIDAD_DISPONIBLE']=cantidad
    Productos.loc[id_prod_new,'PRECIO']=precio
    Productos.to_csv(path_Productos, encoding='utf-8')
def modificar_producto(id_producto,cantidad=None,precio=None):
    """
    id_producto: ID del producto.
    cantidad: Nueva cantidad.
    precio: Nuevo precio.
    """
    
    crear_evento('Modificacion producto',id_producto,Productos.loc[id_producto,'PRECIO'],
                 precio,Productos.loc[id_producto,'CANTIDAD_DISPONIBLE'],cantidad)
    
    if id_producto not in Productos.index.unique():
        print('Indice de producto no válido.')
        return 
    if cantidad is None and precio is None:
        print('Debe ingresar una nueva cantidad o precio.')
        return 
    if precio is not None:
        Productos.loc[id_producto,'PRECIO']=int(precio)
    if cantidad is not None:
        Productos.loc[id_producto,'CANTIDAD_DISPONIBLE']=int(cantidad)
    print('Producto actualziado exitosamente.')  
    
    
    for oferta in Ofertas:
        if Productos.loc[id_producto,'PRODUCTO']  in Ofertas[oferta]:
            cantidad=np.infty
            for prod in Ofertas[oferta]:
                cantidad_aux=Productos.loc[Productos['PRODUCTO']==prod,'CANTIDAD_DISPONIBLE'].values[0]
                cantidad=min(cantidad,cantidad_aux //Ofertas[oferta][prod])
            Productos.loc[Productos['PRODUCTO']==oferta,'CANTIDAD_DISPONIBLE']=cantidad
    Productos.to_csv(path_Productos, encoding='utf-8')
    
def crear_despacho(id_venta,fecha,calle,numero,depto,comuna,fecha_entrega,monto_despacho):
    """
    id_venta: Identificador de la venta asociada.
    fecha: Fecha de generación del despacho.
    calle: Nombre de la calle.
    numero: Numero de la dirección.
    depto: Numero del depto.
    comuna: Nombre de la comuna.
    fecha_entrega: Fecha inicial de la entrega.
    
    Función que crea un nuevo despacho. Genera el ID_DESPACHO y lo agrega a la custionada.
    
    """
    id_despacho_new=len(Despachos)+2100
    Despachos.loc[id_despacho_new,'FECHA']=fecha
    Despachos.loc[id_despacho_new,'FECHA_ENTREGA']=fecha_entrega
    Despachos.loc[id_despacho_new,'COMUNA']=comuna
    Despachos.loc[id_despacho_new,'DEPTO-OTROS']=depto
    Despachos.loc[id_despacho_new,'NUMERO']=numero
    Despachos.loc[id_despacho_new,'CALLE']=calle
    Despachos.loc[id_despacho_new,'ID_VENTA']=id_venta
    Despachos.to_csv(path_Despachos, encoding='utf-8')
    return id_despacho_new
def crear_venta(id_comprador,telefono,lista_productos,fecha,calle=None,numero=None,depto=None,comuna=None,
                fecha_entrega=None,
               monto_despacho=None,descuento=0):
    """
    id_comprador: Identificador comprado
    lista_productos: diccionario con los ID y las contidades de los productos comprados.
    fecha: Fecha de generación de la venta.
    
    Las siguientes variables son para crear el despacho.
    
    calle: Nombre de la calle.
    numero: Numero de la dirección.
    depto: Numero del depto.
    comuna: Nombre de la comuna.
    fecha_entrega: Fecha inicial de la entrega.
    
    Función que crea una nueva venta. Genera el ID_VENTA y agrega la venta a la tabla de ventas.
    """
    
    id_venta_new=len(Ventas)+2000
    Lista_Ventas[id_venta_new]=lista_productos.copy()
    monto_prods=0
    for id_prod in Lista_Ventas[id_venta_new]:
        ###Actualizamos las cantidades
        monto_prods=monto_prods+Lista_Ventas[id_venta_new][id_prod]*int(Productos.loc[id_prod,'PRECIO'])
        if Productos.loc[id_prod,'PRODUCTO'] in Ofertas:
            for prod in Ofertas[Productos.loc[id_prod,'PRODUCTO']]:
                ###Obtenemos la clave del producto
                id_prod_aux=Productos.loc[Productos['PRODUCTO']==prod].index.values
                ##Actualizamos la cantidad de cada producto en la oferta
                Productos.loc[id_prod_aux,'CANTIDAD_DISPONIBLE']=(Productos.loc[id_prod_aux,'CANTIDAD_DISPONIBLE']
                -Ofertas[Productos.loc[id_prod,'PRODUCTO']][prod]*Lista_Ventas[id_venta_new][id_prod])
        #else:
        #    Productos.loc[id_prod,'CANTIDAD_DISPONIBLE']=(int(Productos.loc[id_prod,'CANTIDAD_DISPONIBLE'])-
        #                                                 Lista_Ventas[id_venta_new][id_prod])
    ###Actualizamos la cantidad de las ofertas.
    for oferta in Ofertas:    
       # if Productos.loc[id_prod,'PRODUCTO'] in Ofertas:
        cantidad=np.infty
        for prod in Ofertas[oferta]:
            cantidad_aux=Productos.loc[Productos['PRODUCTO']==prod,'CANTIDAD_DISPONIBLE'].values[0]
            cantidad=min(cantidad,cantidad_aux //Ofertas[oferta][prod])
        Productos.loc[Productos['PRODUCTO']==oferta,'CANTIDAD_DISPONIBLE']=cantidad
    
    monto_prods=np.sum([ Lista_Ventas[id_venta_new][id_prod]*int(Productos.loc[id_prod,'PRECIO']) 
                   for id_prod in Lista_Ventas[id_venta_new]])
    id_despacho=crear_despacho(id_venta_new,fecha,calle,numero,depto,comuna,fecha_entrega,monto_despacho)
    
    crear_evento('Nueva venta',id_venta_new)
    
    Ventas.loc[id_venta_new,'FECHA']=fecha
    Ventas.loc[id_venta_new,'MONTO_PRODUTOS']=monto_prods
    Ventas.loc[id_venta_new,'MONTO_TOTAL']=monto_prods+monto_despacho-descuento
    Ventas.loc[id_venta_new,'DESCUENTO']=descuento
    Ventas.loc[id_venta_new,'ID_DESPACHO']=id_despacho
    Ventas.loc[id_venta_new,'ID_COMPRADOR(RUT)']=id_comprador
    Ventas.loc[id_venta_new,'TELEFONO']=telefono
    Ventas.to_csv(path_Ventas, encoding='utf-8')
    with open(path_Lista_Ventas, 'wb') as file:
        pickle.dump(Lista_Ventas, file)
    return id_venta_new
def volver(root,top):
    root.deiconify()
    root.state('zoomed')
    top.destroy()
class Ventana_guia_despachos:
    def __init__(self,root,bg_color):
        self.root=root
        self.bg_color=bg_color
        top = Toplevel(self.root)
        top.geometry('1000x700')
        top.state('zoomed')
        top.configure(background=self.bg_color)
        top.title("Detalle Compra")
        top.protocol("WM_DELETE_WINDOW", functools.partial(volver, self.root,top))
        
        self.btn_volver = Button(top,text="Volver", command=functools.partial(volver, self.root,top))
        self.btn_volver.pack(side='bottom',padx=10)
        
        self.guia_despachos=pd.merge(left=Ventas['ID_COMPRADOR(RUT)'],right=Despachos,
                                     left_index=True,right_on=['ID_VENTA'])
        
        self.guia_despachos['FECHA_ENTREGA']=pd.to_datetime(self.guia_despachos['FECHA_ENTREGA'])
        self.guia_despachos_filtrada=self.guia_despachos.copy()
        self.guia_despachos_filtrada=self.guia_despachos_filtrada[self.guia_despachos_filtrada['ESTADO']!='ENTREGADO']
        
        frame_opciones=Frame(top)
        frame_opciones.pack(padx=5,pady=6)
        
        frame_guia_despacho=Frame(top)
        frame_guia_despacho.pack(padx=5,pady=6)
        
        frame_exportar_guia=Frame(top)
        frame_exportar_guia.pack(padx=5,pady=5)
        
        self.tabla_guia_despachos = Table(frame_guia_despacho, dataframe=self.guia_despachos_filtrada,height=400,
                                            showtoolbar=True, showstatusbar=True,editable=False,width=700)
        self.tabla_guia_despachos.show()
        
        
        
        self.label_nombre_guia=Label(frame_exportar_guia,text='Título guía:',justify=CENTER)
        self.label_nombre_guia.pack(side='left',padx=5)
        
        self.entry_nombre_guia=Entry(frame_exportar_guia)
        self.entry_nombre_guia.pack(side='left',padx=5)
            
           
        
        self.btn_exportar_guia=Button(frame_exportar_guia,text='Generar guía despacho.',justify=CENTER,
                                 command=self.exportar_guia)
        self.btn_exportar_guia.pack(side='left',padx=5)
        
        self.label_rango_fechas=Label(frame_opciones,text='Seleccione rango de fechas:',justify=CENTER)
        self.label_rango_fechas.pack(side='left',padx=5)
        
        self.label_fecha_inicial=Label(frame_opciones,text='Fecha inicial:',justify=CENTER)
        self.label_fecha_inicial.pack(side='left',padx=5)
        self.entry_fecha_inicial=ttk.Combobox(frame_opciones,state="readonly")
        self.entry_fecha_inicial['values']=list(np.unique([fecha.date() for fecha in self.guia_despachos['FECHA_ENTREGA']]))
        self.entry_fecha_inicial.pack(side='left',padx=5)
        
        self.label_fecha_final=Label(frame_opciones,text='Fecha final:',justify=CENTER)
        self.label_fecha_final.pack(side='left',padx=5)
        self.entry_fecha_final=ttk.Combobox(frame_opciones,state="readonly")
        self.entry_fecha_final['values']=list(np.unique([fecha.date() for fecha in self.guia_despachos['FECHA_ENTREGA']]))
        self.entry_fecha_final.pack(side='left',padx=5)
        
        self.btn_gen_guia=Button(frame_opciones,text='Generar guía despacho.',justify=CENTER,
                            command=self.generar_guia_despacho)
        self.btn_gen_guia.pack(side='left',padx=5)
        
        self.root.withdraw()
    def generar_guia_despacho(self):
        fecha_inicial=entry_fecha_inicial.get()
        fecha_final=entry_fecha_inicial.get()
        if fecha_inicial=='':
            messagebox.showinfo('Fecha inválida','Seleccione una fecha inicial.')
            return 
        if fecha_final=='':
            messagebox.showinfo('Fecha inválida','Seleccione una fecha final.')
            return 
        fecha_inicial=pd.Timestamp(fecha_inicial)
        fecha_final=pd.Timestamp(fecha_final)
        if fecha_inicial>fecha_final:
            messagebox.showinfo('Fecha inválida','La fecha inicial debe ser menor a la fecha final.')
            return 
        self.guia_despachos_filtrada=self.guia_despachos[self.guia_despachos['FECHA_ENTREGA']>=fecha_inicial]
        self.guia_despachos_filtrada=self.guia_despachos_filtrada[self.guia_despachos['FECHA_ENTREGA']<=fecha_final]
        self.guia_despachos_filtrada=self.guia_despachos_filtrada[self.guia_despachos_filtrada['ESTADO']!='ENTREGADO']
        self.tabla_guia_despachos.tableChanged()
        self.tabla_guia_despachos.destroy()
        self.tabla_guia_despachos = Table(frame_guia_despacho, dataframe=self.guia_despachos_filtrada,height=400,
                                        showtoolbar=True, showstatusbar=True,editable=False,width=700)
        self.tabla_guia_despachos.show()
        messagebox.showinfo('Guía generada exitosamente.','Guía generada exitosamente.')
    def exportar_guia(self):
        nombre_guia=self.entry_nombre_guia.get()
        if nombre_guia=='':
            messagebox.showinfo('Error guía despacho','Titulo guía despacho en blanco.')
            return

        path_destino=filedialog.askdirectory(title='Selecione ruta de salida')#'Data_test.csv'
        path_destino = str(os.path.normpath(path_destino))+os.sep+nombre_guia+'.csv'
        self.guia_despachos_filtrada.to_csv(path_destino, encoding='utf-8')
        messagebox.showinfo('Guía despacho','Guía despachos generado exitosamente.')
class Ventana_detalles_venta:
    def __init__(self,root,bg_color):
        self.root=root
        self.bg_color=bg_color
        top = Toplevel(self.root)
        top.geometry('1000x1000')
        top.state('zoomed')
        top.configure(background=self.bg_color)
        top.title("Detalle Compra")
        top.protocol("WM_DELETE_WINDOW", functools.partial(volver, self.root,top))
        
        self.btn_volver = Button(top,text="Volver", command=functools.partial(volver, self.root,top))
        self.btn_volver.pack(side='bottom',padx=10)
        
        frame_tabla_ventas=Frame(top)
        frame_tabla_ventas.pack(padx=5)
        self.tabla_ventas = Table(frame_tabla_ventas, dataframe=Ventas.reset_index(),
        showtoolbar=False, showstatusbar=True,editable=False,width=800,height=300)
        self.tabla_ventas.show()
        
        frame_opciones=Frame(top)
        frame_opciones.pack(padx=5)
        
        self.label_opciones=Label(frame_opciones,text='ID_VENTA')
        self.label_opciones.pack(side='left',padx=5)
        
        self.entry_id_venta=ttk.Combobox(frame_opciones,state="readonly")
        self.entry_id_venta['values']=list(Ventas.index.values)
        self.entry_id_venta.pack(side='left',padx=5)
        
        
        
        self.btn_ver_resumen=Button(frame_opciones,text='Ver Resumen.',justify=CENTER,command=self.ver_resumen)
        self.btn_ver_resumen.pack(side='left',padx=5)
        
        frame_resumen=Frame(top)
        frame_resumen.pack(padx=5)
        self.text_resumen=StringVar()
        self.text_resumen.set('')
        self.label_titulo_resumen=Label(frame_resumen,text='Resumen venta:',justify=CENTER)
        self.label_titulo_resumen.pack(padx=5,pady=5)
        self.label_resumen=Label(frame_resumen,textvariable= self.text_resumen,justify=LEFT
                                 ,width=300,height=300)
        self.label_resumen.pack(padx=5,pady=5)
        
        self.root.withdraw()
    def ver_resumen(self):
        id_venta=self.entry_id_venta.get()
        if id_venta=='':
            return
        id_venta=int(id_venta)
        str_lista_venta=''
        for id_prod in Lista_Ventas[id_venta]:
            prod=Productos.loc[id_prod,'PRODUCTO']
            str_lista_venta=str_lista_venta+prod+': '+str(Lista_Ventas[id_venta][id_prod])+'\n'
        str_lista_venta=str_lista_venta+'Monto Venta: '+str(Ventas.loc[id_venta,'MONTO_PRODUTOS'])+'\n'
        str_lista_venta=str_lista_venta+'Monto Total: '+str(Ventas.loc[id_venta,'MONTO_TOTAL'])+'\n'
        id_despacho=int(Ventas.loc[id_venta,'ID_DESPACHO'])
        str_lista_venta=str_lista_venta+'ID Despacho: '+str(id_despacho)+'\n'
        for col in ['FECHA','CALLE','NUMERO','DEPTO-OTROS','COMUNA','FECHA_ENTREGA']:
            aux=str(Despachos.loc[id_despacho,col])
            str_lista_venta=str_lista_venta+ col+':'+aux+'\n'
        self.text_resumen.set(str_lista_venta)
        
class Ventana_tablas:
    def __init__(self,root,bg_color):
        self.root=root
        self.bg_color=bg_color
        top = Toplevel(self.root)
        
        top.geometry('1200x600')
        top.state('zoomed')
        top.configure(background=self.bg_color)
        top.title("Tablas")
        top.protocol("WM_DELETE_WINDOW", functools.partial(volver, self.root,top))
        
        self.btn_volver = Button(top,text="Volver", command=functools.partial(volver, self.root,top))
        self.btn_volver.pack(side='bottom',padx=10)
        
        frame_lables=Frame(top)
        frame_lables.pack(padx=5)
        
        self.label_prods=Label(frame_lables,text='Stocks-Productos',justify=CENTER,bg='blue',fg='white',width=50)
        self.label_prods.pack(fill='x',expand=True,padx=10,pady=5,side='left')
        self.label_ventas=Label(frame_lables,text='Ventas',justify=CENTER,bg='blue',fg='white',width=50)
        self.label_ventas.pack(fill='x',expand=True,padx=10,pady=5,side='left')
        self.label_despachos=Label(frame_lables,text='Despachos',justify=CENTER,bg='blue',fg='white',width=50)
        self.label_despachos.pack(fill='x',expand=True,padx=10,pady=5,side='left')
        
        frame_productos=Frame(top,width=300,height=100)
        frame_productos.pack(side='left',padx=5,pady=5,fill='x',expand=True)
        
        frame_ventas=Frame(top,width=300,height=100)
        frame_ventas.pack(side='left',padx=5,pady=5,fill='x',expand=True)
        
        frame_despachos=Frame(top,width=300,height=100)
        frame_despachos.pack(side='left',padx=5,pady=5,fill='x',expand=True)
        
        
        self.tabla_ventas = Table(frame_ventas, dataframe=Ventas.reset_index(),height=400,
                                            showtoolbar=False, showstatusbar=True,editable=False,width=300)
        self.tabla_ventas.show()
        
        self.tabla_productos = Table(frame_productos, 
                                dataframe=Productos[['PRODUCTO','CANTIDAD_DISPONIBLE','PRECIO']].reset_index(),
                                           showtoolbar=False,height=400, showstatusbar=True,editable=False,width=300)
        self.tabla_productos.show()
        
        self.tabla_despachos = Table(frame_despachos, dataframe=Despachos.reset_index(),
                                            showtoolbar=True,height=400, showstatusbar=True,editable=True,width=300)
        self.tabla_despachos.show()
        
        self.root.withdraw()
class Ventana_eliminar_venta:
    def __init__(self,root,bg_color):
        self.root=root
        self.bg_color=bg_color
        self.root.withdraw()
        top = Toplevel(self.root)
        top.geometry('600x600')
        top.state('zoomed')
        top.configure(background=self.bg_color)
        top.title("Eliminar Venta")
        top.protocol("WM_DELETE_WINDOW", functools.partial(volver, self.root,top))
        
        self.btn_volver = Button(top,text="Volver", command=functools.partial(volver, self.root,top))
        self.btn_volver.pack(side='bottom',padx=10)
        
        self.Ventas_aux=Ventas.reset_index()
        
        frame_ventas= Frame(top)
        frame_ventas.pack(padx=10,pady=10)
        self.ventas_anteriores = Table(frame_ventas, dataframe=self.Ventas_aux,
                                            showtoolbar=True, showstatusbar=True,editable=False)
        
        self.ventas_anteriores.show()
        frame_opciones=Frame(top,width=200)
        frame_opciones.pack(padx=10,pady=10)
        
        self.label_id_venta=Label(frame_opciones,text='ID_VENTA')
        self.label_id_venta.pack(padx=5,side='left')
        self.entry_id_venta=ttk.Combobox(frame_opciones,state="readonly")
        self.entry_id_venta["values"]=list(Ventas.index.values)
        self.entry_id_venta.pack(padx=5,side='left')
        
        self.btn_eliminar_venta=Button(frame_opciones,text='Eliminar.',command=self.eliminar_venta)
        self.btn_eliminar_venta.pack(padx=5,side='left')
    def eliminar_venta(self):
        id_venta=self.entry_id_venta.get()
        if id_venta=='':
            return
        id_venta=int(id_venta)
        Ventas.drop(labels=id_venta,inplace=True)
        Ventas.to_csv(path_Ventas, encoding='utf-8')
        Despachos.drop(labels=Despachos[Despachos['ID_VENTA']==id_venta].index.values,inplace=True)
        Despachos.to_csv(path_Despachos, encoding='utf-8')
        for prod in Lista_Ventas[id_venta]:
            Productos.loc[prod,'CANTIDAD_DISPONIBLE']=(Productos.loc[prod,'CANTIDAD_DISPONIBLE']+
                                                       Lista_Ventas[id_venta][prod])
            if Productos.loc[prod,'PRODUCTO'] in Ofertas:
                for prod_aux in Ofertas[Productos.loc[prod,'PRODUCTO']]:
                    id_prod_aux=Productos.loc[Productos['PRODUCTO']==prod_aux].index.values[0]
                    Productos.loc[id_prod_aux,'CANTIDAD_DISPONIBLE']=(Productos.loc[id_prod_aux,'CANTIDAD_DISPONIBLE']+
                                     Lista_Ventas[id_venta][prod]* Ofertas[Productos.loc[prod,'PRODUCTO']][prod_aux])
            
            
        for oferta in Ofertas:
            cantidad=np.infty
            for prod in Ofertas[oferta]:
                cantidad_aux=Productos.loc[Productos['PRODUCTO']==prod,'CANTIDAD_DISPONIBLE'].values[0]
                cantidad=min(cantidad,cantidad_aux //Ofertas[oferta][prod])
            Productos.loc[Productos['PRODUCTO']==oferta,'CANTIDAD_DISPONIBLE']=cantidad
            
        Productos.to_csv(path_Productos, encoding='utf-8')
        Lista_Ventas.pop(id_venta)
        with open(path_Lista_Ventas, 'wb') as file:
            pickle.dump(Lista_Ventas, file)
        self.Ventas_aux.drop(self.Ventas_aux.index[self.Ventas_aux['ID_VENTA']==id_venta],inplace=True)
        self.ventas_anteriores.tableChanged()
        self.entry_id_venta["values"]=list(Ventas.index.values)
        crear_evento('Eliminar venta',id_venta)
class Ventana_nueva_venta:
    def __init__(self,root,bg_color):
        self.bg_color=bg_color
        self.root=root
        self.fecha=pd.Timestamp(datetime.now())
        self.fecha=self.fecha.replace(second=0,microsecond=0,nanosecond=0,minute=0,hour=0)
        self.lista_venta_acutal={}
        top = Toplevel(self.root)
        
        top.geometry('1200x600')
        top.state('zoomed')
        top.configure(background=self.bg_color)
        top.title("Nueva Venta")
        top.protocol("WM_DELETE_WINDOW", functools.partial(volver, self.root,top))
        
        
        
        self.btn_volver = Button(top,text="Volver", command=functools.partial(volver, self.root,top))
        self.btn_volver.pack(side='bottom',padx=10)
        
        
        
        self.btn_crear_venta=Button(top,command=self.crear_venta,text='Crear Venta.')
        self.btn_crear_venta.pack(side='bottom',padx=10)
        
        
        frame_fecha=Frame(top,bg=self.bg_color)
        frame_fecha.pack(fill='x',padx=10,pady=3)
        
        self.label_fecha_nueva=Label(frame_fecha,text='Ingrese fecha (opcional):',justify=CENTER)
        self.label_fecha_nueva.pack(side='left',padx=5)
        self.label_fecha_nueva_año=Label(frame_fecha,text='año:')
        self.label_fecha_nueva_año.pack(side='left',padx=5)
        self.entry_fecha_nueva_año=Entry(frame_fecha)
        self.entry_fecha_nueva_año.pack(side='left',padx=5)
        self.label_fecha_nueva_mes=Label(frame_fecha,text='mes:')
        self.label_fecha_nueva_mes.pack(side='left',padx=5)
        self.entry_fecha_nueva_mes=Entry(frame_fecha)
        self.entry_fecha_nueva_mes.pack(side='left',padx=5)
        self.label_fecha_nueva_dia=Label(frame_fecha,text='dia:')
        self.label_fecha_nueva_dia.pack(side='left',padx=5)
        self.entry_fecha_nueva_dia=Entry(frame_fecha)
        self.entry_fecha_nueva_dia.pack(side='left',padx=5)
        self.btn_fecha_nueva=Button(frame_fecha,text='Cambiar Fecha',justify=CENTER,command=self.cambiar_fecha)
        self.btn_fecha_nueva.pack(side='left',padx=5)
        self.texto_fecha=StringVar()
        self.texto_fecha.set('Fecha: '+str(self.fecha.date())+'.')
        self.label_fecha=Label(frame_fecha,textvariable=self.texto_fecha,justify=CENTER)
        self.label_fecha.pack(side='left',padx=5)
        
        
        self.texto_lista_prods=StringVar()
        self.texto_lista_prods.set('Lista de Producto:\n')
        self.label_lista_prods=Label(top, 
        textvariable=self.texto_lista_prods,justify=CENTER,bg='blue',fg='white')
        self.label_lista_prods.pack(padx=3,pady=3,fill='x',expand=True)
        
        
        
        frame1=Frame(top,bg=self.bg_color)
        frame1.pack(fill='x',expand=True,padx=10,pady=3)
        
        self.label_comprador= Label(frame1,text='Nombre o Rut Comprador:')
        self.label_comprador.pack(side='left',padx=10)
        self.entry_comprador= Entry(frame1,width=30)
        self.entry_comprador.pack(side='left',padx=10)
        
        self.label_tel= Label(frame1,text='Número teléfono:')
        self.label_tel.pack(side='left',padx=10)
        self.entry_tel= Entry(frame1,width=30)
        self.entry_tel.pack(side='left',padx=10)
        
        self.label_fecha_entrega= Label(frame1,text='Fecha entrega:')
        self.label_fecha_entrega.pack(side='left')
        self.entry_fecha_entrega= ttk.Combobox(frame1,state="readonly")
        self.entry_fecha_entrega["values"]=list([str(fecha_aux.date()) 
                                            for fecha_aux in pd.date_range(self.fecha,periods=10,freq='D')])
        self.entry_fecha_entrega.pack(side='left',padx=10)
        
        self.label_descuento= Label(frame1,text='Descuento',justify=CENTER)
        self.label_descuento.pack(side='left',padx=10)
        self.entry_descuento=Entry(frame1,text='0')
        self.entry_descuento.pack(side='left',padx=10)
        
        
        frame2=Frame(top,bg=self.bg_color)
        frame2.pack(fill='x',expand=True,padx=10,pady=10)
        
        #dept=depto_entry.get()
        #    comuna=comuna_entry.get()
        #    numero=numero_entry.get()
        #    monto_despacho=monto_despacho_entry.get()
        #    calle=calle_entry.get()
        
        
        self.label_calle=Label(frame2,text='Calle:')
        self.label_calle.pack(side='left',padx=10)
        self.entry_calle=Entry(frame2)
        self.entry_calle.pack(side='left',padx=10)
        
        self.label_numero=Label(frame2,text='Número:')
        self.label_numero.pack(side='left',padx=10)
        self.entry_numero=Entry(frame2)
        self.entry_numero.pack(side='left',padx=10)
        
        self.label_depto=Label(frame2,text='Depto:')
        self.label_depto.pack(side='left',padx=10)
        self.entry_depto=Entry(frame2)
        self.entry_depto.pack(side='left',padx=10)
        
        self.label_comuna=Label(frame2,text='Comuna:')
        self.label_comuna.pack(side='left',padx=10)
        self.entry_comuna=Entry(frame2)
        self.entry_comuna.pack(side='left',padx=10)
        
        self.label_monto_despacho=Label(frame2,text='Monto Despacho:')
        self.label_monto_despacho.pack(side='left',padx=10)
        self.entry_monto_despacho=Entry(frame2)
        self.entry_monto_despacho.pack(side='left',padx=10)
        
        
        frame3=Frame(top,bg=self.bg_color)
        frame3.pack(fill='x',expand=True,padx=10,pady=10)
        
        
        self.label_sel_prod= Label(frame3,text='Seleccione producto:')
        self.label_sel_prod.pack(side='left',padx=10)
        self.combo1 = ttk.Combobox(frame3, state="readonly",width=100)
        self.combo1["values"] = list(Productos['PRODUCTO'].unique())
        self.combo1.pack(side='left',padx=10)
        
        self.label_cantidad= Label(frame3,text='Canitdad:')
        self.label_cantidad.pack(side='left')
        self.entry_cantidad= Entry(frame3,width=10)
        self.entry_cantidad.pack(side='left',padx=10)
            
        self.btn_add_prod= Button(frame3,text='Agregar a la lista.',
                             command=self.agregar_prod_lista_venta,justify=CENTER)
        self.btn_add_prod.pack(side='left',padx=10)
        
        
        self.root.withdraw()
    def crear_venta(self):
        lista_venta_acutal_por_ids={}
        if self.lista_venta_acutal:

            for prod in self.lista_venta_acutal:
                id_prod=Productos[Productos['PRODUCTO']==prod].index.values[0]
                lista_venta_acutal_por_ids[id_prod]=int(self.lista_venta_acutal[prod])
        else:
            messagebox.showinfo('Lista productos inválida.','Debe seleccionar al menos un producto.')
            return
        descuento=self.entry_descuento.get()
        if descuento.isdigit():
            descuento=int(descuento)
        else:
            messagebox.showinfo('Descuento invalido.','El descuento debe ser un número positivo.')
            return
        telefono=self.entry_tel.get()
        id_comprador=self.entry_comprador.get()
        fecha_entrega=self.entry_fecha_entrega.get()
        dept=self.entry_depto.get()
        comuna=self.entry_comuna.get()
        numero=self.entry_numero.get()
        monto_despacho=self.entry_monto_despacho.get()
        if monto_despacho.isdigit():
            monto_despacho=int(monto_despacho)
        else:
            messagebox.showinfo('Monto despacho invalido.','El monto de despacho debe ser un número positivo.')
            return
        calle=self.entry_calle.get()
        id_venta=crear_venta(id_comprador,telefono,lista_venta_acutal_por_ids,str(self.fecha.date()),
        calle=calle,numero=numero,depto=dept,comuna=comuna,fecha_entrega=fecha_entrega,
           monto_despacho=monto_despacho,descuento=descuento)

        self.entry_descuento.delete(0,len(self.entry_descuento.get()))
        self.entry_comprador.delete(0,len(id_comprador))
        self.entry_calle.delete(0,len(calle))
        self.entry_numero.delete(0,len(numero))
        self.entry_depto.delete(0,len(dept))
        self.entry_comuna.delete(0,len(comuna))
        self.entry_cantidad.delete(0,len(self.entry_cantidad.get()))
        self.entry_monto_despacho.delete(0,len(self.entry_monto_despacho.get()))

        id_venta=int(id_venta)
        str_lista_venta='Resumen Venta:\n'
        for id_prod in Lista_Ventas[id_venta]:
            prod=Productos.loc[id_prod,'PRODUCTO']
            str_lista_venta=str_lista_venta+prod+': '+str(Lista_Ventas[id_venta][id_prod])+'\n'
        str_lista_venta=str_lista_venta+'Monto Venta: '+str(Ventas.loc[id_venta,'MONTO_PRODUTOS'])+'\n'
        str_lista_venta=str_lista_venta+'Monto Total: '+str(Ventas.loc[id_venta,'MONTO_TOTAL'])+'\n'
        id_despacho=int(Ventas.loc[id_venta,'ID_DESPACHO'])
        str_lista_venta=str_lista_venta+'ID Despacho: '+str(id_despacho)+'\n'
        for col in ['FECHA','CALLE','NUMERO','DEPTO-OTROS','COMUNA','FECHA_ENTREGA']:
            aux=str(Despachos.loc[id_despacho,col])
            str_lista_venta=str_lista_venta+ col+':'+aux+'\n'

        self.texto_lista_prods.set('Venta Generada exitosamente.\n'+str_lista_venta)
        self.lista_venta_acutal={}
    def cambiar_fecha(self):
        año=self.entry_fecha_nueva_año.get()
        mes=self.entry_fecha_nueva_mes.get()
        dia=self.entry_fecha_nueva_dia.get()
        if año.isdigit() and mes.isdigit() and dia.isdigit():
            año=int(año)
            mes=int(mes)
            dia=int(dia)
        else:
            messagebox.showinfo('Error fecha','Ingrese una fecha válida.')
            return
        if año <2020 or año >2200:
            messagebox.showinfo('Error fecha','Ingrese un año válido.')
            return 
        if mes <0 or mes>12:
            messagebox.showinfo('Error fecha','Ingrese un mes válido. (como número)')
            return 
        try:
            self.fecha=pd.Timestamp(day=dia,month=mes,year=año)
        except:
            messagebox.showinfo('Error fecha','Ingrese una fecha válida.')
            return 
        self.texto_fecha.set('Fecha: '+str(self.fecha.date())+'.')
        self.entry_fecha_entrega["values"]=list([str(fecha_aux.date()) 
                                        for fecha_aux in pd.date_range(self.fecha,periods=10,freq='D')])
        messagebox.showinfo('Fecha modificada','Fecha modificada exitosamente.')
        return
    def agregar_prod_lista_venta(self):
        producto=self.combo1.get()
        cantidad=self.entry_cantidad.get()
        if producto=='':
            messagebox.showinfo('Error producto','Debe seleccionar el producto.')
            return
        if cantidad.isdigit():
            cantidad=int(cantidad)
            if cantidad<=0:
                messagebox.showinfo('Error cantidad','Debe seleccionar al menos una unidad.')
                return
        else:
            messagebox.showinfo('Error cantidad','Debe ingresar la cantidad.')
            return
        if Productos.loc[Productos['PRODUCTO']==producto,'CANTIDAD_DISPONIBLE'].values[0]-cantidad<0:
            messagebox.showinfo('Producto sin stock suficiente.','Producto '+producto+' sin stock suficiente.')
            return
        self.lista_venta_acutal[producto]=cantidad
        str_lista_venta_actual='Lista de Producto:\n'
        for prod in self.lista_venta_acutal:
            str_lista_venta_actual=str_lista_venta_actual+prod+': '+str(self.lista_venta_acutal[prod])+'\n'


        self.texto_lista_prods.set(str_lista_venta_actual)
class Ventana_gestionar_prods:
    def __init__(self,root,bg_color):
        
        self.bg_color=bg_color
        self.root=root
        top = Toplevel(self.root)
        top.geometry('1000x800')
        top.state('zoomed')
        top.configure(background=self.bg_color)
        top.title("Gestión de Productos")
        top.protocol("WM_DELETE_WINDOW", functools.partial(volver, self.root,top))
        
        self.btn_volver = Button(top,text="Volver", command=functools.partial(volver, self.root,top))
        self.btn_volver.pack(side='bottom',expand=True,fill='x',padx=10)
        
        frame_tabla_prods=Frame(top)
        frame_tabla_prods.pack(padx=10,pady=10)
        self.tabla_productos = Table(frame_tabla_prods, dataframe=Productos,
                                           showtoolbar=False, showstatusbar=True,editable=False,width=900,height=100)
        self.tabla_productos.show()
        
        frame_agregar_prod=Frame(top)
        frame_agregar_prod.pack(padx=10,expand=True,fill='x')
        
        frame_modificar_prod=Frame(top)
        frame_modificar_prod.pack(padx=10,expand=True,fill='x')
        
        frame_agregar_oferta=Frame(top)
        frame_agregar_oferta.pack(padx=10,expand=True,fill='x')
        
        frame_modificar_oferta=Frame(top)
        frame_modificar_oferta.pack(padx=10,expand=True,fill='x')

        
        self.texto_resultado=StringVar()
        self.texto_resultado.set('Agregue un nuevo producto:')
        self.label_resultado=Label(frame_agregar_prod,textvariable=self.texto_resultado,justify=CENTER)
        self.label_resultado.pack()
        
        self.btn_agregar_prod=Button(frame_agregar_prod,text='Agregar Producto',
                                     command=self.agregar_producto,width=100)
        self.btn_agregar_prod.pack(side='bottom',fill='x',padx=10)
        
        self.label_nomb_prod=Label(frame_agregar_prod,text='Nombre Producto',justify=CENTER)
        self.label_nomb_prod.pack(side='left',padx=10,pady=10)
        self.entry_nomb_prod=Entry(frame_agregar_prod)
        self.entry_nomb_prod.pack(side='left',padx=10)
        
        self.label_descripcion=Label(frame_agregar_prod,text='Descripción')
        self.label_descripcion.pack(side='left',padx=10)
        self.entry_descripcion=Entry(frame_agregar_prod)
        self.entry_descripcion.pack(side='left',padx=10)
        
        self.label_precio=Label(frame_agregar_prod,text='Precio')
        self.label_precio.pack(side='left')
        self.entry_precio=Entry(frame_agregar_prod,width=10,text='precio')
        self.entry_precio.pack(side='left',padx=10)
        
        self.label_cantidad=Label(frame_agregar_prod,text='Cantidad')
        self.label_cantidad.pack(side='left')
        self.entry_cantidad=Entry(frame_agregar_prod,width=10,text='cantidad')
        self.entry_cantidad.pack(side='left',padx=10)
        
        
        ####Para modificar un producto
        self.productos_menos_ofertas= list([ prod for prod in Productos['PRODUCTO'] if prod not in Ofertas])
        
        self.label_title_mod=Label(frame_modificar_prod,text='Modificación Productos',justify=CENTER)
        self.label_title_mod.pack(padx=5,pady=10)
        self.label_producto_mod=Label(frame_modificar_prod,text='Producto:',justify=CENTER)
        self.label_producto_mod.pack(side='left',padx=5)
        
        self.entry_producto_mod=ttk.Combobox(frame_modificar_prod,state="readonly")
        self.entry_producto_mod['values']=self.productos_menos_ofertas
        self.entry_producto_mod.pack(side='left',padx=5)
        
        self.label_precio_mod=Label(frame_modificar_prod,text='Precio nuevo:',justify=CENTER)
        self.label_precio_mod.pack(side='left',padx=5)
        self.entry_precio_mod=Entry(frame_modificar_prod)
        self.entry_precio_mod.pack(side='left',padx=5)
        
        self.label_cantidad_mod=Label(frame_modificar_prod,text='Cantidad nueva:',justify=CENTER)
        self.label_cantidad_mod.pack(side='left',padx=5)
        self.entry_cantidad_mod=Entry(frame_modificar_prod)
        self.entry_cantidad_mod.pack(side='left',padx=5)
        
        
            
        self.btn_mod=Button(frame_modificar_prod,text='Modificar Producto.',
                            command=self.modificar_prod,justify=CENTER)
        self.btn_mod.pack(side='left',padx=5)
        
        
        self.lista_productos_oferta={}
        
        
        
        self.btn_agregar_oferta=Button(frame_agregar_oferta,text='Agregar Oferta',justify=CENTER,
                                  command=self.agregar_oferta)
        self.btn_agregar_oferta.pack(padx=5,expand=True,fill='x',side='bottom')
        
        self.txt_oferta= StringVar()
        self.txt_oferta.set('Resumen Oferta:')
        self.label_detalle_oferta=Label(frame_agregar_oferta,
                                        textvariable=self.txt_oferta,justify=CENTER)
        self.label_detalle_oferta.pack(padx=5,pady=5,expand=True,fill='x',side='bottom')
        
        self.label_agregar_oferta= Label(frame_agregar_oferta,text='Agregar Oferta',justify=LEFT)
        self.label_agregar_oferta.pack(padx=5)
        
        self.label_nombre_oferta= Label(frame_agregar_oferta,text='Nombre Oferta',justify=LEFT)
        self.label_nombre_oferta.pack(side='left',padx=5)
        self.entry_nombre_oferta =Entry(frame_agregar_oferta)
        self.entry_nombre_oferta.pack(side='left',padx=5)
        
        self.label_prod_oferta=Label(frame_agregar_oferta,text='Producto:')
        self.label_prod_oferta.pack(side='left',padx=5)
        self.entry_prod_oferta=ttk.Combobox(frame_agregar_oferta,state="readonly")
        self.entry_prod_oferta['values']=self.productos_menos_ofertas
        self.entry_prod_oferta.pack(side='left',padx=5)
        
        self.label_cantidad_oferta=Label(frame_agregar_oferta,text='Cantidad:')
        self.label_cantidad_oferta.pack(side='left',padx=5)
        self.entry_cantidad_oferta=Entry(frame_agregar_oferta)
        self.entry_cantidad_oferta.pack(side='left',padx=5)
        
        self.label_precio_oferta=Label(frame_agregar_oferta,text='Precio:')
        self.label_precio_oferta.pack(side='left',padx=5)
        self.entry_precio_oferta=Entry(frame_agregar_oferta)
        self.entry_precio_oferta.pack(side='left',padx=5)
                
        self.btn_agregar_prod_oferta=Button(frame_agregar_oferta,text='Agregar producto.',
                                       command=self.agregar_prod_oferta)
        self.btn_agregar_prod_oferta.pack(side='left',padx=5)
        
        self.lista_ofertas=list([ prod for prod in Productos['PRODUCTO'] if prod in Ofertas])
        
        self.label_title_mod_of=Label(frame_modificar_oferta,text='Modificar Ofertas.',justify=CENTER)
        self.label_title_mod_of.pack(padx=5)
        self.label_ofertas_mod_of=Label(frame_modificar_oferta,text='Oferta :',justify=CENTER)
        self.label_ofertas_mod_of.pack(side='left',padx=5)
        self.entry_ofertas_mod_of=ttk.Combobox(frame_modificar_oferta,state="readonly",width=40)
        self.entry_ofertas_mod_of['values']=self.lista_ofertas
        self.entry_ofertas_mod_of.pack(side='left',padx=5)
        self.label_nuevo_nombre_mod_of=Label(frame_modificar_oferta,text='Nuevo nombre:',justify=CENTER)
        self.label_nuevo_nombre_mod_of.pack(side='left',padx=5)
        self.entry_nuevo_nombre_mod_of=Entry(frame_modificar_oferta,width=40)
        self.entry_nuevo_nombre_mod_of.pack(side='left',padx=5)
        self.btn_mod_of=Button(frame_modificar_oferta,justify=CENTER,text='Modificar Oferta.',
                              command=self.modificar_oferta)
        self.btn_mod_of.pack(side='left',padx=5)
        
        
        self.root.withdraw()
    def modificar_oferta(self):
        oferta=self.entry_ofertas_mod_of.get()
        oferta_new=self.entry_nuevo_nombre_mod_of.get()
        crear_evento('Modificacion oferta',Productos.loc[Productos['PRODUCTO']==oferta].index.values[0]
                     ,None,None,None,None,oferta,oferta_new)
        if oferta=='' or oferta_new=='' :
            messagebox.showinfo('Error','Seleccione oferta e ingrese un nuevo nombre.')
            return
        dic_oferta_old=Ofertas[oferta]
        Ofertas.pop(oferta)
        Productos.loc[Productos['PRODUCTO']==oferta,'PRODUCTO']=oferta_new
        Ofertas[oferta_new]=dic_oferta_old
        
        
        self.lista_ofertas=list([ prod for prod in Productos['PRODUCTO'] if prod in Ofertas])
        self.entry_ofertas_mod_of['values']=self.lista_ofertas
        messagebox.showinfo('Modificacipón oferta','Oferta Modificada exitosamente.')
        self.tabla_productos.tableChanged()
        
    def agregar_producto(self):
        producto=self.entry_nomb_prod.get()
        descripcion=self.entry_descripcion.get()
        cantidad=self.entry_cantidad.get()
        precio=self.entry_precio.get()

        if producto=='':
            self.texto_resultado.set('Nombre del producto invalido.')
            return 
        if cantidad.isdigit()==False:
            self.texto_resultado.set('La cantidad debe ser un número entero.')
            return 
        cantidad=int(cantidad)
        if precio.isdigit()==False:
            self.texto_resultado.set('El precio debe ser un número entero.')
            return 
        precio=int(precio)
        crear_producto(producto,descripcion,cantidad,precio)
        self.texto_resultado.set('Producto agregado exitosamente.')
        self.productos_menos_ofertas= list([ prod for prod in Productos['PRODUCTO'] if prod not in Ofertas])
        self.entry_producto_mod['values']=self.productos_menos_ofertas
        self.entry_prod_oferta['values']=self.productos_menos_ofertas
        self.tabla_productos.tableChanged()
    def modificar_prod(self):
        producto=self.entry_producto_mod.get()
        if producto=='':
            return
        precio=self.entry_precio_mod.get()
        cantidad=self.entry_cantidad_mod.get()
        if precio.isdigit():
            precio=int(precio)
        elif precio=='':
            precio=None
        else:
            return
        if cantidad.isdigit():
            cantidad=int(cantidad)
        elif cantidad=='':
            cantidad=None
        else:
            return
        if precio is None and cantidad is None:
            return 
        id_product=Productos.loc[Productos['PRODUCTO']==producto].index.values[0]
        modificar_producto(id_product,cantidad,precio)
        messagebox.showinfo('Modificación producto.','Producto modificado exitosamente.')
        self.tabla_productos.tableChanged()
    def agregar_oferta(self):
        if self.lista_productos_oferta:
            nombre_oferta=self.entry_nombre_oferta.get()
            precio=self.entry_precio_oferta.get()
            if nombre_oferta=='':
                return
            if precio.isdigit():
                precio=int(precio)
            else:
                return
            crear_oferta(nombre_oferta,self.lista_productos_oferta,precio)

            self.txt_oferta.set('Oferta agregada exitosamente.')
            self.tabla_productos.tableChanged()
            self.lista_productos_oferta={}
            
    def agregar_prod_oferta(self):
            
        prod=self.entry_prod_oferta.get()
        cantidad=self.entry_cantidad_oferta.get()
        if prod=='':
            return
        if cantidad.isdigit():
            cantidad=int(cantidad)
        else:
            return
        self.lista_productos_oferta[prod]=cantidad
        str_txt_oferta='Resumen Oferta:\n'
        for prod in self.lista_productos_oferta:
            str_txt_oferta=str_txt_oferta+prod+':'+str(self.lista_productos_oferta[prod])+'\n'
        self.txt_oferta.set(str_txt_oferta)
        

class Programa:
    def __init__(self):
        self.bg_color='black'
        self.root = Tk()###El padre
        
        
        self.imagen= Image.open("BannerTheGoodLife.jpeg")
        self.imagen=ImageTk.PhotoImage(self.imagen)
        self.root.title('Super Panda Admin.')
        self.root.geometry('1000x500')
        self.root.configure(background=self.bg_color)
        self.root.state('zoomed')
        # Show image using label
        self.label_imagen= Label( self.root, image = self.imagen,background='black')
        self.label_imagen.pack(padx=1,pady=1)
        
        self.text_archivo=StringVar()
        self.text_archivo.set('Seleccione una operación')
        self.label_archivo=Label(self.root, textvariable=self.text_archivo,justify=CENTER,bg='blue',fg='white')
        self.label_archivo.pack(fill='x',expand=True,padx=20,pady=5)
        
        self.boton_nueva_venta = Button(self.root, text='Nueva Venta', 
                                        command=self.nueva_venta, justify=CENTER)
        self.boton_nueva_venta.pack(fill='x',expand=True,padx=20,pady=5)
        
        self.boton_eliminar_venta = Button(self.root, text='Eliminar Venta', 
                                        command=self.eliminar_venta, justify=CENTER)
        
        self.boton_eliminar_venta.pack(fill='x',expand=True,padx=20,pady=5)
        
        self.boton_gestionar_prods = Button(self.root,text='Gestionar producto',command=self.gestionar_prods,
                                            justify=CENTER)
        self.boton_gestionar_prods.pack(fill='x',expand=True,padx=20,pady=5)
        
        self.boton_ver_tablas=Button(self.root,text='Ver Tablas',command=self.ver_tablas,justify=CENTER)
        self.boton_ver_tablas.pack(fill='x',expand=True,padx=20,pady=5)
        
        
        self.boton_ver_detalle_venta=Button(self.root,text='Ver Detalle Venta',command=self.ver_detalle_venta,
                                           justify=CENTER)
        self.boton_ver_detalle_venta.pack(fill='x',expand=True,padx=20,pady=5)
        
        self.boton_crear_guia_despacho=Button(self.root,text='Guía despachos',command=self.crear_guia_despacho,
                                             justify=CENTER)
        self.boton_crear_guia_despacho.pack(fill='x',expand=True,padx=20,pady=5)
        
        self.boton_crear_reporte= Button(self.root,text='Crear reporte',command=self.crear_reporte,
                                            justify=CENTER)
        self.boton_crear_reporte.pack(fill='x',expand=True,padx=20,pady=5)
        self.boton_salir= Button(self.root,text='Salir',command=self.crear_reporte,
                                            justify=CENTER)
        self.boton_crear_reporte.pack(fill='x',expand=True,padx=20,pady=5)
    def crear_guia_despacho(self):
        ventana=Ventana_guia_despachos(self.root,self.bg_color)
    def ver_detalle_venta(self):
        ventana=Ventana_detalles_venta(self.root,self.bg_color)
    def ver_tablas(self):
        ventana=Ventana_tablas(self.root,self.bg_color)
    def eliminar_venta(self):
        ventana=Ventana_eliminar_venta(self.root,self.bg_color)
        
    def nueva_venta(self):
        ventana=Ventana_nueva_venta(self.root,self.bg_color)
    def gestionar_prods(self):
        ventana=Ventana_gestionar_prods(self.root,self.bg_color)
    def crear_reporte(self):
        pass

    

programa=Programa()
programa.root.mainloop()
Productos.to_csv(path_Productos, encoding='utf-8')
Ventas.to_csv(path_Ventas, encoding='utf-8')
Despachos.to_csv(path_Despachos, encoding='utf-8')
with open(path_Ofertas, 'wb') as file:
    pickle.dump(Ofertas, file)
with open(path_Lista_Ventas, 'wb') as file:
    pickle.dump(Lista_Ventas, file)