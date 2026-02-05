from conexion_base import conectar_bd

mi_conexion = conectar_bd()

if mi_conexion:
    cursor = mi_conexion.cursor()
    
    print("\n--- INICIO DE SESIÓN ---")
    usuario = input("Nombre_Usuario: ")
    contraseña = input("Contraseña: ")
    query = 'SELECT Rol FROM Usuarios WHERE Nombre_Usuario = ? AND Contraseña = ?'
    cursor.execute(query, (usuario, contraseña))
    resultado = cursor.fetchone()

    if resultado:
        rol = resultado[0]
        print(f"\nBienvenido, {usuario}. Tu rol es: {rol}")
        if rol == 'Administrador':
            print("Acceso completo concedido.")
        elif rol == 'Vendedor':
            print("Acceso limitado concedido.")
        elif rol == 'Inventario':
            print("Acceso a inventario concedido.")
        else:
            print("Rol no reconocido. Acceso denegado.")

        # --- Vamos a hacer el menú ---
        continuar = True
        while continuar:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1. Ver productos")
            print("2. Agregar producto")
            print("3. Eliminar producto")
            print("4. Actualizar producto")
            print("5. Ventas")
            print("6. Buscar producto")
            print("7. Historial de ventas")
            print("8. Salir")
            opcion = input("Seleccione una opción: ")

            if opcion == '1':
                cursor.execute('SELECT * FROM Productos')
                productos = cursor.fetchall()

                print("\n" + "=" * 80)
                print("\n--- LISTA DE PRODUCTOS ---")
                print("\n" + "=" * 80)
                print(f"{'ID':<5} | {'Producto':<20} | {'Stock':<10} | {'Caracteristica':<15} | {'Precio':<10}")
                print("-" * 80)
                
                for p in productos:
                    p_limpio = [str(dato) if dato is not None else '---' for dato in p]
                    alerta_stock = ""
                    try:
                        stock_int = int(p[2])
                        if stock_int < 5:
                            alerta_stock = " ¡Stock bajo!"
                    except (ValueError, TypeError):
                        alerta_stock = ""
                    print(f"{p_limpio[0]:<5} | {p_limpio[1]:<20} | {p_limpio[2]:<10} | {p_limpio[3]:<15} | {p_limpio[4]:<10}{alerta_stock}")
                    print("-" * 80)
                
            elif opcion == '2':
                if rol in ['Administrador', 'Inventario']:
                    print("\n--- AGREGAR PRODUCTO ---")
                    nombre_producto = input("Nombre del producto: ")
                    try:
                        precio = float(input("Precio del producto: "))
                        cantidad = int(input("Cantidad del producto: "))
                        caracteristica = input("Característica del producto (opcional): ")
                        cursor.execute(
                            'INSERT INTO Productos (Nombre, Precio, Stock, Caracteristica) VALUES (?, ?, ?, ?)',
                            (nombre_producto, precio, cantidad, caracteristica)
                        )
                        mi_conexion.commit()
                        print("Producto agregado exitosamente.")
                    except ValueError:
                        print("Error: Precio debe ser un número y Cantidad debe ser un entero.")
                else:
                    print("Acceso denegado. Solo los administradores pueden agregar productos.")

            elif opcion == '3':
                if rol == 'Administrador':
                    print("\n--- ELIMINAR PRODUCTO ---")
                    try:
                        id_producto = input("ID del producto a eliminar: ")
                        cursor.execute('SELECT * FROM Productos WHERE ID_Producto = ?', (id_producto,))
                        producto = cursor.fetchone()

                        if producto:
                            confirmacion = input(f"¿Está seguro de que desea eliminar el producto '{producto[0]}'? (S/N): ")

                            if confirmacion.upper() == 'S':
                                cursor.execute('DELETE FROM Productos WHERE ID_Producto = ?', (id_producto,))
                                mi_conexion.commit()
                                print("Producto eliminado exitosamente.")
                            else:
                                print("Eliminación cancelada.")
                        else:
                            print("ID Producto no encontrado.")
                    except ValueError:
                        print("Error: Debe ingresar un ID válido.")
                else:
                    print("Acceso denegado. Solo los administradores pueden eliminar productos.")

            elif opcion == '4':
                if rol in ['Administrador', 'Inventario']:
                    print("\n--- ACTUALIZAR PRODUCTO ---")
                    try:
                        id_producto = input("ID del producto a actualizar: ")
                        cursor.execute('SELECT * FROM Productos WHERE ID_Producto = ?', (id_producto,))
                        producto = cursor.fetchone()

                        if producto:
                            print(f"Producto actual: {producto[0]}, Precio: {producto[1]}, Stock: {producto[2]}")
                            nuevo_precio = float(input("Nuevo precio del producto: "))
                            nueva_cantidad = int(input("Nueva cantidad del producto: "))
                            cursor.execute(
                                'UPDATE Productos SET Precio = ?, Stock = ? WHERE ID_Producto = ?',
                                (nuevo_precio, nueva_cantidad, id_producto)
                            )
                            mi_conexion.commit()
                            print("Producto actualizado exitosamente.")
                        else:
                            print("ID Producto no encontrado.")
                    except ValueError:
                        print("Error: Debe ingresar un ID válido, un precio numérico y una cantidad entera.")
                else:
                    print("Acceso denegado. Solo los administradores pueden actualizar productos.")

            elif opcion == '5':
                if rol in ['Administrador', 'Vendedor']:
                    print("\n--- REGISTRAR VENTA ---")
                    try:
                        id_producto = input("ID del producto vendido: ")
                        cantidad_vendida = int(input("Cantidad vendida: "))
                        cliente = input("Nombre del cliente: ")
                        metodo = input("Método de pago: ")
                        cursor.execute('SELECT Id_Producto, Stock, Precio FROM Productos WHERE ID_Producto = ?', (id_producto,))
                        producto = cursor.fetchone()

                        if producto:
                            nombre_producto, stock_actual, precio = producto[0], producto[1], producto[2]
                            if cantidad_vendida <= stock_actual:
                                total_precio = precio * cantidad_vendida
                                nuevo_stock = stock_actual - cantidad_vendida
                                cursor.execute(
                                    'INSERT INTO Ventas (ID_Producto, Cantidad_Vendida, Cliente, Metodo_Pago, Total_Precio, Estado_Pago) VALUES (?, ?, ?, ?, ? ,?)',
                                    (id_producto, cantidad_vendida, cliente, metodo, total_precio, 'Pagado'))
                                cursor.execute(
                                    'UPDATE Productos SET Stock = ? WHERE ID_Producto = ?',
                                    (nuevo_stock, id_producto))

                                mi_conexion.commit()
                                print("Venta registrada exitosamente.")
                            else:
                                print("Error: Stock insuficiente para completar la venta.")
                        else:
                            print("ID Producto no encontrado.")
                    except ValueError:
                        print("Error: Debe ingresar un ID válido y una cantidad entera.")

            elif opcion == '6':
                print("\n--- BUSCAR PRODUCTO ---")
                termino = input("Que buscas?: ").strip()
                query = """ SELECT * FROM Productos WHERE CAST(ID_Producto AS VARCHAR) = ? OR Nombre LIKE ? OR Caracteristica LIKE ?"""
                like_termino = f"%{termino}%"
                cursor.execute(query, (termino, like_termino, like_termino))
                resultados = cursor.fetchall()

                if resultados:
                    print("\n" + "=" * 80)
                    print("\n--- RESULTADOS DE LA BÚSQUEDA ---")
                    print("\n" + "=" * 80)
                    print(f"{'ID':<5} | {'Producto':<20} | {'Stock':<10} | {'Caracteristica':<15} | {'Precio':<10}")
                    print("-" * 80)
                    
                    for p in resultados:
                        p_limpio = [str(dato) if dato is not None else '---' for dato in p]
                        alerta_stock = ""
                        try:
                            stock_int = int(p[2])
                            if stock_int < 5:
                                alerta_stock = " ¡Stock bajo!"
                        except (ValueError, TypeError):
                            alerta_stock = ""
                        print(f"{p_limpio[0]:<5} | {p_limpio[1]:<20} | {p_limpio[2]:<10} | {p_limpio[3]:<15} | {p_limpio[4]:<10} | {alerta_stock}")
                        print("-" * 80)
                else:
                    print("No se encontraron productos que coincidan con la búsqueda.")

            elif opcion == '7':
                if rol in ['Administrador', 'Inventario']:
                    print("\n--- HISTORIAL DE VENTAS ---")
                    cursor.execute('SELECT * FROM Ventas')
                    ventas = cursor.fetchall()

                    print("\n" + "=" * 100)
                    print("\n--- LISTA DE VENTAS ---")
                    print("\n" + "=" * 100)
                    print(f"{'ID':<6} | {'ID Prod':<11} | {'Cliente':<15} | {'Cant':<8} | {'Total':<10} | {'Método':<15} | {'Estado Pago':<10}")
                    print("-" * 100)
                    
                    for v in ventas:
                        v_limpio = [str(dato) if dato is not None else '---' for dato in v]
                        print(f"{v_limpio[0]:<6} | {v_limpio[1]:<11} | {v_limpio[2]:<15} | {v_limpio[3]:<8} | {v_limpio[4]:<10} | {v_limpio[5]:<15} | {v_limpio[6]:<10}")
                        print("-" * 100)

                else:
                    print("Acceso denegado. Solo administradores e inventario pueden ver el historial de ventas.")

            elif opcion == '8':
                print("Saliendo del sistema. ¡Hasta luego!")
                continuar = False

    else:
        print("Nombre de usuario o contraseña incorrectos. Acceso denegado.")
                
    mi_conexion.close()