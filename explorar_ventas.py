import pandas as pd
import matplotlib.pyplot as plt

try:
    # Cargar el archivo Excel
    df_ventas = pd.read_excel('Aurelion/ventas.xlsx')

    # Imprimir las primeras filas para tener una idea de los datos
    print("Primeras 5 filas de ventas.xlsx:")
    print(df_ventas.head())

    # Imprimir los nombres de las columnas para verificar
    print("\nColumnas en ventas.xlsx:")
    print(df_ventas.columns.tolist())

    # Agrupar por la columna 'medio_pago' y contar las ocurrencias
    # Asumimos que la columna se llama 'medio_pago'. Si no es así, el siguiente print de columnas ayudará a depurar.
    if 'medio_pago' in df_ventas.columns:
        pagos_agrupados = df_ventas['medio_pago'].value_counts()

        print("\nConteo de ventas por medio de pago:")
        print(pagos_agrupados)

        # Generar el gráfico de torta
        plt.figure(figsize=(8, 8))
        plt.pie(pagos_agrupados, labels=pagos_agrupados.index, autopct='%1.1f%%', startangle=140)
        plt.title('Distribución de Medios de Pago')
        plt.ylabel('') # Ocultar el label del eje y

        # Guardar el gráfico
        ruta_grafico = 'grafico_medios_pago.png'
        plt.savefig(ruta_grafico)
        print(f"\nGráfico guardado en: {ruta_grafico}")

    else:
        print("\nNo se encontró la columna 'medio_pago'. Por favor, revisa los nombres de las columnas impresos arriba y ajusta el script.")

except FileNotFoundError:
    print("El archivo Aurelion/ventas.xlsx no fue encontrado.")
except Exception as e:
    print(f"Un error ocurrió: {e}")