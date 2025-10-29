# Pseudocódigo del Script de Limpieza

Este documento describe la lógica del script `limpieza.py` en forma de pseudocódigo.

## 1. Configuración

`INICIO`

  `DEFINIR` una lista de cadenas de texto llamada `ARCHIVOS_A_LIMPIAR`.
  `ASIGNAR` a `ARCHIVOS_A_LIMPIAR` los nombres de los archivos Excel a procesar:
    - "Aurelion/clientes.xlsx"
    - "Aurelion/ventas.xlsx"
    - "Aurelion/detalle_ventas.xlsx"
    - "Aurelion/productos.xlsx"

`FIN`

## 2. Función Principal: `detectar_duplicados`

`INICIO DE FUNCIÓN detectar_duplicados`

  `MOSTRAR` "--- Iniciando Detección de Duplicados ---"

  `PARA CADA` `archivo` `EN` la lista `ARCHIVOS_A_LIMPIAR`:

    `SI` el `archivo` no existe en el sistema:
      `MOSTRAR` un mensaje de advertencia indicando que el archivo no se encontró.
      `CONTINUAR` con el siguiente archivo en la lista.
    `FIN SI`

    `INTENTAR:`
      `MOSTRAR` "Analizando el archivo: [nombre del archivo]..."

      `CARGAR` el contenido del `archivo` Excel en una tabla de datos llamada `tabla`.

      `OBTENER` el número total de filas en `tabla` y guardarlo en `total_filas`.
      `MOSTRAR` "Total de filas encontradas: [valor de total_filas]".

      `CONTAR` el número de filas que son duplicados exactos de otras filas en `tabla`.
      `GUARDAR` este conteo en `num_duplicados`.

      `SI` `num_duplicados` es mayor que 0:
        `MOSTRAR` "¡Se encontraron [valor de num_duplicados] filas duplicadas!".

        `// Lógica Opcional (inactiva en el script original)`
        `// MOSTRAR las filas que tienen duplicados.`

      `SINO:`
        `MOSTRAR` "No se encontraron filas duplicadas.".
      `FIN SI`

      `// Lógica Opcional para Guardar (inactiva en el script original)`
      `// SI num_duplicados > 0:`
      `//   CREAR una nueva tabla 'tabla_limpia' eliminando los duplicados de 'tabla'.`
      `//   GENERAR un nuevo nombre de archivo, por ejemplo "nombre_original_limpio.xlsx".`
      `//   GUARDAR 'tabla_limpia' en el nuevo archivo.`
      `//   MOSTRAR un mensaje de confirmación.`
      `// FIN SI`

    `CAPTURAR CUALQUIER ERROR:`
      `MOSTRAR` un mensaje de error indicando qué falló al procesar el archivo.
    `FIN INTENTAR/CAPTURAR`

  `FIN PARA CADA`

  `MOSTRAR` "--- Detección de Duplicados Finalizada ---"

`FIN DE FUNCIÓN`

## 3. Punto de Entrada del Script

`SI` este script es el programa principal que se está ejecutando:
  `LLAMAR A LA FUNCIÓN` `detectar_duplicados`.
`FIN SI`
