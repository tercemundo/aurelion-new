# Análisis de Churn de Clientes

Este documento describe el propósito, funcionamiento y configuración del script de Python `analisis_churn.py`.

## 1. Propósito del Script

El script `analisis_churn.py` está diseñado para analizar la base de datos de clientes y ventas con el fin de identificar "clientes en riesgo" o "clientes perdidos" (análisis de churn).

El criterio principal para identificar a un cliente en riesgo es su **inactividad**. Se considera que un cliente está inactivo si no ha realizado ninguna compra en un período de tiempo configurable.

## 2. Requisitos

Para ejecutar este script, necesitas tener Python instalado en tu sistema, junto con las siguientes librerías:

-   `pandas`: Para la manipulación y análisis de los datos.
-   `openpyxl`: Para que `pandas` pueda leer los archivos de formato Excel (`.xlsx`).

Puedes instalar estas dependencias ejecutando el siguiente comando en tu terminal:

```bash
pip install pandas openpyxl
```

## 3. Cómo Ejecutar el Script

1.  Abre una terminal o línea de comandos.
2.  Navega hasta el directorio raíz de este proyecto (`MarceloG-ProyectoAurelion`).
3.  Ejecuta el siguiente comando:

```bash
python analisis_churn.py
```

## 4. Configuración

Al principio del script, encontrarás una sección de "Parámetros de Análisis" que puedes modificar según tus necesidades.

```python
# --- Parámetros de Análisis ---
# Define el número de días sin comprar para considerar a un cliente como "perdido"
DIAS_INACTIVIDAD_UMBRAL = 180

# Nombres de los archivos y columnas.
ARCHIVO_VENTAS = 'Aurelion/ventas.xlsx'
ARCHIVO_CLIENTES = 'Aurelion/clientes.xlsx'

COLUMNA_CLIENTE_ID_VENTAS = 'id_cliente'
COLUMNA_FECHA_VENTA = 'fecha'
COLUMNA_CLIENTE_ID_CLIENTES = 'id_cliente'
# --------------------------
```

-   `DIAS_INACTIVIDAD_UMBRAL`: Es el parámetro más importante. Define cuántos días de inactividad son necesarios para que un cliente sea considerado "perdido". Por defecto, está en 180 días (aproximadamente 6 meses).
-   `ARCHIVO_VENTAS` y `ARCHIVO_CLIENTES`: Rutas a los archivos de datos.
-   `COLUMNA_...`: Nombres de las columnas que el script utiliza para identificar el ID del cliente y la fecha de la venta. Es crucial que estos nombres coincidan exactamente con los de tus archivos Excel.

## 5. Lógica del Análisis

El script sigue los siguientes pasos:

1.  **Carga de Datos**: Lee los archivos `ventas.xlsx` y `clientes.xlsx` en memoria.
2.  **Verificación de Columnas**: Comprueba que los nombres de las columnas configuradas (`id_cliente`, `fecha`) existen en los datos cargados. Si no, muestra un error y la lista de columnas disponibles para facilitar la corrección.
3.  **Cálculo de la Última Compra**: Para cada cliente, busca en los datos de ventas y encuentra la fecha de su compra más reciente.
4.  **Cálculo de Días de Inactividad**: Calcula la diferencia en días entre la fecha de la última venta registrada en *todo* el dataset y la fecha de la última compra de *cada* cliente.
5.  **Identificación de Clientes Perdidos**: Compara los días de inactividad de cada cliente con el `DIAS_INACTIVIDAD_UMBRAL`. Si el número de días es mayor, el cliente se marca como "perdido".
6.  **Generación de Resultados**: Muestra un resumen en la terminal.

## 6. Resultados (Salida del Script)

Al ejecutar el script, verás una salida en la terminal con el siguiente formato:

-   **Mensajes de estado**: Informa si los archivos se cargaron correctamente y cuál es la última fecha de venta registrada.
-   **Resumen del Análisis**:
    -   Total de clientes en la base de datos.
    -   Número de clientes considerados perdidos (inactivos).
    -   Porcentaje de clientes perdidos sobre el total.
    -   Número de clientes que nunca han realizado una compra.
-   **Lista de IDs**: Si se encuentran clientes perdidos, se imprime una lista con los `id_cliente` de cada uno de ellos.
