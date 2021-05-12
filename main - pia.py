import sys
import os
import datetime
import time
import sqlite3
from sqlite3 import Error
import pandas as pd
import re
#Librerías

#Inicialización de variables
respuesta = 1
resultado = 1
exportar = 1
monto_total = 0.00
suma_ventas = 0.00
clave_calculada = 0
cant_articulos = 0

fecha_aceptada = False

#Tuplas
encabezados = ("No. Venta", "Monto", "Fecha")
art_encabezados = ("Clave", "Articulo", "Precio", "Existencia")
det_encabezados =  ("Clave", "Articulo", "Cantidad", "Precio", "Subtotal")

#Diccionarios
ventas_dic = {}
venta_dic = {}
estructuraArticulo = {}

#Listas
lista_subtotales = []

#Strings
captura = ""

# Validador de expresiones regulares
# _txt es el texto a validar. _regex es el patrón de expresión regular a validar.
def RegEx(_txt,_regex):
    coincidencia=re.match(_regex, _txt)
    return bool(coincidencia)

#Función del Menú para que se ejecute cada vez al termino de cada opción
def menuPrincipal():
    print("__________________________________________________")
    print("\n          *** Cosméticos True:BEAUTY! ***       ")
    print("\n            Menú principal           ")
    print("   [1] Registrar una venta.")
    print("   [2] Consultar una venta.")
    print("   [3] Obtener un reporte de ventas\n       para una fecha en específico.")
    print("   [X] Salir.")
    print("__________________________________________________\n")

#Función que muestra el catálogo de articulos
def mostrarCatalogo():
    try:
        with sqlite3.connect("CosmetiqueríaFinal.db") as conn:
            mi_cursor = conn.cursor()
            global cant_articulos
            mi_cursor.execute("SELECT id_articulo, descripcion, precio FROM articulos WHERE existencia > 0;")
            articulos = mi_cursor.fetchall()

            print(f"{art_encabezados[0]}\t{art_encabezados[1]}\t{art_encabezados[2]}")
            print("----------------------------------------")

            for sku, nombre, precio in articulos:
                print(f"{sku}\t", end="")
                print(f"{nombre}\t", end="")
                print("${:.2f}" .format(precio) + " mxn")
                estructuraArticulo[sku] = {"Sku":sku, "Descripcion":nombre, "Precio":precio}
                cant_articulos += 1
            print("----------------------------------------")
    except Error as e:
        print (e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        conn.close()

# Función que valida un dato, y si es correcto, lo coloca en captura. RegEx por función.
def validarDatos(_patron,_pregunta="Dame un dato: "):
    # Se especifica que captura es global.
    global captura
    while True:
        _fxvalor = input(_pregunta)
        coincide = re.search(_patron, _fxvalor)
        if (coincide):
            captura = _fxvalor
            break
        else:
            print("*** El dato no es correcto. Intenta de nuevo. ***")

# Función que valida una respuesta, y si es correcto, lo coloca en resultado. RegEx por función.
def validarPregunta(_patron,_pregunta="Dame un dato: "):
    global resultado
    while True:
        _fxvalor = input(_pregunta)
        coincide = re.search(_patron, _fxvalor)
        if (coincide):
            resultado = int(_fxvalor)
            break
        else:
            print("*** La respuesta no es correcta. Intenta de nuevo. ***")

#Función que inserta los detalles de una venta en una tabla relacionada
def detalleVenta():
    try:
        with sqlite3.connect("CosmetiqueríaFinal.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
            mi_cursor = conn.cursor()

            global clave_calculada
            mi_cursor.execute("SELECT COUNT(id_venta) FROM ventas;")
            claves_contadas = mi_cursor.fetchone() #fetchone()
            clave_calculada = int(''.join(map(str, claves_contadas)))
            clave_calculada += 1

            valores = {"folio":clave_calculada, "sku":id_selected, "cantidad":cant_pzas}
            mi_cursor.execute("INSERT INTO detalle_venta VALUES(:folio,:sku,:cantidad);", valores)

            print("Articulo agregado al carrito")
    except Error as e:
        print (e)
    except:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
    finally:
        conn.close()

while (True):
    menuPrincipal()
    opcion = input("¿Qué opción deseas?: ")
    respuesta = 1
    if RegEx(opcion,"^[123xX0]{1}$"):
        if opcion=="1":
            while respuesta == 1:
                print("\nCatálogo - Piezas existentes: ")
                mostrarCatalogo()
                validarPregunta(r"^[1-9]{1}[0-9]{0,}$","\n¿Cuántos articulos se registrarán?: ")
                cant_datos = resultado
                for dato in range(cant_datos):
                    while True:
                        validarPregunta(r"^[1-9]{1}[0-9]{0,}$","\nSelecciona la clave del articulo: ")
                        if resultado <= cant_articulos:
                            sku_selected = resultado
                            break
                        else:
                            print(f"*** Por ahora solo contamos con {cant_articulos} productos en el catálogo. ***\n*** Intenta de nuevo. ***")

                    validarPregunta(r"^[1-9]{1}[0-9]{0,}$","Cantidad de piezas: ")
                    cant_pzas = resultado

                    for i in estructuraArticulo:
                        if estructuraArticulo[i]["Sku"] == sku_selected:
                            id_selected = estructuraArticulo[i]["Sku"]
                            precio_venta = estructuraArticulo[i]["Precio"]
                            subtotal = round(cant_pzas * precio_venta, 2)
                            lista_subtotales.append(subtotal)
                            detalleVenta()
                monto_total = sum(lista_subtotales)
                lista_subtotales = []

                # while not fecha_aceptada:
                #     try:
                #         fecha_actual = datetime.date.today()
                #         fecha_capturada = (input("\nIngresa la fecha en que se realiza la venta (dd/mm/aaaa): "))
                #         fecha_capturada = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
                #         if fecha_capturada <= fecha_actual:
                #             fecha_aceptada = True
                #         else:
                #             print("*** Ingresa una fecha no mayor al día de hoy. Intenta de nuevo ***")
                #             fecha_aceptada = False
                #     except ValueError:
                #         print("*** La fecha proporcionada no se encuentra en el formato indicato, favor de corregir. ***")

                fecha_actual = datetime.date.today()
                fecha_procesada = datetime.datetime.combine(fecha_actual, datetime.datetime.min.time())

                venta = [clave_calculada,monto_total,fecha_procesada]

                print("\nEl monto total es: ${:.2f}" .format(monto_total) + " mxn" + f"\nVenta: #{venta[0]} - Fecha captura: {venta[2]}")
                try:
                    with sqlite3.connect("CosmetiqueríaFinal.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                        mi_cursor = conn.cursor()
                        valores = {"folio":clave_calculada, "monto":monto_total, "fecha_procesada":fecha_procesada}
                        mi_cursor.execute("INSERT INTO ventas VALUES(:folio,:monto,:fecha_procesada);", valores)
                        print("Venta registrada exitosamente")
                except Error as e:
                    print (e)
                except:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                finally:
                    conn.close()
                validarPregunta(r"^[01]{1}$","\n¿Deseas realizar otra venta? \n (1-Si / 0-No): ")
                respuesta = resultado
                cant_articulos = 0
                subtotal = 0
                fecha_aceptada = False
            #Reseteo
            estructuraArticulo = {}
            valores = {}
            lista_subtotales = []
            venta = []
        elif opcion=="2":
            respuesta = 1
            exportar = 1
            while respuesta == 1:
                validarPregunta(r"^[1-9]{1}[0-9]{0,}$","\nDime la clave de la venta que deseas consultar: ")
                clave_buscar = resultado
                try:
                    with sqlite3.connect("CosmetiqueríaFinal.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                        mi_cursor = conn.cursor()
                        #global id_dic
                        criterios = {"folio":clave_buscar}

                        mi_cursor.execute("SELECT ven.id_venta, ven.monto, ven.fecha_registro, det.id_articulo_fk, art.descripcion, det.cantidad_comprada, art.precio, (det.cantidad_comprada * art.precio) AS SUBTOTAL \
                        FROM ventas AS ven \
                        JOIN detalle_venta AS det ON ven.id_venta = det.id_venta_fk \
                        JOIN articulos AS art ON det.id_articulo_fk = art.id_articulo \
                        WHERE ven.id_venta = :folio \
                        ORDER BY ven.id_venta;", criterios)
                        venta = mi_cursor.fetchall()

                        if venta:
                            print(f"\n{det_encabezados[0]}\t{det_encabezados[1]}\t{det_encabezados[2]}\t{det_encabezados[3]}\t\t{det_encabezados[4]}")
                            print("---------------------------------------"*2)
                        else:
                            print(f"\nNo hay registros de venta con la clave: {clave_buscar}")
                        id_dic = 0
                        for folio, monto, fecha_registro, sku, descripcion, cantidad_comprada, precio, subtotal in venta:
                            id_dic += 1
                            print(f"{sku}\t", end="")
                            print(f"{descripcion}\t\t", end="")
                            print(f"{cantidad_comprada}\t\t", end="")
                            print("${:.2f}" .format(precio)+"\t\t", end="")
                            print("${:.2f}" .format(subtotal) + " mxn")
                            venta_dic[id_dic] = {"No. Venta":folio, "Monto":monto, "Fecha":fecha_registro, "Clave":sku, "Articulo":descripcion, "Cantidad":cantidad_comprada, "Precio":precio, "Subtotal":subtotal}
                        print("---------------------------------------"*2)
                except Error as e:
                    print (e)
                except:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                finally:
                    conn.close()
                if venta:
                    print(f"\nVenta encontrada: #{folio} - Fecha de registro: {fecha_registro}")
                    print("El monto total fue: ${:.2f}" .format(monto) + " mxn")
                validarPregunta(r"^[01]{1}$","\n¿Deseas consultar otra venta? \n (1-Si / 0-No): ")
                respuesta = resultado
            if venta:
                validarPregunta(r"^[01]{1}$","\n¿Deseas exportar un reporte de dicha consulta? \n (1-Si / 0-No): ")
                exportar = resultado
                while exportar == 1:
                    print("\nExportando archivo...")
                    df_venta = pd.DataFrame(venta_dic)
                    df_venta.to_csv (r'reporte_venta.csv',index=True, header=None)
                    print("Exportación exitosa")
                    del df_venta
                    exportar = 0
            #Reseteo
            estructuraArticulo = {}
            valores = {}
            venta_dic = {}
            venta = []
        elif opcion=="3":
            respuesta = 1
            exportar = 1
            while respuesta == 1:
                while not fecha_aceptada:
                    try:
                        fecha_actual = datetime.date.today()
                        fecha_capturada = (input("\nIngresa una fecha específica para generar reporte (dd/mm/aaaa): "))
                        fecha_procesada = datetime.datetime.strptime(fecha_capturada, "%d/%m/%Y").date()
                        if fecha_procesada <= fecha_actual:
                            fecha_aceptada = True
                        else:
                            print("*** Ingresa una fecha no mayor al día de hoy. Intenta de nuevo ***")
                            fecha_aceptada = False
                    except ValueError:
                        print("*** La fecha proporcionada no se encuentra en el formato indicato, favor de corregir. ***")
                try:
                    with sqlite3.connect("CosmetiqueríaFinal.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
                        mi_cursor = conn.cursor()
                        criterios = {"fecha": fecha_procesada}
                        mi_cursor.execute("SELECT * FROM ventas WHERE DATE(fecha_registro) = :fecha;", criterios)
                        venta = mi_cursor.fetchall()

                        if venta:
                            print(f"\n{encabezados[0]}\t{encabezados[1]}\t\t{encabezados[2]}")
                            print("---------------------------------"*2)
                        else:
                            print(f"\nNo hay registros de venta con la fecha: {fecha_capturada}")

                        for folio, monto, fecha_registro in venta:
                            print(f"{folio}\t\t", end="")
                            print("${:.2f}" .format(monto) + " mxn\t", end="")
                            print(fecha_registro)
                            suma_ventas = suma_ventas + monto
                            ventas_dic[folio] = {"No. Venta":folio, "Monto":monto, "Fecha":fecha_registro}
                        print("---------------------------------"*2)
                except sqlite3.Error as e:
                    print (e)
                except Exception:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
                finally:
                    if (conn):
                        conn.close()
                if venta:
                    print(f"\nVenta realizadas: {len(ventas_dic)} en la fecha consultada: {fecha_registro}")
                    print("La suma del importe de las ventas es de: ${:.2f}" .format(suma_ventas) + " mxn")
                validarPregunta(r"^[01]{1}$","\n¿Deseas consultar otra fecha para el reporte? \n (1-Si / 0-No): ")
                respuesta = resultado
                fecha_aceptada = False
                suma_ventas = 0
            if venta:
                validarPregunta(r"^[01]{1}$","\n¿Deseas exportar el reporte de dicha consulta? \n (1-Si / 0-No): ")
                exportar = resultado
                while exportar == 1:
                    print("\nExportando archivo...")
                    df_ventas = pd.DataFrame(ventas_dic)
                    df_ventas.to_csv (r'reporte_fecha.csv',index=True, header=None)
                    print("Exportación exitosa")
                    del df_ventas
                    exportar = 0
            #Reseteo
            estructuraArticulo = {}
            valores = {}
            ventas_dic = {}
            venta = []
        elif opcion=="x" or opcion=="X":
            print("\nGracias por visitar nuestra tienda.")
            print("\n *** Cosméticos True:BEAUTY! ***       ")
            print("         ¡VUELVA PRONTO!       \n")
            break
        else:
            print ("\n*** No has pulsado ninguna opción correcta. Intenta de nuevo. ***")
    else:
        print("\n*** Esa respuesta no es válida. Intenta de nuevo. ***")
