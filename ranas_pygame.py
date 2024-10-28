import pygame
import threading
import time

# Inicializa Pygame
pygame.init()

# Constantes para la pantalla y colores
ANCHO, ALTO = 800, 200
TAMANIO_RANA = 80  # Tamaño de cada imagen de rana
FPS = 30

# Colores opcionales (para debug)
BLANCO = (255, 255, 255)

# Cargar imágenes
fondo = pygame.image.load("fondo.jpg")
rana_izquierda = pygame.image.load("rana_izquierda.png")
rana_derecha = pygame.image.load("rana_derecha.png")
espacio = pygame.image.load("espacio.png")

# Escalar las imágenes para adaptarse al tamaño deseado
rana_izquierda = pygame.transform.scale(rana_izquierda, (TAMANIO_RANA, TAMANIO_RANA))
rana_derecha = pygame.transform.scale(rana_derecha, (TAMANIO_RANA, TAMANIO_RANA))
espacio = pygame.transform.scale(espacio, (TAMANIO_RANA, TAMANIO_RANA))

# Configuración de la ventana
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de Ranas")

class Estanque:
    def __init__(self, n):
        self.n = n
        self.estanque = ['L'] * n + ['_'] + ['R'] * n
        self.lock = threading.Lock()

    def mostrar(self):
        """Dibuja el estanque en la pantalla usando Pygame."""
        ventana.blit(fondo, (0, 0))  # Dibuja el fondo
        for i, posicion in enumerate(self.estanque):
            x = i * TAMANIO_RANA  # Posición horizontal para cada rana o espacio

            if posicion == 'L':
                ventana.blit(rana_izquierda, (x, 50))
            elif posicion == 'R':
                ventana.blit(rana_derecha, (x, 50))
            else:
                ventana.blit(espacio, (x, 50))

        pygame.display.update()  # Actualiza la pantalla

    def mover(self, origen, destino):
        """Intercambia las posiciones entre el origen y el destino."""
        self.estanque[origen], self.estanque[destino] = self.estanque[destino], self.estanque[origen]

    def encontrar_movimientos(self, grupo):
        """Encuentra todos los movimientos válidos para un grupo."""
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

    def esta_completado(self):
        """Verifica si el juego ha sido completado."""
        return self.estanque == ['R'] * self.n + ['_'] + ['L'] * self.n


class JuegoDeRanas:
    def __init__(self, n):
        self.estanque = Estanque(n)

    def generar_secuencia_saltos(self, n):
        secuencia = []
        for i in range(1, n + 1):
            secuencia.append((i, 'L' if i % 2 != 0 else 'R'))
        if n % 2 != 0:
            secuencia.extend([(n, 'L'), (n, 'R')])
        secuencia.extend([(n, 'L'), (n, 'R'), (n, 'L')])
        for i in range(n - 1, 0, -1):
            secuencia.append((i, 'R' if i % 2 != 0 else 'L'))
        return secuencia

    def movimiento_grupo(self, grupo, saltos):
        for _ in range(saltos):
            with self.estanque.lock:
                movimientos = self.estanque.encontrar_movimientos(grupo)
                if movimientos:
                    origen, destino = movimientos.pop(0)
                    self.estanque.mover(origen, destino)
                    self.estanque.mostrar()
                    time.sleep(0.5)

    def ejecutar(self):
        n = self.estanque.n
        secuencia_saltos = self.generar_secuencia_saltos(n)
        self.estanque.mostrar()

        for saltos, grupo in secuencia_saltos:
            if self.estanque.esta_completado():
                print("¡Felicidades! Has completado el juego.")
                return
            hilo = threading.Thread(target=self.movimiento_grupo, args=(grupo, saltos))
            hilo.start()
            hilo.join()


def main():
    n = int(input("Ingrese la cantidad de ranas por lado: "))
    juego = JuegoDeRanas(n)
    reloj = pygame.time.Clock()

    # Bucle principal del juego
    ejecutando = True
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False

        juego.ejecutar()
        reloj.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
