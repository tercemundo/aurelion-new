import pandas as pd
import plotly.graph_objects as go
from colorama import Fore, Style

# --- Funciones de Gráficos Específicos ---

def generar_grafico_ventas_por_categoria(archivos_config, columnas_config, print_titulo_func):
    print_titulo_func("Gráfico: Ventas Totales por Categoría")
    try:
        df_detalle = pd.read_excel(archivos_config['detalle'])
        df_productos = pd.read_excel(archivos_config['productos'])
        df_merged = pd.merge(df_detalle, df_productos, left_on=columnas_config['detalle_producto_id'], right_on=columnas_config['producto_id'], suffixes=('_detalle', '_producto'))
        
        precio_col_base = columnas_config['producto_precio']
        precio_col = precio_col_base + '_producto' if precio_col_base + '_producto' in df_merged.columns else precio_col_base
        df_merged['valor_total'] = df_merged[columnas_config['detalle_cantidad']] * df_merged[precio_col]

        ventas_por_categoria = df_merged.groupby(columnas_config['producto_categoria'])['valor_total'].sum().reset_index()

        fig = go.Figure(data=[go.Bar(x=ventas_por_categoria[columnas_config['producto_categoria']], y=ventas_por_categoria['valor_total'], text=ventas_por_categoria['valor_total'].apply(lambda x: f'{x:,.2f} €'), textposition='auto')])
        fig.update_layout(title_text='Ventas Totales por Categoría de Producto', xaxis_title='Categoría', yaxis_title='Ventas Totales (€)')
        
        print("Mostrando gráfico interactivo en el navegador...")
        fig.show()
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error al generar el gráfico: {e}" + Style.RESET_ALL)

def generar_grafico_ventas_por_producto(archivos_config, columnas_config, print_titulo_func):
    print_titulo_func("Gráfico: Top 15 Productos más Vendidos")
    try:
        df_detalle = pd.read_excel(archivos_config['detalle'])
        df_productos = pd.read_excel(archivos_config['productos'])
        df_merged = pd.merge(df_detalle, df_productos, left_on=columnas_config['detalle_producto_id'], right_on=columnas_config['producto_id'], suffixes=('_detalle', '_producto'))

        precio_col_base = columnas_config['producto_precio']
        precio_col = precio_col_base + '_producto' if precio_col_base + '_producto' in df_merged.columns else precio_col_base
        df_merged['valor_total'] = df_merged[columnas_config['detalle_cantidad']] * df_merged[precio_col]

        nombre_col_base = columnas_config['producto_nombre']
        nombre_col = nombre_col_base + '_producto' if nombre_col_base + '_producto' in df_merged.columns else nombre_col_base
        ventas_por_producto = df_merged.groupby(nombre_col)['valor_total'].sum().nlargest(15).reset_index()

        fig = go.Figure(data=[go.Bar(x=ventas_por_producto[nombre_col], y=ventas_por_producto['valor_total'], text=ventas_por_producto['valor_total'].apply(lambda x: f'{x:,.2f} €'), textposition='auto')])
        fig.update_layout(title_text='Top 15 Productos con Mayores Ventas', xaxis_title='Producto', yaxis_title='Ventas Totales (€)')
        
        print("Mostrando gráfico interactivo en el navegador...")
        fig.show()
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error al generar el gráfico: {e}" + Style.RESET_ALL)

def generar_grafico_ventas_por_dia(archivos_config, columnas_config, print_titulo_func):
    print_titulo_func("Gráfico: Ventas por Día de la Semana (L-V)")
    try:
        df_ventas = pd.read_excel(archivos_config['ventas'])
        df_detalle = pd.read_excel(archivos_config['detalle'])
        df_productos = pd.read_excel(archivos_config['productos'])

        df_merged = pd.merge(df_ventas, df_detalle, on=columnas_config['venta_id'])
        df_merged = pd.merge(df_merged, df_productos, left_on=columnas_config['detalle_producto_id'], right_on=columnas_config['producto_id'], suffixes=('_detalle', '_producto'))

        precio_col_base = columnas_config['producto_precio']
        precio_col = precio_col_base + '_producto' if precio_col_base + '_producto' in df_merged.columns else precio_col_base
        df_merged['valor_total'] = df_merged[columnas_config['detalle_cantidad']] * df_merged[precio_col]

        df_merged['fecha'] = pd.to_datetime(df_merged['fecha'])
        df_merged['dia_semana'] = df_merged['fecha'].dt.dayofweek
        df_laborables = df_merged[df_merged['dia_semana'] < 5] # Lunes (0) a Viernes (4)

        ventas_por_dia = df_laborables.groupby('dia_semana')['valor_total'].sum()
        dias = {0: 'Lunes', 1: 'Martes', 2: 'Miércoles', 3: 'Jueves', 4: 'Viernes'}
        ventas_por_dia.index = ventas_por_dia.index.map(dias.get)
        ventas_por_dia = ventas_por_dia.reindex(['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes'])

        fig = go.Figure(data=[go.Bar(x=ventas_por_dia.index, y=ventas_por_dia.values, text=ventas_por_dia.values, texttemplate='%{text:,.2f} €')])
        fig.update_layout(title_text='Ventas Totales por Día de la Semana (Lunes a Viernes)', xaxis_title='Día de la Semana', yaxis_title='Ventas Totales (€)')
        
        print("Mostrando gráfico interactivo en el navegador...")
        fig.show()
    except Exception as e:
        print(Fore.RED + f"Ocurrió un error al generar el gráfico: {e}" + Style.RESET_ALL)

# --- Menú Principal de Gráficos ---

def iniciar_menu_graficos(archivos_config, columnas_config, print_titulo_func):
    while True:
        print_titulo_func("Submenú de Gráficos")
        print("a) Ventas por Categoría")
        print("b) Top 15 Productos más vendidos")
        print("c) Ventas por Día de la Semana (L-V)")
        print("d) Volver al menú principal")

        opcion = input("\nSelecciona una opción de gráfico: ").lower()

        if opcion == 'a':
            generar_grafico_ventas_por_categoria(archivos_config, columnas_config, print_titulo_func)
        elif opcion == 'b':
            generar_grafico_ventas_por_producto(archivos_config, columnas_config, print_titulo_func)
        elif opcion == 'c':
            generar_grafico_ventas_por_dia(archivos_config, columnas_config, print_titulo_func)
        elif opcion == 'd':
            print("Volviendo al menú principal...")
            break
        else:
            print(Fore.RED + "Opción no válida. Por favor, intenta de nuevo." + Style.RESET_ALL)