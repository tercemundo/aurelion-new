# Análisis Completo de Datos de Ventas

## Estadísticas Descriptivas Básicas

### Variables Principales de Ventas

El análisis de 120 transacciones revela patrones importantes en el comportamiento de compra :[1][2][3][4]

**Importe Total por Venta:**
- Media: $22,095.14
- Mediana: $19,999.00
- Desviación estándar: $13,363.12
- Rango: $272.00 - $61,503.00
- Coeficiente de variación: 60.48%

**Cantidad de Productos por Venta:**
- Media: 8.47 unidades
- Mediana: 8.00 unidades
- Desviación estándar: 4.50
- Rango: 1-19 unidades

**Tipos de Productos por Transacción:**
- Media: 2.86 productos diferentes
- Mediana: 3.00 productos
- La mayoría de las ventas incluyen entre 2-4 productos distintos

### Análisis por Segmentos

**Ventas por Ciudad:**
- Carlos Paz lidera con ticket promedio de $27,219.38 (13 ventas)
- Villa María: $28,486.36 promedio (11 ventas)
- Río Cuarto: Mayor volumen con 37 ventas, promedio $21,410.89

**Ventas por Medio de Pago:**
- Efectivo: Mayor ticket promedio $25,265.38 (37 transacciones)
- QR: $23,809.33 promedio (30 transacciones)
- Tarjeta: Menor ticket $17,696.12 (26 transacciones)
- Transferencia: $20,082.19 promedio (27 transacciones)

**Ventas por Categoría:**
- Limpieza: 178 ítems vendidos, promedio $8,068.99 por ítem
- Alimentos: 165 ítems vendidos, promedio $7,364.46 por ítem
- Facturación total Limpieza: $1,436,281
- Facturación total Alimentos: $1,215,136

## Identificación del Tipo de Distribución

### Importe Total
**Características:** Distribución no normal con sesgo moderado hacia la derecha (skewness: 0.5940). El test de Shapiro-Wilk rechaza la normalidad (p-valor: 0.0017). Esta distribución indica que la mayoría de las ventas se concentran en montos más bajos, con algunas transacciones de alto valor que elevan el promedio. El coeficiente de variación del 60.48% señala alta dispersión en los importes.[3][1]

**Interpretación:** Comportamiento típico de ventas minoristas donde la mayoría son compras regulares con algunos pedidos excepcionales de mayor valor.

### Cantidad Total de Productos
**Características:** Distribución aproximadamente simétrica (skewness: 0.3099) pero no normal según Shapiro-Wilk (p-valor: 0.0028). La mediana (8 unidades) está muy cerca de la media (8.47 unidades), indicando equilibrio en la distribución central.[3]

**Interpretación:** Los clientes tienden a comprar cantidades similares de productos, con variación moderada (CV: 53.17%).

### Ítems Comprados
**Características:** Distribución discreta con valores entre 1-5 productos diferentes por venta. Distribución simétrica (skewness: 0.1173) con concentración en 2-3 productos por transacción.[3]

**Interpretación:** Los clientes suelen hacer compras focalizadas en pocos productos, sugiriendo compras de reposición específicas más que compras grandes planificadas.

## Análisis de Correlaciones

### Correlaciones entre Variables Principales

**Importe Total vs Cantidad Total:** Existe una fuerte correlación positiva esperada, ya que comprar más unidades incrementa el valor total de la venta. Esta relación confirma el comportamiento lógico del modelo de negocio.[3]

**Importe Total vs Ítems Comprados:** Correlación positiva moderada, donde incluir más tipos de productos diferentes incrementa el valor de la transacción. Sin embargo, la correlación no es perfecta porque algunos productos tienen precios unitarios muy diferentes (rango: $272-$4,982).[4]

**Cantidad vs Ítems:** Correlación positiva débil a moderada, ya que aumentar la variedad de productos tiende a aumentar las unidades totales, pero los clientes pueden comprar muchas unidades de pocos productos o pocas unidades de varios productos.

### Correlaciones por Segmentos

**Ciudad y Valor de Venta:** Carlos Paz y Villa María presentan tickets promedio superiores (≈$27,000-$28,000) comparado con Alta Gracia ($19,260). Esto sugiere diferencias socioeconómicas o patrones de consumo por ubicación geográfica.[2][1]

**Medio de Pago y Valor:** El efectivo está asociado con transacciones de mayor valor ($25,265) mientras que las tarjetas con menor valor ($17,696). Esto podría indicar que compras grandes se prefieren en efectivo posiblemente por descuentos o preferencias del comercio.[1]

**Categoría y Frecuencia:** Limpieza tiene mayor volumen de ítems (178 vs 165) y mayor facturación total, indicando mayor demanda y/o precios más altos en esta categoría.[4][3]

## Detección de Outliers

### Método IQR (Rango Intercuartílico)

**Importe Total:**
- Q1: $11,618.50
- Q3: $33,260.50
- IQR: $21,642.00
- Límite inferior: Q1 - 1.5×IQR = -$20,844.50 (no aplica, valor mínimo $272)
- Límite superior: Q3 + 1.5×IQR = $65,723.50

**Outliers detectados:** Una venta de $61,503 se acerca al límite superior pero no lo excede. Esta transacción representa un pedido excepcionalmente grande (probablemente mayorista o compra especial) que se encuentra en el percentil 99.[3]

**Cantidad Total:**
- IQR: 7 unidades
- Outliers: Ventas con más de 16-17 unidades (límite superior: 12 + 1.5×7 = 22.5)
- Venta máxima: 19 unidades, considerada outlier moderado[3]

**Ítems Comprados:**
- IQR: 2 productos
- Límite superior: 4 + 1.5×2 = 7 productos
- Valor máximo: 5 productos (dentro del rango normal)
- No se detectan outliers significativos en esta variable

### Outliers por Precio Unitario

Productos con precios extremos :[4]
- **Precio mínimo:** Pan Lactal Integral ($272) - representa el producto más económico del catálogo
- **Precios máximos:** Suavizante 1L ($4,920), Miel Pura 250g ($4,982), Pepsi 1.5L ($4,973)
- Estos precios extremos no son errores sino productos premium o con márgenes especiales

### Impacto de Outliers

Los outliers en importe total explican por qué la media ($22,095) es superior a la mediana ($19,999), evidenciando el sesgo hacia la derecha en la distribución. Estas transacciones atípicas:[3]
- Representan menos del 5% de las ventas totales
- Contribuyen desproporcionadamente a la facturación total
- Pueden corresponder a clientes B2B o compras estacionales especiales

## Gráficos Representativos

### Gráfico 1: Distribución de Ventas por Categoría

Este gráfico de barras compararía la facturación total entre Alimentos ($1,215,136) y Limpieza ($1,436,281), mostrando que Limpieza genera 18% más ingresos pese a ser un catálogo mixto. Incluiría también el número de ítems vendidos (165 vs 178) para visualizar tanto volumen como valor.[4][3]

### Gráfico 2: Histograma de Distribución de Importe Total

Un histograma con curva de densidad mostraría la concentración de ventas en el rango $11,000-$34,000 (rango intercuartílico) con cola larga hacia la derecha, visualizando el sesgo positivo identificado (skewness: 0.594). Incluiría líneas verticales marcando la media ($22,095) y mediana ($19,999) para ilustrar la diferencia.[3]

### Gráfico 3: Boxplot Comparativo por Medio de Pago

Un gráfico de cajas múltiples compararía la distribución del importe total según el medio de pago, evidenciando que efectivo tiene mayor dispersión y valores más altos, mientras tarjeta concentra transacciones de menor valor. Este gráfico también revelaría los outliers en cada categoría.[1]

## Interpretación Orientada al Problema

### Hallazgos Clave para la Gestión Comercial

**Segmentación de Clientes:**
Los datos revelan dos perfiles principales de compra :[2][1][3]
1. **Comprador regular:** Ticket promedio $12,000-$20,000, 2-3 productos, 5-8 unidades
2. **Comprador intensivo:** Ticket >$33,000, 4-5 productos, >12 unidades

**Oportunidades de Optimización:**

*Estrategia por Ciudad:* Carlos Paz y Villa María muestran mayor capacidad de gasto. Considerar campañas premium y productos de mayor valor en estas ubicaciones.[2]

*Incentivos de Pago:* Las transacciones con tarjeta tienen menor valor promedio ($17,696 vs $25,265 en efectivo). Implementar promociones específicas para tarjeta podría incrementar el ticket promedio en este segmento.[1]

*Mix de Productos:* Limpieza genera más ingresos que Alimentos. Evaluar expandir el catálogo de limpieza o mejorar márgenes en Alimentos para equilibrar la rentabilidad.[4]

**Gestión de Inventario:**

La alta variabilidad (CV 60.48%) en los importes sugiere demanda irregular. Implementar:[3]
- Stock de seguridad mayor para los 20 productos más vendidos
- Análisis ABC para priorizar productos según rotación y rentabilidad
- Monitoreo de outliers para identificar patrones estacionales o clientes mayoristas

**Detección de Anomalías:**

Las ventas >$60,000 requieren validación especial por ser outliers significativos. Establecer alertas automáticas para transacciones que excedan 3 desviaciones estándar ($62,184) para prevenir fraudes o errores de facturación.[3]

**Recomendaciones Estratégicas:**

1. **Aumentar ítems por venta:** El promedio actual es 2.86 productos. Estrategias de cross-selling podrían incrementar esto a 4-5 productos, aumentando el ticket promedio 30-40%.

2. **Fidelización geográfica:** Río Cuarto tiene el mayor volumen (37 ventas) pero ticket medio-bajo. Programas de fidelización podrían convertir frecuencia en mayor valor por transacción.

3. **Optimización de precios:** El amplio rango de precios ($272-$4,982) indica oportunidades para ajustes estratégicos y promociones cruzadas entre productos de bajo y alto valor.

Este análisis proporciona una base cuantitativa sólida para decisiones comerciales basadas en datos, identificando tanto oportunidades de crecimiento como áreas de riesgo operativo.
