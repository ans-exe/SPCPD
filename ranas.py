import threading
import time

# Estado inicial y posición objetivo del espacio vacío
start = ["a", "b", "c", "_", "d", "f", "g"]
target_empty_index = len(start) // 2  # Índice medio para el espacio vacío

# Crear un bloqueo global
lock = threading.Lock()

# Variable global compartida para el estado
current_state = start[:]

# Función para verificar si alcanzamos el objetivo


def is_goal(state):
    empty_index = state.index("_")
    # Verificamos que el espacio esté en el centro y todas las ranas a los lados correctos
    left_side = state[:empty_index]
    right_side = state[empty_index + 1:]
    # El lado izquierdo debe tener solo ranas del lado derecho original y viceversa
    return (empty_index == target_empty_index and
            all(rana in start[len(start) // 2 + 1:] for rana in left_side) and
            all(rana in start[:len(start) // 2] for rana in right_side))

# Función que cada hilo (rana) ejecutará


def rana_thread(rana, index):
    global current_state
    while not is_goal(current_state):
        with lock:
            empty_index = current_state.index("_")
            # Verificar si la rana puede moverse al espacio vacío
            if abs(empty_index - index) == 1 or abs(empty_index - index) == 2:
                # Mover la rana al espacio vacío
                current_state[empty_index], current_state[index] = current_state[index], current_state[empty_index]

                # Imprimir el paso actual
                print(
                    f"Rana '{rana}' se movió de posición {index} a {empty_index}")
                print("Estado actual:", current_state)

                # Actualizar índice de la rana después del movimiento
                index = empty_index

        time.sleep(0.1)  # Pausa para evitar sobrecarga de CPU


# Crear y lanzar un hilo para cada rana
threads = []
for i, rana in enumerate(start):
    if rana != "_":  # Ignoramos el espacio vacío
        thread = threading.Thread(target=rana_thread, args=(rana, i))
        threads.append(thread)
        thread.start()

# Esperar a que todos los hilos terminen
for thread in threads:
    thread.join()

# Imprimir el resultado final
print("¡Estado final alcanzado!", current_state)
