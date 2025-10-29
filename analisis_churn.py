import pandas as pd
from datetime import datetime

# --- Parámetros de Análisis ---
# Define el número de días sin comprar para considerar a un cliente como "perdido"
DIAS_INACTIVIDAD_UMBRAL = 180

# Nombres de los archivos y columnas. AJUSTA ESTOS VALORES SI ES NECESARIO.
ARCHIVO_VENTAS = 'Aurelion/ventas.xlsx'
ARCHIVO_CLIENTES = 'Aurelion/clientes.xlsx'

COLUMNA_CLIENTE_ID_VENTAS = 'id_cliente'
COLUMNA_FECHA_VENTA = 'fecha'
COLUMNA_CLIENTE_ID_CLIENTES = 'id_cliente'
# --------------------------

def analizar_churn():
    """
    Analiza los datos de ventas para identificar clientes que podrían considerarse perdidos
    basado en su inactividad.
    """
    try:
        # Cargar los datos sin parsear fechas inicialmente para poder verificar las columnas
        df_ventas = pd.read_excel(ARCHIVO_VENTAS)
        df_clientes = pd.read_excel(ARCHIVO_CLIENTES)

        # --- Verificación de Columnas ---
        if COLUMNA_FECHA_VENTA not in df_ventas.columns or COLUMNA_CLIENTE_ID_VENTAS not in df_ventas.columns:
            print(f"\n--- ¡ERROR DE CONFIGURACIÓN DE COLUMNAS! ---")
            print(f"No se encontraron las columnas esperadas en '{ARCHIVO_VENTAS}'.")
            print(f"Se esperaba encontrar '{COLUMNA_CLIENTE_ID_VENTAS}' y '{COLUMNA_FECHA_VENTA}'.")
            print("\nLas columnas que sí se encontraron son:")
            print(df_ventas.columns.tolist())
            print("\nPor favor, ajusta las variables 'COLUMNA_CLIENTE_ID_VENTAS' y 'COLUMNA_FECHA_VENTA' al inicio del script con los nombres correctos y vuelve a ejecutarlo.")
            print("------------------------------------------------\n")
            return # Detener la ejecución

        print("Archivos Excel y columnas requeridas encontrados.")

        # Ahora sí, procesar las fechas
        df_ventas[COLUMNA_FECHA_VENTA] = pd.to_datetime(df_ventas[COLUMNA_FECHA_VENTA], errors='coerce')
        df_ventas.dropna(subset=[COLUMNA_FECHA_VENTA], inplace=True)


        # Encontrar la fecha de la última compra para cada cliente
        ultima_compra = df_ventas.groupby(COLUMNA_CLIENTE_ID_VENTAS)[COLUMNA_FECHA_VENTA].max().reset_index()
        ultima_compra.columns = [COLUMNA_CLIENTE_ID_CLIENTES, 'FechaUltimaCompra']

        # Determinar la fecha más reciente en todo el conjunto de datos para el cálculo
        fecha_mas_reciente = df_ventas[COLUMNA_FECHA_VENTA].max()
        print(f"La última fecha de venta registrada es: {fecha_mas_reciente.date()}")

        # Calcular los días desde la última compra para cada cliente
        ultima_compra['DiasDesdeUltimaCompra'] = (fecha_mas_reciente - ultima_compra['FechaUltimaCompra']).dt.days

        # Unir la información de la última compra con el listado total de clientes
        df_clientes_completo = pd.merge(df_clientes, ultima_compra, on=COLUMNA_CLIENTE_ID_CLIENTES, how='left')

        # Identificar clientes perdidos
        df_clientes_perdidos = df_clientes_completo[df_clientes_completo['DiasDesdeUltimaCompra'] > DIAS_INACTIVIDAD_UMBRAL]

        # Clientes que nunca han comprado
        clientes_sin_compras = df_clientes_completo[df_clientes_completo['DiasDesdeUltimaCompra'].isna()]

        # Resultados
        total_clientes = len(df_clientes)
        cantidad_clientes_perdidos = len(df_clientes_perdidos)
        cantidad_clientes_sin_compras = len(clientes_sin_compras)
        porcentaje_perdidos = (cantidad_clientes_perdidos / total_clientes) * 100 if total_clientes > 0 else 0

        print("\n--- Análisis de Churn de Clientes ---")
        print(f"Umbral de inactividad definido: {DIAS_INACTIVIDAD_UMBRAL} días")
        print("-" * 35)
        print(f"Total de clientes en la base de datos: {total_clientes}")
        print(f"Número de clientes considerados perdidos (inactivos): {cantidad_clientes_perdidos}")
        if porcentaje_perdidos > 0:
            print(f"Porcentaje de clientes perdidos: {porcentaje_perdidos:.2f}%")
        print(f"Número de clientes que nunca han realizado una compra: {cantidad_clientes_sin_compras}")
        print("-" * 35)

        if cantidad_clientes_perdidos > 0:
            print("\nIDs de los clientes perdidos:")
            for cliente_id in df_clientes_perdidos[COLUMNA_CLIENTE_ID_CLIENTES]:
                print(cliente_id)


    except FileNotFoundError as e:
        print(f"Error: No se pudo encontrar el archivo -> {e.filename}")
        print("Por favor, asegúrate de que los nombres de archivo y las rutas son correctas.")
    except KeyError as e:
        print(f"Error: No se pudo encontrar la columna -> {e}")
        print("Por favor, verifica que los nombres de las columnas en el script coincidan con los de tus archivos Excel.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    analizar_churn()
