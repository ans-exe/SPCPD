import time
import threading
from colorama import Fore, Style, init

# Inicializar colorama para entornos de Windows
init()

# Representación inicial del estanque con n ranas de cada lado
n = 3  # Cambia el valor de n para aumentar el número de ranas
estanque_inicial = ['L'] * n + ['_'] + ['R'] * n

# Lock para sincronizar movimientos
lock = threading.Lock()

# Función para mostrar el estanque
def mostrar_estanque(estanque):
    print(Style.RESET_ALL + "Ranas ->     ", end="  ")
    
    for posicion in estanque:
        if posicion == 'L':
            print(Fore.RED + posicion, end=" ")  # Ranas de la izquierda en rojo
        elif posicion == 'R':
            print(Fore.GREEN + posicion, end=" ")  # Ranas de la derecha en verde
        else:
            print(Fore.WHITE + posicion, end=" ")  # Espacio vacío en blanco
    
    print(Style.RESET_ALL)  # Restablecemos el color a la configuración predeterminada
    print(Style.RESET_ALL + "Posiciones -> " + " ".join(map(str, range(len(estanque)))))

# Encuentra todos los movimientos válidos posibles para un grupo
def encontrar_movimientos(estanque, grupo):
    movimientos = []
    posicion_vacia = estanque.index('_')  # Encuentra la posición del espacio vacío
    
    for i in range(len(estanque)):
        if grupo == 'L' and estanque[i] == 'L':  # Rana 'L' solo se mueve a la derecha
            if i + 1 < len(estanque) and estanque[i + 1] == '_':  # mover un espacio a la derecha
                movimientos.append((i, i + 1))
            elif i + 2 < len(estanque) and estanque[i + 2] == '_':  # saltar sobre una rana
                movimientos.append((i, i + 2))
        elif grupo == 'R' and estanque[i] == 'R':  # Rana 'R' solo se mueve a la izquierda
            if i - 1 >= 0 and estanque[i - 1] == '_':  # mover un espacio a la izquierda
                movimientos.append((i, i - 1))
            elif i - 2 >= 0 and estanque[i - 2] == '_':  # saltar sobre una rana
                movimientos.append((i, i - 2))
    
    # Ordenar los movimientos por distancia al espacio vacío
    movimientos.sort(key=lambda mov: abs(mov[0] - posicion_vacia))
    return movimientos

# Mueve la rana en el estanque
def mover_rana(estanque, origen, destino):
    estanque[origen], estanque[destino] = estanque[destino], estanque[origen]

# Lógica de movimiento para cada grupo basado en la secuencia de saltos
def movimiento_grupo(estanque, grupo, saltos):
    for _ in range(saltos):
        with lock:  # Bloqueo para evitar que ambos grupos se muevan a la vez
            movimientos = encontrar_movimientos(estanque, grupo)
            if movimientos:
                origen, destino = movimientos.pop(0)  # Mover la rana más cercana al espacio vacío
                mover_rana(estanque, origen, destino)
                mostrar_estanque(estanque)
                time.sleep(0.5)
            else:
                break  # Si no hay movimientos posibles, detener

# Función para ejecutar el juego con hilos
def ejecutar_juego_con_hilos():
    estanque = estanque_inicial[:]
    mostrar_estanque(estanque)
    
    # Definir secuencia de movimientos y turnos
    secuencia_saltos = [(1, 'L'), (2, 'R'), (3, 'L'), (3, 'R'), (3, 'L'), (2, 'R'), (1, 'L')]

    # Crear hilos para cada secuencia de movimiento
    for saltos, grupo in secuencia_saltos:
        if estanque == ['R'] * n + ['_'] + ['L'] * n:
            print(Fore.MAGENTA + "¡Felicidades! Has completado el juego." + Style.RESET_ALL)
            return
        
        # Crear y ejecutar un hilo para el grupo de ranas correspondiente
        hilo = threading.Thread(target=movimiento_grupo, args=(estanque, grupo, saltos))
        hilo.start()
        hilo.join()  # Esperar a que el hilo termine antes de continuar con el siguiente

    # Mensaje final si se completa el ciclo de movimientos sin resolver el juego
    if estanque != ['R'] * n + ['_'] + ['L'] * n:
        print(Fore.RED + "El juego no se completó en 15 movimientos." + Style.RESET_ALL)

# Inicia el juego
if __name__ == "__main__":
    ejecutar_juego_con_hilos()
