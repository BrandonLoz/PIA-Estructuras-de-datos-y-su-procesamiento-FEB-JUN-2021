import sys
import datetime
import sqlite3

try:
    with sqlite3.connect("CosmetiqueríaFinal.db", detect_types = sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as conn:
        mi_cursor = conn.cursor()

        mi_cursor.execute("CREATE TABLE IF NOT EXISTS articulos (\
            id_articulo INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
            descripcion TEXT NOT NULL UNIQUE,\
            precio NUMERIC NOT NULL,\
            existencia NUMERIC\
            );")

        mi_cursor.execute("CREATE TABLE IF NOT EXISTS ventas (\
            id_venta INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,\
            monto NUMERIC NOT NULL,\
            fecha_registro timestamp NOT NULL\
            );")

        mi_cursor.execute("CREATE TABLE IF NOT EXISTS detalle_venta (\
            id_venta_fk INTEGER,\
            id_articulo_fk INTEGER, \
            cantidad_comprada INTEGER NOT NULL,\
            FOREIGN KEY(id_venta_fk) REFERENCES ventas(id_venta),\
            FOREIGN KEY(id_articulo_fk) REFERENCES articulos(id_articulo)\
            );")

#         #NUEVAS Y MODIFICACIONES
#         mi_cursor.execute("CREATE TABLE IF NOT EXISTS ventas (\
#             id_venta INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,\
#             id_vendedor_fk INTEGER,\
#             monto NUMERIC NOT NULL,\
#             fecha_registro timestamp NOT NULL,\
#             FOREIGN KEY(id_vendedor_fk) REFERENCES vendedores(id_vendedor)\
#             );")
# 
#         mi_cursor.execute("CREATE TABLE IF NOT EXISTS vendedores (\
#             id_vendedor INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,\
#             nombre TEXT NOT NULL UNIQUE,\
#             password VARCHAR(100) NOT NULL\
#             );")
#         #NUEVAS Y MODIFICACIONES

        print("Tabla creada")
except sqlite3.Error as e:
    print(e)
except:
    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
finally:
    if (conn):
        conn.close()
        print("Se ha cerrado la conexión")



