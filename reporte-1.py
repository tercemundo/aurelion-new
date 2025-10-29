import pandas as pd
import os
from colorama import init, Fore, Style
import graficos  # <-- IMPORTAMOS EL NUEVO MÓDULO

# --- Configuración ---
ARCHIVOS = {
    'clientes': 'Aurelion/clientes.xlsx',
    'ventas': 'Aurelion/ventas.xlsx',
    'detalle': 'Aurelion/detalle_ventas.xlsx',
    'productos': 'Aurelion/productos.xlsx'
}

COLUMNAS = {
    'cliente_id': 'id_cliente',
    'cliente_nombre': 'nombre_cliente',
    'cliente_email': 'email',
    'venta_id': 'id_venta',
    'venta_medio_pago': 'medio_pago',
    'fecha': 'fecha', # Añadido para el gráfico por día
    'detalle_venta_id': 'id_venta',
    'detalle_producto_id': 'id_producto',
    'detalle_cantidad': 'cantidad',
    'producto_id': 'id_producto',
    'producto_nombre': 'nombre_producto',
    'producto_precio': 'precio_unitario',
    'producto_categoria': 'categoria'
}
# --------------------

def imprimir_banner():
    banner = r"""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║   ████████╗██╗███████╗███╗   ██╗██████╗  █████╗                  ║
    ║   ╚══██╔══╝██║██╔════╝████╗  ██║██╔══██╗██╔══██╗                 ║
    ║      ██║   ██║█████╗  ██╔██╗ ██║██║  ██║███████║                 ║
    ║      ██║   ██║██╔══╝  ██║╚██╗██║██║  ██║██╔══██║                 ║
    ║      ██║   ██║███████╗██║ ╚████║██████╔╝██║  ██║                 ║
    ║      ╚═╝   ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝                 ║
    ║                                                                   ║
    ║        █████╗ ██╗   ██╗██████╗ ███████╗██╗     ██╗ ██████╗ ███╗ ║
    ║       ██╔══██╗██║   ██║██╔══██╗██╔════╝██║     ██║██╔═══██╗████╗║
    ║       ███████║██║   ██║██████╔╝█████╗  ██║     ██║██║   ██║██╔██║
    ║       ██╔══██║██║   ██║██╔══██╗██╔══╝  ██║     ██║██║   ██║██║╚█║
    ║       ██║  ██║╚██████╔╝██║  ██║███████╗███████╗██║╚██████╔╝██║ ╚║
    ║       ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ║
    ║                                                                   ║
    ║              Sistema de Gestión de Ventas v1.0                   ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    print(Fore.CYAN + banner + Style.RESET_ALL)

def print_titulo(texto):
    print("\n" + Style.BRIGHT + Fore.YELLOW + "--- " + texto.upper() + " ---" + Style.RESET_ALL)

def cargar_y_verificar_datos():
    dfs = {}
    print_titulo("Cargando y Verificando Datos")
    for nombre, ruta in ARCHIVOS.items():
        if not os.path.exists(ruta):
            print(Fore.RED + "Error: El archivo '" + ruta + "' no se encontró." + Style.RESET_ALL)
            return None
        dfs[nombre] = pd.read_excel(ruta)
        print(Fore.GREEN + "Archivo '" + ruta + "' cargado correctamente." + Style.RESET_ALL)

    columnas_requeridas = {
        'clientes': [COLUMNAS['cliente_id'], COLUMNAS['cliente_nombre'], COLUMNAS['cliente_email']],
        'ventas': [COLUMNAS['venta_id'], COLUMNAS['cliente_id'], COLUMNAS['venta_medio_pago'], COLUMNAS['fecha']],
        'detalle': [COLUMNAS['detalle_venta_id'], COLUMNAS['detalle_producto_id'], COLUMNAS['detalle_cantidad']],
        'productos': [COLUMNAS['producto_id'], COLUMNAS['producto_nombre'], COLUMNAS['producto_precio'], COLUMNAS['producto_categoria']]
    }
    todo_ok = True
    for nombre_df, df in dfs.items():
        columnas_faltantes = [col for col in columnas_requeridas.get(nombre_df, []) if col not in df.columns]
        if columnas_faltantes:
            print("\n" + Fore.RED + "--- ¡ERROR DE CONFIGURACIÓN! ---" + Style.RESET_ALL)
            print("En el archivo '" + ARCHIVOS[nombre_df] + "', no se encontraron las siguientes columnas esperadas: " + Fore.YELLOW + str(columnas_faltantes) + Style.RESET_ALL)
            print(Fore.CYAN + "Las columnas que SÍ se encontraron son: " + str(df.columns.tolist()) + Style.RESET_ALL)
            print("Por favor, corrige los nombres en la sección 'COLUMNAS' del script.")
            todo_ok = False
    if not todo_ok:
        return None
    print("\n" + Fore.GREEN + "Todos los archivos y columnas han sido verificados con éxito." + Style.RESET_ALL)
    return dfs

def analizar_productos(df_detalle, df_productos):
    print_titulo("1. Análisis de Productos Más y Menos Vendidos")
    ventas_por_producto = df_detalle.groupby(COLUMNAS['detalle_producto_id'])[COLUMNAS['detalle_cantidad']].sum()
    df_productos_idx = df_productos.set_index(COLUMNAS['producto_id'])
    reporte_productos = ventas_por_producto.to_frame().join(df_productos_idx[COLUMNAS['producto_nombre']])
    mas_vendido = reporte_productos.nlargest(1, COLUMNAS['detalle_cantidad'])
    print("Producto más vendido: " + Fore.GREEN + str(mas_vendido.iloc[0][COLUMNAS['producto_nombre']]) + Style.RESET_ALL)
    print("Unidades vendidas: " + Fore.GREEN + str(int(mas_vendido.iloc[0][COLUMNAS['detalle_cantidad']])) + Style.RESET_ALL)
    menos_vendido = reporte_productos.nsmallest(1, COLUMNAS['detalle_cantidad'])
    print("\nProducto menos vendido: " + Fore.YELLOW + str(menos_vendido.iloc[0][COLUMNAS['producto_nombre']]) + Style.RESET_ALL)
    print("Unidades vendidas: " + Fore.YELLOW + str(int(menos_vendido.iloc[0][COLUMNAS['detalle_cantidad']])) + Style.RESET_ALL)

def analizar_clientes(dfs):
    df_clientes, df_ventas = dfs['clientes'], dfs['ventas']
    print_titulo("2. Top 10 Clientes por Número de Compras")
    compras_por_cliente = df_ventas[COLUMNAS['cliente_id']].value_counts().nlargest(10)
    top_10_ids = compras_por_cliente.index
    df_clientes_idx = df_clientes.set_index(COLUMNAS['cliente_id'])
    top_10_clientes = df_clientes_idx.loc[top_10_ids][[COLUMNAS['cliente_nombre']]].join(compras_por_cliente.to_frame(name='conteo_compras'))
    print(top_10_clientes)
    print_titulo("3. Clientes con Cero Compras")
    clientes_con_compras = df_ventas[COLUMNAS['cliente_id']].unique()
    clientes_sin_compras = df_clientes[~df_clientes[COLUMNAS['cliente_id']].isin(clientes_con_compras)]
    if not clientes_sin_compras.empty:
        print(f"Se encontraron {len(clientes_sin_compras)} clientes sin compras. Contactos:")
        for index, row in clientes_sin_compras.iterrows():
            print(f"  - {row[COLUMNAS['cliente_nombre']]} - {row[COLUMNAS['cliente_email']]}")
    else:
        print("Todos los clientes han realizado al menos una compra.")
    return top_10_ids

def analizar_medio_de_pago(df_ventas):
    print_titulo("4. Análisis de Medios de Pago")
    conteo_pagos = df_ventas[COLUMNAS['venta_medio_pago']].value_counts()
    mas_usado = conteo_pagos.index[0]
    menos_usado = conteo_pagos.index[-1]
    print("Medio de pago más utilizado: " + Fore.GREEN + mas_usado + Style.RESET_ALL + f" ({conteo_pagos.iloc[0]} veces)")
    print("Medio de pago menos utilizado: " + Fore.YELLOW + menos_usado + Style.RESET_ALL + f" ({conteo_pagos.iloc[-1]} veces)")

def calcular_ticket_promedio(top_10_ids, dfs):
    print_titulo("5. Ticket Promedio del Top 10 Clientes")
    df_ventas, df_detalle, df_productos = dfs['ventas'], dfs['detalle'], dfs['productos']
    df_detalle = pd.merge(df_detalle, df_productos[[COLUMNAS['producto_id'], COLUMNAS['producto_precio']]], left_on=COLUMNAS['detalle_producto_id'], right_on=COLUMNAS['producto_id'], suffixes=[
'_detalle', '_producto'])
    precio_col = COLUMNAS['producto_precio'] + '_producto' if COLUMNAS['producto_precio'] + '_producto' in df_detalle.columns else COLUMNAS['producto_precio']
    df_detalle['valor_linea'] = df_detalle[COLUMNAS['detalle_cantidad']] * df_detalle[precio_col]
    valor_por_venta = df_detalle.groupby(COLUMNAS['detalle_venta_id'])['valor_linea'].sum().to_frame(name='valor_total_venta')
    ventas_con_valor = pd.merge(df_ventas, valor_por_venta, left_on=COLUMNAS['venta_id'], right_index=True)
    ventas_top_10 = ventas_con_valor[ventas_con_valor[COLUMNAS['cliente_id']].isin(top_10_ids)]
    ticket_promedio = ventas_top_10.groupby(COLUMNAS['cliente_id'])['valor_total_venta'].mean().to_frame(name='ticket_promedio')
    df_clientes_idx = dfs['clientes'].set_index(COLUMNAS['cliente_id'])
    reporte_ticket = df_clientes_idx.loc[ticket_promedio.index][[COLUMNAS['cliente_nombre']]].join(ticket_promedio)
    reporte_ticket['ticket_promedio'] = reporte_ticket['ticket_promedio'].map('{:,.2f} €'.format)
    print(reporte_ticket)

def ejecutar_reporte():
    dfs = cargar_y_verificar_datos()
    if dfs is None:
        return
    try:
        analizar_productos(dfs['detalle'], dfs['productos'])
        top_10_ids = analizar_clientes(dfs)
        analizar_medio_de_pago(dfs['ventas'])
        calcular_ticket_promedio(top_10_ids, dfs)
        print_titulo("Reporte Finalizado")
    except Exception as e:
        print("\n" + Fore.RED + "Ocurrió un error inesperado: " + str(e) + Style.RESET_ALL)
        print("Verifica que los nombres de las columnas en la sección de configuración son correctos.")

def mostrar_explicacion():
    print_titulo("Explicación del Sistema")
    print("Este sistema analiza los datos de ventas para proveer un reporte completo que incluye:")
    print("- El producto más y menos vendido.")
    print("- El top 10 de clientes con más compras.")
    print("- Un listado de clientes que nunca han comprado.")
    print("- El método de pago más y menos frecuente.")
    print("- El gasto promedio por compra para el top 10 de clientes.")

def mostrar_creditos():
    print_titulo("Créditos")
    print("Generado por Marcelo Guazzardo")

def iniciar_menu():
    init(autoreset=True)
    imprimir_banner()
    while True:
        print("\n" + Fore.GREEN + Style.BRIGHT + "Menú Principal" + Style.RESET_ALL)
        print("1. Explicación del sistema")
        print("2. Generar reporte de ventas")
        print("3. Créditos")
        print("4. Generar Gráfico")
        print("5. Salir")

        opcion = input("\nSelecciona una opción: ")

        if opcion == '1':
            mostrar_explicacion()
        elif opcion == '2':
            ejecutar_reporte()
        elif opcion == '3':
            mostrar_creditos()
        elif opcion == '4':
            graficos.iniciar_menu_graficos(ARCHIVOS, COLUMNAS, print_titulo)
        elif opcion == '5':
            print("\nSaliendo del sistema. ¡Hasta pronto!")
            break
        else:
            print("\n" + Fore.RED + "Opción no válida. Por favor, intenta de nuevo." + Style.RESET_ALL)

if __name__ == "__main__":
    iniciar_menu()
