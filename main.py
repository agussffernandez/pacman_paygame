import pygame
import json


# Inicialización de pygame
pygame.init()


# Dimensiones de la pantalla
ANCHO = 400
ALTURA = 400
PANTALLA = pygame.display.set_mode((ANCHO, ALTURA))

# Título de la ventana
pygame.display.set_caption("Pac-Man Básico")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fps
FPS = 15
clock = pygame.time.Clock()  # Creamos un objeto clock que nos ayudará a controlar la velocidad de actualización del juego.

# Cargar el mapa desde el archivo JSON
with open("mapa.json", "r") as file:
    data = json.load(file)

# Extraer los datos del mapa, comida y fantasmas
MAPA = data["mapa"]
points = data["comida"]  # Lista de puntos (posiciones en el mapa donde Pac-Man comerá)
fantasmas = data["fantasmas"]


# Cargar la imagen del Pac-Man
pacman_image = pygame.image.load("pacman.png")
pacman_image_izq =pygame.transform.flip(pacman_image, True, False)  # Voltea la imagen para que mire hacia la izquierda

# Redimensionar la imagen a un tamaño de 50x50 píxeles
pacman_image = pygame.transform.scale(pacman_image, (35, 35))
pacman_image_izq = pygame.transform.scale(pacman_image_izq, (35, 35))
# Envolvemos la imagen en un rectángulo para manejar mejor la posición
pacman_rect = pacman_image.get_rect()


# FUNCIONES:

def encontrar_posicion_inicial(mapa) -> tuple:
    """ 
    Encuentra la primera celda libre (valor 0) empezando desde la parte inferior 
    del mapa y recorriendo de izquierda a derecha en cada fila.
    """
    # Recorrer el mapa desde la fila más baja hacia la más alta
    for y in range(len(mapa) - 1, -1, -1):  # Recorre de abajo hacia arriba
        for x in range(len(mapa[0])):  # Recorre de izquierda a derecha
            if mapa[y][x] == 0:  # Si encontramos un pasillo libre (0)
                return x * 40, y * 40  # Convertimos las coordenadas a píxeles

# Variables del pacman
pacman_x, pacman_y = encontrar_posicion_inicial(MAPA)  # Posición inicial de Pac-Man

pacman_speed = 5

# Contador de puntos recogidos
points_collected = 0


def dibujar_mapa() -> None:
    """ 
    Dibuja el mapa con los puntos de comida y las paredes
    """
    PANTALLA.fill(BLACK)
    # Recorre la cantidad de filas/listas que hay en mapa
    for y in range(len(MAPA)):
        # Recorre cada columna o posición de la primer fila, ya que siempre la primer fila será la siguiente a recorrer por el for anterior
        for x in range(len(MAPA[0])):
            if MAPA[y][x] == 1:
                # Se hace la multiplicación por 40 para ajustarlo a los píxeles,
                pygame.draw.rect(PANTALLA, WHITE, (x * 40, y * 40, 40, 40))

    # Dibujar los puntos de comida
    for point in points:
        # Cada point tiene las claves x y y que representan las coordenadas del punto de comida.
        # point["x"] * 40 + 20: Multiplicamos las coordenadas x por 40 para convertirlas en píxeles y luego sumamos 20 para centrar el círculo dentro de la celda.
        # point["y"] * 40 + 20: Lo mismo para la coordenada y, multiplicamos por 40 y sumamos 20 para centrar el círculo en la celda.
        # 5: El radio del círculo, es decir, el tamaño del punto de comida. En este caso, el radio es de 5 píxeles.
        pygame.draw.circle(PANTALLA, WHITE, (point["x"] * 40 + 20, point["y"] * 40 + 20), 5)


def mover_pacman(x: int, y: int, speed: int, keys) -> tuple:
    """ 
    Mueve al pacman según la posición (x,y) en la que se encuentre, y según la tecla que presione
    """
    pacman_direction = "right"
    
    if keys[pygame.K_LEFT]:
        x -= speed
        pacman_direction = "left"
    if keys[pygame.K_RIGHT]:
        x += speed
        pacman_direction = "right"
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    # Limitar al Pac-Man para que no se salga de la pantalla
    if x < 0:  # Si Pac-Man se mueve más allá del borde izquierdo
        x = 0
    if x > ANCHO - pacman_image.get_width():  # Resta el ancho de la imagen de Pac-Man al ancho total de la ventana
        x = ANCHO - pacman_image.get_width()
    if y < 0:  # Si Pac-Man se mueve más allá del borde superior
        y = 0
    if y > ALTURA - pacman_image.get_height():  # Si Pac-Man se mueve más allá del borde inferior
        y = ALTURA - pacman_image.get_height()

    return x, y, pacman_direction


def detectar_comida(x: int, y: int, points_collected: int) -> tuple:
    """ 
    Detecta si el Pac-Man ha recogido alguno de los puntos en la lista points. Si
    Pac-Man ha tocado un punto, ese punto se elimina de la lista y el contador de puntos recogidos se incrementa.
    """
    puntos_sin_comer = []  # Lista que almacenará los puntos no recogidos
    for point in points:
        # Desempaquetar las coordenadas del punto
        # Se convierten las coordenadas de las celdas del mapa (en la cuadrícula de 40x40) en coordenadas de píxeles.
        px, py = point["x"] * 40, point["y"] * 40
        # pygame.Rect(px, py, 40, 40) crea un nuevo rectángulo de 40x40 píxeles centrado en las coordenadas del punto de comida (px, py).
        # Si el rectángulo de pacman_rect se superpone con el rectángulo creado de comida, entonces Pac-Man ha recogido ese punto.
        comida_rect = pygame.Rect(px, py, 40, 40)
        if pacman_rect.colliderect(comida_rect):
            points_collected += 1  # Incrementa el contador de puntos
        else:
            # Si Pac-Man no ha tocado este punto, lo agregamos a la nueva lista
            puntos_sin_comer.append(point)

    # Devolver los valores actualizados (nueva lista de puntos y el contador de puntos)
    return puntos_sin_comer, points_collected


# Ciclo principal
corriendo = True

while corriendo:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False

    # Obtener las teclas presionadas
    keys = pygame.key.get_pressed()

    # Mover al Pac-Man
    pacman_x, pacman_y, pacman_direction = mover_pacman(pacman_x, pacman_y, pacman_speed, keys)

    # Actualizar la posición del pacman
    pacman_rect.topleft = (pacman_x, pacman_y)
    
    if pacman_direction == "right":
        pacman = pacman_image
    elif pacman_direction == "left":
        pacman = pacman_image_izq
    
    
    # Detectar si come algún punto
    points, points_collected = detectar_comida(pacman_x, pacman_y, points_collected)

    # Dibujar el mapa y los puntos
    dibujar_mapa()

    # Dibujar Pac-Man usando la imagen cargada
    PANTALLA.blit(pacman, pacman_rect)


    # Mostrar el marcador con un fondo rectangulo blanco
    fuente = pygame.font.SysFont(None, 30)
    texto = fuente.render(f"Puntos: {points_collected}", True, BLACK)
    # Obtener el rectangulo del texto
    texto_rect = texto.get_rect()
    # Ubicar la posición del recuadro en la esquina superior izquierda
    texto_rect.topleft = (10, 10)
    # Elegir un margen alrededor del texto para el recuadro
    margen = 10
    # Dibuja el recuadro blanco detrás del texto, usando el rectángulo de texto
    # La función inflate() de Pygame cambia el tamaño del rectángulo (Rect) incrementando su ancho y alto.  Al poner 2 * margen, estamos expandiendo el rectángulo en ambas direcciones (horizontal y vertical). Si no, solo se expanderia de 1 solo lado
    pygame.draw.rect(PANTALLA, WHITE, texto_rect.inflate(2*margen, 2*margen))
    # Dibujar el texto encima del recuadro
    PANTALLA.blit(texto, texto_rect)


    # Actualizar la pantalla
    pygame.display.update()

    # Control de FPS
    clock.tick(FPS)

pygame.quit()
