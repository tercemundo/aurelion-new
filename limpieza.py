import pandas as pd
import os

# --- Configuración ---
# Lista de los archivos Excel que se van a analizar.
# Agrega o quita archivos de esta lista según sea necesario.
ARCHIVOS_A_LIMPIAR = [
    'Aurelion/clientes.xlsx',
    'Aurelion/ventas.xlsx',
    'Aurelion/detalle_ventas.xlsx',
    'Aurelion/productos.xlsx'
]
# --------------------

def detectar_duplicados():
    """
    Abre una lista de archivos Excel, informa sobre la cantidad de filas duplicadas
    en cada uno y opcionalmente puede guardarlos sin duplicados.
    """
    print("--- Iniciando Detección de Duplicados ---")

    for archivo in ARCHIVOS_A_LIMPIAR:
        if not os.path.exists(archivo):
            print(f"\nADVERTENCIA: El archivo '{archivo}' no se encontró y será omitido.")
            continue

        try:
            print(f"\nAnalizando el archivo: '{archivo}'...")

            # Cargar el archivo Excel
            df = pd.read_excel(archivo)

            # Contar el total de filas
            total_filas = len(df)
            print(f"  - Total de filas encontradas: {total_filas}")

            # Detectar y contar duplicados
            # Esto cuenta todas las filas que son una copia exacta de otra que apareció antes.
            num_duplicados = df.duplicated().sum()

            if num_duplicados > 0:
                print(f"  - ¡Se encontraron {num_duplicados} filas duplicadas!")

                # Opcional: Mostrar las filas duplicadas
                # Descomenta la siguiente línea si quieres ver cuáles son las filas duplicadas.
                # print(df[df.duplicated(keep=False)].sort_values(by=list(df.columns)))

            else:
                print("  - No se encontraron filas duplicadas.")

            # --- Opcional: Guardar archivo sin duplicados ---
            # Si quieres crear una copia del archivo sin las filas duplicadas,
            # descomenta las siguientes líneas.
            #
            # if num_duplicados > 0:
            #     df_sin_duplicados = df.drop_duplicates()
            #     # Se crea un nuevo nombre para el archivo de salida
            #     nombre_base, extension = os.path.splitext(archivo)
            #     archivo_salida = f"{nombre_base}_limpio{extension}"
            #     df_sin_duplicados.to_excel(archivo_salida, index=False)
            #     print(f"  - Se ha guardado una versión limpia en: '{archivo_salida}'")
            # ----------------------------------------------------

        except Exception as e:
            print(f"  - Ocurrió un error al procesar el archivo '{archivo}': {e}")

    print("\n--- Detección de Duplicados Finalizada ---")


if __name__ == "__main__":
    detectar_duplicados()
