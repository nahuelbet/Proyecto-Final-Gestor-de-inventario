"""
Archivo principal del Sistema de Gestion de Inventario.
Maneja la interfaz de usuario por consola.
"""
from funciones import *
from colorama import Style, Fore, init

init(autoreset=True)

def menu():
    """
    Ejecuta el bucle infinito de la interfaz. Muestra las opciones, 
    filtra la eleccion del usuario y deriva a la funcion correspondiente.
    """
    while True:
        print(f"\nMenu Principal")
        print("Seleccione una opcion:")
        print("1. Registrar productos.")
        print("2. Mostrar productos.")
        print("3. Buscar producto")
        print("4. Actualizar productos.")
        print("5. Reporte de stock")
        print("6. Eliminar productos.")
        print(f"7. {Fore.RED}Salir")

        opcion = input("Selecciona una opcion(1-7): ").strip()

        if opcion == "1":
            print(f"\n{Fore.CYAN}--- Registrar nuevo producto ---")

            nombre_prod = input("Nombre del producto a registrar: ").strip().capitalize()
            
            # Bloqueamos el string vacio de entrada para mantener limpia la base de datos
            if not nombre_prod:
                print(f"{Fore.YELLOW}No se puede dejar el campo vacio.")
                continue
                
            descripcion = input("Descripcion del producto: ").strip()
            categoria = input("Categoria: ").capitalize().strip()
            
            try:
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: $"))
                registrar_productos(nombre_prod, descripcion, precio, cantidad, categoria)
            except ValueError as e:
                print(f"{Fore.RED} ERROR {e}. {Fore.RESET}Asegurate de poner numeros validos en cada campo")

        elif opcion == "2":
            mostrar()

        elif opcion == "3":
            # Sub-menu de busqueda: usamos otro while True para atrapar al usuario aca hasta que decida salir
            while True:
                print(f"\n{Fore.CYAN}--- BUSCAR PRODUCTOS ---")
                print("1. Buscar por ID")
                print("2. Buscar por nombre o categoria")
                print("3. Volver atras(o Enter)")
                opcion = input("Opcion: ").strip()

                if opcion == "1":
                    id_a_buscar = input("ID del producto a buscar: ").strip()
                    try:
                        buscar_por_id(id_a_buscar)
                    except:
                        print(f"{Fore.YELLOW}ERROR. Producto no encontrado.")
                elif opcion == "2":
                    nombre_buscar = input("Nombre o categoria del producto a buscar: ").strip()
                    try:
                        buscar_nombre_categ(nombre_buscar)
                    except:
                        print(f"{Fore.YELLOW}ERROR. Producto no encontrado.")
                elif opcion == "3" or opcion == "":
                    # Rompemos el sub-menu para que vuelva naturalmente al menu principal
                    break
                else:
                    print("Opcion no valida")

        elif opcion == "4":
            print(f"\n{Fore.CYAN}--- Actualizar producto ---")
            pedir_id = input("ID del producto a actualizar(Enter para salir): ").strip()
            
            if pedir_id == "":
                # Usamos continue para abortar la operacion
                continue
            try:
                nuevo_precio = float(input("Precio actualizado del producto: "))
                cantidad_actualizada = int(input("Cantidad: "))
                actualizar_productos(pedir_id, nuevo_precio, cantidad_actualizada)
            except:
                print(f"{Fore.RED}ERROR. Ingrese numeros validos.")

        elif opcion == "5":
            print(f"\n{Fore.CYAN}--- Reporte de Bajo Stock ---")
            try:
                limite = int(input("Ingresa el limite de stock para el reporte (ej: 0 para ver sin stock): "))
                reporte_bajo_stock(limite)
            except ValueError:
                print(f"{Fore.RED}Error: El limite tiene que ser un numero entero.")

        elif opcion == "6":
            print(f"\n--- Eliminar producto ---")
            id_eliminar = input("ID del producto a eliminar: ").strip()
            confirmacion = input("Estas seguro? (s-n): ").strip().lower()
            
            if confirmacion == "s":
                try:
                    eliminar_productos(id_eliminar)
                except:
                    print("ERROR. ID no valido.")
            elif confirmacion == "n":
                print("Se cancelo la eliminacion del producto. Volviendo al menu...")
                continue
            else:
                print(f"{Fore.YELLOW}Opción no válida. Se canceló la eliminación.")

        elif opcion == "7":
            print("Saliendo del sistema...")
            break

        else:
            print(Style.BRIGHT + Fore.YELLOW + f"Opcion no valida")



# Evita que el menu se ejecute automaticamente si en el futuro importamos este archivo en otro script
if __name__ == "__main__":
    crear_tabla()
    menu()