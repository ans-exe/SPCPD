import time
import threading
from colorama import Fore, Style, init

# Inicializar colorama para entornos de Windows
init()

class Estanque:
    def __init__(self, n):
        """Inicializa el estanque con n ranas en cada lado y un espacio vacío en el centro."""
        self.estanque = ['L'] * n + ['_'] + ['R'] * n
        self.lock = threading.Lock()

    def mostrar(self):
        """Muestra el estado actual del estanque."""
        print(Style.RESET_ALL + "Ranas ->     ", end="  ")
        for posicion in self.estanque:
            color = Fore.RED if posicion == 'L' else Fore.GREEN if posicion == 'R' else Fore.WHITE
            print(color + posicion, end=" ")
        print(Style.RESET_ALL)
        print(Style.RESET_ALL + "Posiciones -> " + " ".join(map(str, range(len(self.estanque)))))

    def mover_rana(self, origen, destino):
        """Intercambia la posición de una rana con el espacio vacío."""
        self.estanque[origen], self.estanque[destino] = self.estanque[destino], self.estanque[origen]

    def encontrar_movimientos(self, grupo):
        """Encuentra los movimientos válidos para el grupo 'L' o 'R'."""
        movimientos = []
        posicion_vacia = self.estanque.index('_')

        for i in range(len(self.estanque)):
            if grupo == 'L' and self.estanque[i] == 'L':
                if i + 1 < len(self.estanque) and self.estanque[i + 1] == '_':
                    movimientos.append((i, i + 1))
                elif i + 2 < len(self.estanque) and self.estanque[i + 2] == '_':
                    movimientos.append((i, i + 2))
            elif grupo == 'R' and self.estanque[i] == 'R':
                if i - 1 >= 0 and self.estanque[i - 1] == '_':
                    movimientos.append((i, i - 1))
                elif i - 2 >= 0 and self.estanque[i - 2] == '_':
                    movimientos.append((i, i - 2))

        movimientos.sort(key=lambda mov: abs(mov[0] - posicion_vacia))
        return movimientos

    def es_completado(self, n):
        """Verifica si el juego ha sido completado."""
        return self.estanque == ['R'] * n + ['_'] + ['L'] * n


class RanaGrupo(threading.Thread):
    def __init__(self, estanque, grupo, saltos):
        """Inicializa un hilo para mover un grupo de ranas."""
        super().__init__()
        self.estanque = estanque
        self.grupo = grupo
        self.saltos = saltos

    def run(self):
        """Ejecuta los movimientos para el grupo de ranas."""
        for _ in range(self.saltos):
            with self.estanque.lock:
                movimientos = self.estanque.encontrar_movimientos(self.grupo)
                if movimientos:
                    origen, destino = movimientos.pop(0)
                    self.estanque.mover_rana(origen, destino)
                    self.estanque.mostrar()
                    time.sleep(0.5)


class JuegoRanas:
    def __init__(self):
        """Inicializa el juego pidiendo la cantidad de ranas por lado."""
        self.n = int(input("Ingrese la cantidad de ranas por lado: "))
        self.estanque = Estanque(self.n)

    def generar_secuencia_saltos(self):
       
        secuencia = [(i, 'L' if i % 2 != 0 else 'R') for i in range(1, self.n + 1)]

        if self.n % 2 != 0:
            secuencia += [(self.n, 'L'), (self.n, 'R')]

        secuencia += [(self.n, 'L'), (self.n, 'R'), (self.n, 'L')]
        secuencia += [(i, 'R' if i % 2 != 0 else 'L') for i in range(self.n - 1, 0, -1)]

        return secuencia

    def ejecutar(self):
    
        self.estanque.mostrar()
        secuencia_saltos = self.generar_secuencia_saltos()

        for saltos, grupo in secuencia_saltos:
            if self.estanque.es_completado(self.n):
                print(Fore.MAGENTA + "¡Felicidades! Has completado el juego." + Style.RESET_ALL)
                return

            hilo = RanaGrupo(self.estanque, grupo, saltos)
            hilo.start()
            hilo.join()


if __name__ == "__main__":
    juego = JuegoRanas()
    juego.ejecutar()
