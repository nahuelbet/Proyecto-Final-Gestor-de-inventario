import sqlite3
import time
from colorama import Fore, Style, init
init(autoreset=True)

def conectar_bd():
    """Establece y devuelve la conexion principal con la base de datos SQLite."""
    return sqlite3.connect("inventario.db")
        

def crear_tabla():
    """Construye la estructura inicial de la base de datos (tabla productos) si aun no existe."""
    conexion = conectar_bd()

    try:
        # Usamos 'with' para que SQLite maneje el commit automáticamente al terminar
        with conexion:
            cursor = conexion.cursor()
            crear_tabla = '''
            CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT,
            precio REAL NOT NULL,
            cantidad INTEGER NOT NULL,
            categoria TEXT
            )
            '''
            cursor.execute(crear_tabla)

    except sqlite3.Error as e:
        print(f"{Fore.YELLOW}Error al crear la tabla:{Fore.RESET} {e}")
    finally:
        conexion.close()
        

def registrar_productos(nombre_prod, descripcion, precio, cantidad, categoria):
    """
    Inserta un nuevo registro de producto en la base de datos.

    Parametros:
    nombre_prod (str): El nombre o título del producto.
    descripcion (str): Detalles adicionales o caracteristicas.
    precio (float): Valor unitario del producto (acepta decimales).
    cantidad (int): El stock inicial disponible.
    categoria (str): El rubro o seccion a la que pertenece.
    """
    conexion = conectar_bd()
    try:
        with conexion:
            cursor = conexion.cursor()
            query = '''
            INSERT INTO productos (nombre, descripcion, precio, cantidad, categoria)
            VALUES (?, ?, ?, ?, ?)
            '''
            # Insertamos los datos mediante una tupla, toman el valor de los "?"
            datos = (nombre_prod, descripcion, precio, cantidad, categoria)
            cursor.execute(query, datos)
            # Efecto visual para mayor comodidad
            print(f"{Fore.CYAN}Guardando en la base de datos...")
            time.sleep(1.5)
            print(f"{Fore.GREEN + Style.BRIGHT}Producto agregado exitosamente!")
            time.sleep(1)
    except sqlite3.Error as e:
        print(f"{Fore.YELLOW}Ocurrio un error al registrar el producto: {e}")
    finally:
        conexion.close()

def mostrar():
    """Recupera y muestra en consola todos los productos registrados en el inventario."""
    conexion = conectar_bd()
    try:
        with conexion:
            cursor = conexion.cursor()
            query = '''
            SELECT * FROM productos
            '''
            cursor.execute(query)
            listado = cursor.fetchall()
            
            # Efecto visual de procesamiento
            print(f"{Fore.CYAN}Recolectando informacion...")
            time.sleep(1.2)
            
            # Atajamos el caso en que la base de datos esté vacía
            if listado:
                print(f"\n{Style.BRIGHT}Lista de productos:")
                # Desempaquetamos respetando el orden de las columnas en SQL
                for id_, name, desc, prec, cant, cat in listado:
                    print(f"ID: {id_} | Nombre: {name} | Precio: ${prec} | Cantidad: {cant} | Categoria: {cat}")
            else:
                print(f"\n{Fore.YELLOW}El inventario está vacío. No hay productos para mostrar.")
                
            input("\nEnter para continuar")

    except sqlite3.Error as e:
        print(f"{Fore.YELLOW}ERROR:{Fore.RESET}{e}")

    finally:
        conexion.close()


def actualizar_productos(id_actualizar, nuevo_precio, cantidad_actualizada):
    """
    Actualiza el precio y cantidad en stock de un producto especifico

    Parametros:
    id_actualizar (int): ID unico del producto que queremos modificar.
    nuevo_precio (float): Precio unitario actual.
    cantidad_actualizada (int): Cantidad actual en stock.
    """
    conexion = conectar_bd()
    try:
        with conexion:
            cursor = conexion.cursor()
            query = '''
            UPDATE productos
            SET precio = ?,
                cantidad = ?
            WHERE id = ?
            '''
            datos = (nuevo_precio, cantidad_actualizada, id_actualizar)
            cursor.execute(query, datos)
            print(f"{Fore.CYAN}Actualizando producto...")
            time.sleep(1.3)
            # Preguntamos si la base de datos realmente modifico algo
            if cursor.rowcount > 0:
                print(f"{Fore.GREEN}Producto actualizado con éxito!")
            else:
                print(f"{Fore.YELLOW}No se encontró ningún producto con el ID {id_actualizar}")
            time.sleep(1)
    except sqlite3.Error as e:
        print(f"{Fore.YELLOW}Ocurrio un error al actualizar los datos del producto: {e}")
    finally:
        conexion.close()

def eliminar_productos(id_eliminar):
    """
    Elimina un producto especifico de la base de datos mediante su ID.

    Parametros:
    id_eliminar (int): ID unico del producto que queremos eliminar.
    """
    conexion = conectar_bd()
    try:
        with conexion:
            cursor = conexion.cursor()
            query = '''
            DELETE FROM productos
            WHERE id = ?
            '''
            # Coma obligatoria para que SQLite lo tome como tupla
            eliminar = (id_eliminar,)
            cursor.execute(query, eliminar)
            
            print(f"{Fore.RED}Eliminando producto...")
            time.sleep(1.3)

            if cursor.rowcount > 0:
                print(f"{Fore.RED + Style.BRIGHT} Producto eliminado de la base de datos.")
            else:
                print(f"{Fore.YELLOW}El producto con ID {id_eliminar} no existe. No se borro nada.")
                
            time.sleep(1)
            
    except sqlite3.Error as e:
        print(f"{Fore.YELLOW}Ocurrio un error al eliminar el producto: {e}")
        
    finally:
        conexion.close()


def buscar_por_id(id_prod):
    """
    Busca productos en el inventario mediante ID del producto

    Parametros:
    id_prod (int): Numero que ingresa el usuario para buscar el producto  
    """
    conexion = conectar_bd()
    try:
        with conexion:
            cursor = conexion.cursor()
            query = '''
            SELECT * FROM productos
            WHERE id = ?
            '''
            # Le pasamos la tupla de un solo elemento
            cursor.execute(query, (id_prod,))
            info = cursor.fetchone()
            print(f"{Fore.CYAN}Buscando producto...")
            time.sleep(1.5)
            if info: # Validamos que el producto exista (que no sea None)
                print(f"\n{Fore.GREEN}Producto encontrado:")
                # Desempaquetamos directo, respetando el orden exacto del CREATE TABLE
                id_db, nom, descr, prec, cant, cat = info
                print(f"ID: {id_db} | Nombre: {nom} | Descripcion: {descr} | Precio: ${prec} | Cantidad: {cant} | Categoria: {cat}")
            else:
                print(f"{Fore.YELLOW}No se encontro ningun producto con ese ID.")

            input("Presiona Enter para volver al menu...")
                
    except sqlite3.Error as e:
        print(f"{Fore.YELLOW + Style.BRIGHT}Error en la base de datos: {e}")
        
    finally:
        conexion.close()

def buscar_nombre_categ(texto_busqueda):
    """
    Busca productos en el inventario filtrando por coincidencias en el nombre o la categoria.

    Parametros:
    texto_busqueda (str): La palabra o fragmento que ingresa el usuario.
    """
    conexion = conectar_bd()
    try:
        with conexion:
            cursor = conexion.cursor()
            query = '''
            SELECT * FROM productos
            WHERE nombre LIKE ? OR categoria LIKE ?
            '''
            busqueda = f"%{texto_busqueda}%"
            cursor.execute(query, (busqueda, busqueda))
            
            listado = cursor.fetchall()
            print(f"{Fore.CYAN}Buscando producto...")
            time.sleep(1.5)
            if listado:
                print(f"\n{Style.BRIGHT}Resultados de tu búsqueda:")
                for id_db, nom, descr, prec, cant, cat in listado:
                    print(f"ID: {id_db} | Nombre: {nom} | Descripcion: {descr} | Precio: ${prec} | Cantidad: {cant} | Categoria: {cat}")
            else:
                print(f"{Fore.YELLOW}No encontramos nada que coincida con '{texto_busqueda}'.")

            input("Presiona Enter para volver al menu...")
                
    except sqlite3.Error as e:
        print(f"{Fore.RED} Error al buscar: {e}")
        
    finally:
        conexion.close()


def reporte_bajo_stock(limite):
    """
    Genera un reporte de los productos que tienen un stock igual o menor al limite indicado.

    Parametros:
    limite (int): El numero maximo de unidades que se usa como filtro.
    """
    conexion = conectar_bd()
    try:
        with conexion:
            cursor = conexion.cursor()
            query = '''
            SELECT * FROM productos WHERE cantidad <= ?
            '''
            cursor.execute(query, (limite,))
            listado = cursor.fetchall()

            if listado:
                print(f"\nREPORTE: Productos con stock menor o igual a {limite}")
                for id_db, nom, descr, prec, cant, cat in listado:
                    # Lo muestro un poco más limpio, enfocándome en el stock
                    print(f"ID: {id_db} | Nombre: {nom} | STOCK ACTUAL: {cant} | Categoria: {cat}")
            else:
                print(f"\n Inventario sano. No hay productos con {limite} o menos unidades.")

            input("Presiona Enter para volver al menu...")    
                
    except sqlite3.Error as e:
        print(f"{Fore.RED}Error al generar el reporte: {e}")
        
    finally:
        conexion.close()