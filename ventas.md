# Pseudocódigo del Script de Análisis de Ventas

Este documento describe la lógica del script `ventas.py` en forma de pseudocódigo.

## 1. Configuración

`INICIO`

  `DEFINIR` `ARCHIVO_DETALLE_VENTAS` como "Aurelion/detalle_ventas.xlsx".
  `DEFINIR` `ARCHIVO_PRODUCTOS` como "Aurelion/productos.xlsx".

  `// Definir los nombres de columna esperados`
  `DEFINIR` `COL_PRODUCTO_ID_DETALLE` como "id_producto".
  `DEFINIR` `COL_CANTIDAD` como "cantidad".
  `DEFINIR` `COL_PRODUCTO_ID_PROD` como "id_producto".
  `DEFINIR` `COL_NOMBRE_PRODUCTO` como "nombre_producto".

`FIN`

## 2. Función Principal: `analizar_producto_mas_vendido`

`INICIO DE FUNCIÓN analizar_producto_mas_vendido`

  `MOSTRAR` "--- Iniciando Análisis del Producto Más Vendido ---"

  `// Verificación de existencia de archivos`
  `SI` `ARCHIVO_DETALLE_VENTAS` no existe `O` `ARCHIVO_PRODUCTOS` no existe:
    `MOSTRAR` un mensaje de error indicando qué archivo falta.
    `TERMINAR` la ejecución.
  `FIN SI`

  `INTENTAR:`
    `// Carga de datos`
    `CARGAR` el archivo `ARCHIVO_DETALLE_VENTAS` en una tabla `tabla_detalles`.
    `CARGAR` el archivo `ARCHIVO_PRODUCTOS` en una tabla `tabla_productos`.

    `// Verificación de columnas en tabla_detalles`
    `SI` las columnas `COL_PRODUCTO_ID_DETALLE` o `COL_CANTIDAD` no existen en `tabla_detalles`:
      `MOSTRAR` un mensaje de error con la lista de columnas encontradas.
      `TERMINAR` la ejecución.
    `FIN SI`

    `// Verificación de columnas en tabla_productos`
    `SI` las columnas `COL_PRODUCTO_ID_PROD` o `COL_NOMBRE_PRODUCTO` no existen en `tabla_productos`:
      `MOSTRAR` un mensaje de error con la lista de columnas encontradas.
      `TERMINAR` la ejecución.
    `FIN SI`

    `MOSTRAR` "Archivos y columnas verificados correctamente."

    `// Inicio del Análisis`
    `CREAR` una nueva tabla `ventas_agrupadas` agrupando `tabla_detalles` por `COL_PRODUCTO_ID_DETALLE`.
    `PARA CADA` grupo, `SUMAR` los valores de la columna `COL_CANTIDAD`.

    `ENCONTRAR` el `id_producto` que tiene la suma de cantidad más alta en `ventas_agrupadas`. Guardarlo en `producto_mas_vendido_id`.
    `OBTENER` esa suma máxima y guardarla en `total_unidades_vendidas`.

    `BUSCAR` en `tabla_productos` la fila donde `COL_PRODUCTO_ID_PROD` es igual a `producto_mas_vendido_id`.
    `OBTENER` el valor de la columna `COL_NOMBRE_PRODUCTO` de esa fila y guardarlo en `nombre_producto`.

    `// Mostrar Resultados`
    `MOSTRAR` "--- Resultado del Análisis ---"
    `MOSTRAR` "El producto más vendido es: [valor de nombre_producto]"
    `MOSTRAR` "Total de unidades vendidas: [valor de total_unidades_vendidas]"
    `MOSTRAR` "------------------------------"

  `CAPTURAR CUALQUIER ERROR:`
    `MOSTRAR` un mensaje de error detallando el problema que ocurrió durante el análisis.
  `FIN INTENTAR/CAPTURAR`

`FIN DE FUNCIÓN`

## 3. Punto de Entrada del Script

`SI` este script es el programa principal que se está ejecutando:
  `LLAMAR A LA FUNCIÓN` `analizar_producto_mas_vendido`.
`FIN SI`
