import pandas as pd
import os
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

# --- Configuración ---
# Asegúrate de que estos nombres de archivo y columnas coincidan con los tuyos.
ARCHIVOS = {
    'clientes': 'Aurelion/clientes.xlsx',
    'ventas': 'Aurelion/ventas.xlsx',
    'detalle': 'Aurelion/detalle_ventas.xlsx',
    'productos': 'Aurelion/productos.xlsx'
}

COLUMNAS = {
    # Clientes
    'cliente_id': 'id_cliente',
    'cliente_nombre': 'nombre_cliente',
    'cliente_email': 'email',
    # Ventas
    'venta_id': 'id_venta',
    'venta_medio_pago': 'medio_pago',
    # Detalle Ventas
    'detalle_venta_id': 'id_venta',
    'detalle_producto_id': 'id_producto',
    'detalle_cantidad': 'cantidad',
    # Productos
    'producto_id': 'id_producto',
    'producto_nombre': 'nombre_producto',
    'producto_precio': 'precio_unitario'
}
# --------------------


def imprimir_banner():
    """Imprime un banner de bienvenida con ASCII art."""
    banner = r"""
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                   ║
    ║   ████████╗██╗███████╗███╗   ██╗██████╗  █████╗                  ║
    ║   ╚══██╔══╝██║██╔════╝████╗  ██║██╔══██╗██╔══██╗                 ║
    ║      ██║   ██║█████╗  ██╔██╗ ██║██║  ██║███████║                 ║
    ║      ██║   ██║██╔══╝  ██║╚██╗██║██║  ██║██╔══██║                 ║
    ║      ██║   ██║███████╗██║ ╚████║██████╔╝██║  ██║                 ║
    ║      ╚═╝   ╚═╝╚══════╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝                 ║
    ║                                                                   ║
    ║        █████╗ ██╗   ██╗██████╗ ███████╗██╗     ██╗ ██████╗ ███╗ ║
    ║       ██╔══██╗██║   ██║██╔══██╗██╔════╝██║     ██║██╔═══██╗████╗║
    ║       ███████║██║   ██║██████╔╝█████╗  ██║     ██║██║   ██║██╔██║
    ║       ██╔══██║██║   ██║██╔══██╗██╔══╝  ██║     ██║██║   ██║██║╚█║
    ║       ██║  ██║╚██████╔╝██║  ██║███████╗███████╗██║╚██████╔╝██║ ╚║
    ║       ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝ ╚═════╝ ╚═╝  ║
    ║                                                                   ║
    ║              Sistema de Gestión de Ventas v1.0                   ║
    ║                                                                   ║
    ╚═══════════════════════════════════════════════════════════════════╝
    """
    print(f"{Fore.YELLOW}{banner}{Style.RESET_ALL}")


def print_titulo(texto):
    """Imprime un título resaltado."""
    print(f"\n{Style.BRIGHT}{Fore.CYAN}{'='*60}")
    print(f"{Style.BRIGHT}{Fore.CYAN}  {texto.upper()}")
    print(f"{Style.BRIGHT}{Fore.CYAN}{'='*60}{Style.RESET_ALL}")


def cargar_y_verificar_datos():
    """Carga todos los archivos Excel y verifica la existencia de archivos y columnas."""
    dfs = {}
    print_titulo("Cargando y Verificando Datos de Tienda Aurelion")

    for nombre, ruta in ARCHIVOS.items():
        if not os.path.exists(ruta):
            print(f"{Fore.RED}✗ Error: El archivo '{ruta}' no existe.{Style.RESET_ALL}")
            return None

        try:
            df = pd.read_excel(ruta)
            dfs[nombre] = df
            print(f"{Fore.GREEN}✓ Archivo '{nombre}' cargado correctamente ({len(df)} registros){Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}✗ Error al cargar '{ruta}': {e}{Style.RESET_ALL}")
            return None

    # Verificar columnas necesarias
    print(f"\n{Fore.CYAN}Verificando columnas...{Style.RESET_ALL}")

    verificaciones = [
        ('clientes', [COLUMNAS['cliente_id'], COLUMNAS['cliente_nombre'], COLUMNAS['cliente_email']]),
        ('ventas', [COLUMNAS['venta_id'], COLUMNAS['venta_medio_pago']]),
        ('detalle', [COLUMNAS['detalle_venta_id'], COLUMNAS['detalle_producto_id'], COLUMNAS['detalle_cantidad']]),
        ('productos', [COLUMNAS['producto_id'], COLUMNAS['producto_nombre'], COLUMNAS['producto_precio']])
    ]

    for tabla, columnas in verificaciones:
        columnas_faltantes = [col for col in columnas if col not in dfs[tabla].columns]
        if columnas_faltantes:
            print(f"{Fore.RED}✗ Columnas faltantes en '{tabla}': {columnas_faltantes}{Style.RESET_ALL}")
            return None
        print(f"{Fore.GREEN}✓ Columnas verificadas en '{tabla}'{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}{Style.BRIGHT}¡Todos los datos cargados correctamente!{Style.RESET_ALL}")
    return dfs


def calcular_ventas_totales(dfs):
    """Calcula el total de ventas por cliente."""
    print_titulo("Ventas Totales por Cliente")

    # Merge de las tablas
    detalle_productos = pd.merge(
        dfs['detalle'],
        dfs['productos'],
        left_on=COLUMNAS['detalle_producto_id'],
        right_on=COLUMNAS['producto_id']
    )

    # Calcular total por venta
    detalle_productos['total'] = (
        detalle_productos[COLUMNAS['detalle_cantidad']] * 
        detalle_productos[COLUMNAS['producto_precio']]
    )

    # Agrupar por venta
    ventas_totales = detalle_productos.groupby(COLUMNAS['detalle_venta_id'])['total'].sum().reset_index()
    ventas_totales.columns = [COLUMNAS['venta_id'], 'monto_total']

    # Merge con ventas y clientes
    resultado = pd.merge(dfs['ventas'], ventas_totales, on=COLUMNAS['venta_id'])
    resultado = pd.merge(resultado, dfs['clientes'], on=COLUMNAS['cliente_id'])

    # Agrupar por cliente
    ventas_por_cliente = resultado.groupby(COLUMNAS['cliente_nombre'])['monto_total'].sum().reset_index()
    ventas_por_cliente = ventas_por_cliente.sort_values('monto_total', ascending=False)

    print(f"\n{Fore.YELLOW}Top 10 Clientes por Ventas:{Style.RESET_ALL}\n")
    print(ventas_por_cliente.head(10).to_string(index=False))

    return ventas_por_cliente


def analizar_productos_mas_vendidos(dfs):
    """Analiza los productos más vendidos."""
    print_titulo("Productos Más Vendidos")

    detalle_productos = pd.merge(
        dfs['detalle'],
        dfs['productos'],
        left_on=COLUMNAS['detalle_producto_id'],
        right_on=COLUMNAS['producto_id']
    )

    productos_vendidos = detalle_productos.groupby(COLUMNAS['producto_nombre'])[COLUMNAS['detalle_cantidad']].sum().reset_index()
    productos_vendidos.columns = ['Producto', 'Cantidad_Vendida']
    productos_vendidos = productos_vendidos.sort_values('Cantidad_Vendida', ascending=False)

    print(f"\n{Fore.YELLOW}Top 10 Productos Más Vendidos:{Style.RESET_ALL}\n")
    print(productos_vendidos.head(10).to_string(index=False))

    return productos_vendidos


def analizar_medios_pago(dfs):
    """Analiza la distribución de medios de pago."""
    print_titulo("Análisis de Medios de Pago")

    medios_pago = dfs['ventas'][COLUMNAS['venta_medio_pago']].value_counts().reset_index()
    medios_pago.columns = ['Medio_Pago', 'Cantidad']
    medios_pago['Porcentaje'] = (medios_pago['Cantidad'] / medios_pago['Cantidad'].sum() * 100).round(2)

    print(f"\n{Fore.YELLOW}Distribución de Medios de Pago:{Style.RESET_ALL}\n")
    print(medios_pago.to_string(index=False))

    return medios_pago


def generar_resumen_general(dfs):
    """Genera un resumen general de la tienda."""
    print_titulo("Resumen General - Tienda Aurelion")

    total_clientes = len(dfs['clientes'])
    total_ventas = len(dfs['ventas'])
    total_productos = len(dfs['productos'])

    # Calcular ingresos totales
    detalle_productos = pd.merge(
        dfs['detalle'],
        dfs['productos'],
        left_on=COLUMNAS['detalle_producto_id'],
        right_on=COLUMNAS['producto_id']
    )
    detalle_productos['total'] = (
        detalle_productos[COLUMNAS['detalle_cantidad']] * 
        detalle_productos[COLUMNAS['producto_precio']]
    )
    ingresos_totales = detalle_productos['total'].sum()
    ticket_promedio = ingresos_totales / total_ventas if total_ventas > 0 else 0

    print(f"\n{Fore.GREEN}{'─'*50}")
    print(f"{Fore.GREEN}  Total de Clientes:      {Fore.WHITE}{total_clientes:,}")
    print(f"{Fore.GREEN}  Total de Ventas:        {Fore.WHITE}{total_ventas:,}")
    print(f"{Fore.GREEN}  Total de Productos:     {Fore.WHITE}{total_productos:,}")
    print(f"{Fore.GREEN}  Ingresos Totales:       {Fore.WHITE}${ingresos_totales:,.2f}")
    print(f"{Fore.GREEN}  Ticket Promedio:        {Fore.WHITE}${ticket_promedio:,.2f}")
    print(f"{Fore.GREEN}{'─'*50}{Style.RESET_ALL}\n")


def menu_principal():
    """Muestra el menú principal y maneja las opciones."""
    imprimir_banner()

    dfs = cargar_y_verificar_datos()
    if dfs is None:
        print(f"\n{Fore.RED}No se pudieron cargar los datos. Verifica los archivos y vuelve a intentar.{Style.RESET_ALL}")
        return

    while True:
        print(f"\n{Style.BRIGHT}{Fore.MAGENTA}╔═══════════════════════════════════════╗")
        print(f"{Style.BRIGHT}{Fore.MAGENTA}║        MENÚ PRINCIPAL                 ║")
        print(f"{Style.BRIGHT}{Fore.MAGENTA}╚═══════════════════════════════════════╝{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1.{Style.RESET_ALL} Resumen General")
        print(f"{Fore.CYAN}2.{Style.RESET_ALL} Ventas Totales por Cliente")
        print(f"{Fore.CYAN}3.{Style.RESET_ALL} Productos Más Vendidos")
        print(f"{Fore.CYAN}4.{Style.RESET_ALL} Análisis de Medios de Pago")
        print(f"{Fore.CYAN}5.{Style.RESET_ALL} Ver Todos los Análisis")
        print(f"{Fore.RED}0.{Style.RESET_ALL} Salir")

        opcion = input(f"\n{Fore.YELLOW}Selecciona una opción: {Style.RESET_ALL}").strip()

        if opcion == '1':
            generar_resumen_general(dfs)
        elif opcion == '2':
            calcular_ventas_totales(dfs)
        elif opcion == '3':
            analizar_productos_mas_vendidos(dfs)
        elif opcion == '4':
            analizar_medios_pago(dfs)
        elif opcion == '5':
            generar_resumen_general(dfs)
            calcular_ventas_totales(dfs)
            analizar_productos_mas_vendidos(dfs)
            analizar_medios_pago(dfs)
        elif opcion == '0':
            print(f"\n{Fore.GREEN}¡Gracias por usar el Sistema de Tienda Aurelion!{Style.RESET_ALL}")
            print(f"{Fore.GREEN}¡Hasta pronto! 👋{Style.RESET_ALL}\n")
            break
        else:
            print(f"\n{Fore.RED}Opción no válida. Por favor, intenta de nuevo.{Style.RESET_ALL}")

        input(f"\n{Fore.YELLOW}Presiona Enter para continuar...{Style.RESET_ALL}")


if __name__ == "__main__":
    menu_principal()
