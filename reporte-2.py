import pandas as pd
import os
from colorama import init, Fore, Style

# --- Configuración ---
# Asegúrate de que estos nombres de archivo y columnas coincidan con los tuyos.
ARCHIVOS = {
    'clientes': 'Aurelion/clientes.xlsx',
    'ventas': 'Aurelion/ventas.xlsx',
    'detalle': 'Aurelion/detalle_ventas.xlsx',
    'productos': 'Aurelion/productos.xlsx'
}

COLUMNAS = {
    # Clientes
    'cliente_id': 'id_cliente',
    'cliente_nombre': 'nombre_cliente',
    'cliente_email': 'email',
    # Ventas
    'venta_id': 'id_venta',
    'venta_medio_pago': 'medio_pago',
    # Detalle Ventas
    'detalle_venta_id': 'id_venta',
    'detalle_producto_id': 'id_producto',
    'detalle_cantidad': 'cantidad',
    # Productos
    'producto_id': 'id_producto',
    'producto_nombre': 'nombre_producto',
    'producto_precio': 'precio_unitario'
}
# --------------------

def print_titulo(texto):
    """Imprime un título resaltado."""
    #print(f"\n{Style.BRIGHT}{Fore.CYAN}--- {texto.upper()} ---""{Style.RESET_ALL})
    print(f"\n{Style.BRIGHT}{Fore.CYAN}--- {texto.upper()} ---{Style.RESET_ALL}")
def cargar_y_verificar_datos():
    """Carga todos los archivos Excel y verifica la existencia de archivos y columnas."""
    dfs = {}
    print_titulo("Cargando y Verificando Datos")

    for nombre, ruta in ARCHIVOS.items():
        if not os.path.exists(ruta):
            print(f"{Fore.RED}Error: El archivo '{ruta}' no se encontró.{Style.RESET_ALL}")
            return None
        dfs[nombre] = pd.read_excel(ruta)
        print(f"{Fore.GREEN}Archivo '{ruta}' cargado correctamente.{Style.RESET_ALL}")

    columnas_requeridas = {
        'clientes': [COLUMNAS['cliente_id'], COLUMNAS['cliente_nombre'], COLUMNAS['cliente_email']],
        'ventas': [COLUMNAS['venta_id'], COLUMNAS['cliente_id'], COLUMNAS['venta_medio_pago']],
        'detalle': [COLUMNAS['detalle_venta_id'], COLUMNAS['detalle_producto_id'], COLUMNAS['detalle_cantidad']],
        'productos': [COLUMNAS['producto_id'], COLUMNAS['producto_nombre'], COLUMNAS['producto_precio']]
    }

    todo_ok = True
    for nombre_df, df in dfs.items():
        columnas_faltantes = [col for col in columnas_requeridas.get(nombre_df, []) if col not in df.columns]
        if columnas_faltantes:
            print(f"\n{Fore.RED}--- ¡ERROR DE CONFIGURACIÓN! ---")
            print(f"En el archivo '{ARCHIVOS[nombre_df]}', no se encontraron las siguientes columnas esperadas: {Fore.YELLOW}{columnas_faltantes}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Las columnas que SÍ se encontraron son: {df.columns.tolist()}{Style.RESET_ALL}")
            print(f"Por favor, corrige los nombres en la sección 'COLUMNAS' del script.")
            todo_ok = False

    if not todo_ok:
        return None

    print(f"\n{Fore.GREEN}Todos los archivos y columnas han sido verificados con éxito.{Style.RESET_ALL}")
    return dfs

def analizar_productos(df_detalle, df_productos):
    """Determina el artículo más y menos vendido."""
    print_titulo("1. Análisis de Productos Más y Menos Vendidos")
    ventas_por_producto = df_detalle.groupby(COLUMNAS['detalle_producto_id'])[COLUMNAS['detalle_cantidad']].sum()
    
    df_productos_idx = df_productos.set_index(COLUMNAS['producto_id'])
    reporte_productos = ventas_por_producto.to_frame().join(df_productos_idx[COLUMNAS['producto_nombre']])

    mas_vendido = reporte_productos.nlargest(1, COLUMNAS['detalle_cantidad'])
    print(f"Producto más vendido: {Fore.GREEN}{mas_vendido.iloc[0][COLUMNAS['producto_nombre']]}{Style.RESET_ALL}")
    print(f"Unidades vendidas: {Fore.GREEN}{int(mas_vendido.iloc[0][COLUMNAS['detalle_cantidad']])}{Style.RESET_ALL}")

    menos_vendido = reporte_productos.nsmallest(1, COLUMNAS['detalle_cantidad'])
    print(f"\nProducto menos vendido: {Fore.YELLOW}{menos_vendido.iloc[0][COLUMNAS['producto_nombre']]}{Style.RESET_ALL}")
    print(f"Unidades vendidas: {Fore.YELLOW}{int(menos_vendido.iloc[0][COLUMNAS['detalle_cantidad']])}{Style.RESET_ALL}")

def analizar_clientes(dfs):
    """Determina los 10 clientes con más compras y los clientes con 0 compras."""
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
    """Determina el medio de pago más y menos utilizado."""
    print_titulo("4. Análisis de Medios de Pago")
    conteo_pagos = df_ventas[COLUMNAS['venta_medio_pago']].value_counts()
    
    mas_usado = conteo_pagos.index[0]
    menos_usado = conteo_pagos.index[-1]

    print(f"Medio de pago más utilizado: {Fore.GREEN}{mas_usado}{Style.RESET_ALL} ({conteo_pagos.iloc[0]} veces)")
    print(f"Medio de pago menos utilizado: {Fore.YELLOW}{menos_usado}{Style.RESET_ALL} ({conteo_pagos.iloc[-1]} veces)")

def calcular_ticket_promedio(top_10_ids, dfs):
    """Calcula el ticket promedio para los 10 mejores clientes."""
    print_titulo("5. Ticket Promedio del Top 10 Clientes")
    df_ventas, df_detalle, df_productos = dfs['ventas'], dfs['detalle'], dfs['productos']

    # Unir detalle con productos para obtener el precio canónico de la tabla de productos
    df_detalle = pd.merge(df_detalle, df_productos[[COLUMNAS['producto_id'], COLUMNAS['producto_precio']]], left_on=COLUMNAS['detalle_producto_id'], right_on=COLUMNAS['producto_id'], suffixes=['_detalle', '_producto'])
    
    # Calcular el valor de la línea usando el precio del maestro de productos (termina en _producto si hay conflicto)
    # Si no hay conflicto, pandas no añade sufijo. Por eso, verificamos la existencia de la columna con sufijo.
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

def generar_reporte_completo():
    """Función principal que orquesta todo el análisis."""
    init(autoreset=True)
    
    dfs = cargar_y_verificar_datos()
    if dfs is None:
        print(f"\n{Fore.RED}Abortando el análisis debido a errores en la carga de datos.{Style.RESET_ALL}")
        return

    try:
        analizar_productos(dfs['detalle'], dfs['productos'])
        top_10_ids = analizar_clientes(dfs)
        analizar_medio_de_pago(dfs['ventas'])
        calcular_ticket_promedio(top_10_ids, dfs)
        print_titulo("Reporte Finalizado")
    except Exception as e:
        print(f"\n{Fore.RED}Ocurrió un error inesperado durante la generación del reporte: {e}{Style.RESET_ALL}")
        print("Verifica que los nombres de las columnas en la sección de configuración son correctos.")

if __name__ == "__main__":
    generar_reporte_completo()