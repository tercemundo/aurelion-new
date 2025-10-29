import pandas as pd
import os

# --- Configuración ---
ARCHIVO_DETALLE_VENTAS = 'Aurelion/detalle_ventas.xlsx'
ARCHIVO_PRODUCTOS = 'Aurelion/productos.xlsx'

# Nombres de las columnas que se esperan en los archivos.
# AJUSTA ESTOS VALORES SI EL SCRIPT DA UN ERROR DE COLUMNAS.
COL_PRODUCTO_ID_DETALLE = 'id_producto'
COL_CANTIDAD = 'cantidad'
COL_PRODUCTO_ID_PROD = 'id_producto'
COL_NOMBRE_PRODUCTO = 'nombre_producto'
# --------------------

def analizar_producto_mas_vendido():
    """
    Analiza los archivos de ventas para encontrar el producto más vendido
    basado en la cantidad total vendida.
    """
    print("--- Iniciando Análisis del Producto Más Vendido ---")

    # --- Verificación de archivos ---
    archivos_necesarios = [ARCHIVO_DETALLE_VENTAS, ARCHIVO_PRODUCTOS]
    for archivo in archivos_necesarios:
        if not os.path.exists(archivo):
            print(f"\nERROR: El archivo necesario '{archivo}' no se encontró.")
            print("Por favor, asegúrate de que el archivo existe en la ruta correcta.")
            return

    try:
        # --- Carga y Verificación de Columnas ---
        df_detalle = pd.read_excel(ARCHIVO_DETALLE_VENTAS)
        df_productos = pd.read_excel(ARCHIVO_PRODUCTOS)

        # Verificar columnas en detalle_ventas.xlsx
        if COL_PRODUCTO_ID_DETALLE not in df_detalle.columns or COL_CANTIDAD not in df_detalle.columns:
            print(f"\n--- ¡ERROR DE CONFIGURACIÓN DE COLUMNAS! ---")
            print(f"No se encontraron las columnas esperadas en '{ARCHIVO_DETALLE_VENTAS}'.")
            print(f"Se esperaba encontrar '{COL_PRODUCTO_ID_DETALLE}' y '{COL_CANTIDAD}'.")
            print("\nLas columnas que sí se encontraron son:")
            print(df_detalle.columns.tolist())
            print("\nPor favor, ajusta las variables al inicio del script y vuelve a ejecutarlo.")
            return

        # Verificar columnas en productos.xlsx
        if COL_PRODUCTO_ID_PROD not in df_productos.columns or COL_NOMBRE_PRODUCTO not in df_productos.columns:
            print(f"\n--- ¡ERROR DE CONFIGURACIÓN DE COLUMNAS! ---")
            print(f"No se encontraron las columnas esperadas en '{ARCHIVO_PRODUCTOS}'.")
            print(f"Se esperaba encontrar '{COL_PRODUCTO_ID_PROD}' y '{COL_NOMBRE_PRODUCTO}'.")
            print("\nLas columnas que sí se encontraron son:")
            print(df_productos.columns.tolist())
            print("\nPor favor, ajusta las variables al inicio del script y vuelve a ejecutarlo.")
            return

        print("Archivos y columnas verificados correctamente.")

        # --- Análisis ---
        # 1. Sumar las cantidades para cada producto en el detalle de ventas
        ventas_por_producto = df_detalle.groupby(COL_PRODUCTO_ID_DETALLE)[COL_CANTIDAD].sum()

        # 2. Encontrar el ID del producto con la suma más alta (el más vendido)
        producto_mas_vendido_id = ventas_por_producto.idxmax()
        total_unidades_vendidas = ventas_por_producto.max()

        # 3. Buscar el nombre del producto usando su ID
        # Se usa .loc para buscar por el índice (que es el id_producto en df_productos)
        # Primero, aseguramos que el id del producto sea el índice en la tabla de productos
        df_productos_idx = df_productos.set_index(COL_PRODUCTO_ID_PROD)
        nombre_producto = df_productos_idx.loc[producto_mas_vendido_id, COL_NOMBRE_PRODUCTO]

        # --- Resultados ---
        print("\n--- Resultado del Análisis ---")
        print(f"El producto más vendido es: '{nombre_producto}'")
        print(f"Total de unidades vendidas: {int(total_unidades_vendidas)}")
        print("------------------------------")


    except KeyError as e:
        print(f"\nERROR: No se pudo encontrar la columna {e} después de la verificación.")
        print("Esto puede ocurrir si el ID del producto más vendido no existe en el archivo de productos.")
    except Exception as e:
        print(f"\nOcurrió un error inesperado durante el análisis: {e}")


if __name__ == "__main__":
    analizar_producto_mas_vendido()
