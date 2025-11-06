"""
Menu Interactivo con Navegación por Flechas
Usa las teclas UP/DOWN para navegar y ENTER para seleccionar
"""

import os
import sys
from colorama import Fore, Back, Style, init

# Inicializar colorama
init(autoreset=True)

# Detectar sistema operativo para usar las teclas correctas
if os.name == 'nt':  # Windows
    import msvcrt

    def get_key():
        """Captura tecla presionada en Windows"""
        key = msvcrt.getch()
        if key == b'\xe0':  # Tecla especial (flechas)
            key = msvcrt.getch()
            if key == b'H':  # Flecha arriba
                return 'up'
            elif key == b'P':  # Flecha abajo
                return 'down'
        elif key == b'\r':  # Enter
            return 'enter'
        elif key == b'\x1b':  # ESC
            return 'esc'
        return None

else:  # Linux/Mac
    import tty
    import termios

    def get_key():
        """Captura tecla presionada en Linux/Mac"""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)

            if ch == '\x1b':  # Secuencia de escape
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    if ch3 == 'A':  # Flecha arriba
                        return 'up'
                    elif ch3 == 'B':  # Flecha abajo
                        return 'down'
                else:
                    return 'esc'
            elif ch == '\r' or ch == '\n':  # Enter
                return 'enter'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None


def limpiar_pantalla():
    """Limpia la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu(opciones, seleccion):
    """
    Muestra el menú con la opción seleccionada resaltada

    Args:
        opciones: Lista de tuplas (numero, texto)
        seleccion: Índice de la opción seleccionada
    """
    limpiar_pantalla()

    # Encabezado
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print(Fore.CYAN + Style.BRIGHT + "                    MENU PRINCIPAL")
    print(Fore.CYAN + Style.BRIGHT + "=" * 60)
    print()

    # Opciones del menú
    for i, (numero, texto) in enumerate(opciones):
        if i == seleccion:
            # Opción seleccionada (resaltada)
            print(Back.WHITE + Fore.BLACK + Style.BRIGHT + 
                  f"  ► {numero}. {texto}  " + Style.RESET_ALL)
        else:
            # Opciones normales
            print(Fore.GREEN + f"    {numero}. {texto}")

    print()
    print(Fore.YELLOW + "━" * 60)
    print(Fore.YELLOW + "  Use ↑/↓ para navegar | ENTER para seleccionar | ESC para salir")
    print(Fore.YELLOW + "━" * 60)


def ejecutar_opcion(numero, texto):
    """
    Ejecuta la acción correspondiente a la opción seleccionada

    Args:
        numero: Número de la opción
        texto: Texto de la opción
    """
    limpiar_pantalla()
    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
    print(Fore.MAGENTA + Style.BRIGHT + f"  OPCIÓN SELECCIONADA")
    print(Fore.MAGENTA + Style.BRIGHT + "=" * 60)
    print()
    print(Fore.GREEN + Style.BRIGHT + f"  Hola menu {numero}")
    print(Fore.CYAN + f"  Opción: {texto}")
    print()
    print(Fore.YELLOW + "=" * 60)
    print()
    input(Fore.WHITE + "Presione ENTER para volver al menú...")


def main():
    """Función principal del menú"""
    # Definir opciones del menú
    opciones = [
        (1, "Compilar archivos (clientes, productos, etc.)"),
        (2, "Ver productos más vendidos"),
        (3, "Analizar ventas y métricas"),
        (4, "Generar reportes y gráficos y diagramas"),
        (5, "Ver datos estadísticos"),
        (6, "Visualizar resumen completo de cruce"),
        (7, "Salir")
    ]

    seleccion = 0  # Índice de la opción seleccionada

    while True:
        mostrar_menu(opciones, seleccion)

        # Capturar tecla
        key = get_key()

        if key == 'up':
            # Subir en el menú
            seleccion = (seleccion - 1) % len(opciones)

        elif key == 'down':
            # Bajar en el menú
            seleccion = (seleccion + 1) % len(opciones)

        elif key == 'enter':
            # Seleccionar opción
            numero, texto = opciones[seleccion]

            # Si es la opción de salir
            if numero == 7:
                limpiar_pantalla()
                print(Fore.RED + Style.BRIGHT + "\n  Saliendo del programa...")
                print(Fore.CYAN + "  ¡Hasta luego!\n")
                break

            # Ejecutar la opción seleccionada
            ejecutar_opcion(numero, texto)

        elif key == 'esc':
            # Salir con ESC
            limpiar_pantalla()
            print(Fore.RED + Style.BRIGHT + "\n  Saliendo del programa...")
            print(Fore.CYAN + "  ¡Hasta luego!\n")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        limpiar_pantalla()
        print(Fore.RED + Style.BRIGHT + "\n  Programa interrumpido por el usuario")
        print(Fore.CYAN + "  ¡Hasta luego!\n")
        sys.exit(0)
