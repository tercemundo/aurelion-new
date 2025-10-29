[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/tercemundo/aurelion-new/blob/main/aurelion-ppt.ipynb)

## Cómo funciona el proyecto

Este proyecto consiste en un conjunto de scripts de Python diseñados para analizar los datos de ventas de la tienda "Aurelion", que se encuentran en archivos de formato Excel.

El análisis se divide en varios módulos, cada uno con un propósito específico:

-   **`limpieza.py`**: Este script se encarga de la limpieza de datos. Lee los archivos Excel del directorio `Aurelion/` y detecta filas duplicadas, informando de la cantidad encontrada en cada archivo. Opcionalmente, puede generar versiones limpias de los archivos.

-   **`ventas.py`**: Realiza un análisis para encontrar el producto más vendido en términos de unidades. Cruza la información de los archivos `detalle_ventas.xlsx` y `productos.xlsx` para determinar el producto estrella.

-   **`analisis_churn.py`**: Este módulo analiza la retención de clientes. Identifica a los clientes que se consideran "perdidos" o inactivos por no haber realizado compras en un período de tiempo configurable (por defecto, 180 días).

-   **`reporte.py`**: Es el script principal que unifica los análisis y presenta un menú interactivo al usuario. Desde este menú se pueden generar los siguientes reportes:
    -   **Resumen General**: Muestra métricas clave como el total de clientes, ventas, ingresos y el ticket promedio.
    -   **Ventas por Cliente**: Presenta un listado de los clientes que más han comprado.
    -   **Productos Más Vendidos**: Muestra un top 10 de los productos con mayor cantidad de ventas.
    -   **Análisis de Medios de Pago**: Desglosa las ventas según el método de pago utilizado.

Para utilizar el proyecto, el usuario puede ejecutar los scripts individualmente para obtener análisis específicos o correr `reporte.py` para acceder a todos los reportes de forma centralizada.
