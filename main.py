import pygame
import random


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
clock = pygame.time.Clock() # Creamos un objeto clock que nos ayudará a controlar la velocidad de actualización del juego.

# Cargar la imagen del Pac-Man
pacman_image = pygame.image.load("pacman.png")
# Redimensionar la imagen a un tamaño de 50x50 pixeles
pacman_image = pygame.transform.scale(pacman_image, (50,50))
#Envolvemos la imagen en un rectangulo para manejar mejor la posición
pacman_rect = pacman_image.get_rect() 

# Variables del pacman
pacman_x, pacman_y = 50, 50 # Posicion inicial del packman
pacman_speed = 5



# FUNCIONES:


# Lista de puntos (posiciones en el mapa donde Pac-Man comerá)
points = [(100, 100), (200, 200), (300, 300)]
# Contador de puntos recogidos
points_collected = 0  



def dibujar_mapa() -> None:
    """ 
    Dibuja el mapa con los puntos en los cuales el pacman debera comer
    """
    PANTALLA.fill(BLACK)
    # Dibuja los puntos
    for point in points:
        #  Dibuja un círculo de color blanco en las posiciones definidas en la lista points.
        pygame.draw.circle(PANTALLA, WHITE, point, 5)


def mover_pacman(x: int, y: int, speed: int, keys) -> tuple:
    """ 
    Mueve al pacman segun la posición (x,y) en la que se encuentre, y según la tecla que presione
    """
    if keys[pygame.K_LEFT]:
        x -= speed
        """ 
        Si se presiona la flecha hacia la izquierda, restamos la velocidad (speed) al valor de x. Esto mueve a Pac-Man hacia la izquierda en la pantalla (porque las coordenadas x disminuyen cuando nos movemos hacia la izquierda).
        """
    if keys[pygame.K_RIGHT]:
        x+= speed
    if keys[pygame.K_UP]:
        y -= speed
        """ 
        Si se presiona la flecha hacia arriba, restamos la velocidad (speed) al valor de y. Esto mueve a Pac-Man hacia arriba en la pantalla (porque las coordenadas y disminuyen cuando nos movemos hacia arriba, ya que en Pygame el eje Y crece hacia abajo).
        """
    if keys[pygame.K_DOWN]:
        y += speed
    
    # Limitar al Pac-Man para que no se salga de la pantalla
    if x < 0:# Si Pac-Man se mueve más allá del borde derecho
        x = 0
    if x > ANCHO - pacman_image.get_width():
        # Resta el ancho de la imagen de Pac-Man al ancho total de la ventana. 
        x = ANCHO - pacman_image.get_width()
    if y < 0: # Si Pac-Man se mueve más allá del borde superior
        y = 0
    if y > ALTURA - pacman_image.get_height(): # Si Pac-Man se mueve más allá del borde inferior
        y = ALTURA - pacman_image.get_height()
    
    return x, y


def detectar_comida(x: int, y:int, points_collected: int) -> tuple:
    """ 
    Detecta si el Pac-Man ha recogido alguno de los puntos en la lista points. Si
    Pac-Man ha tocado un punto, ese punto se elimina de la lista y el contador de puntos recogidos se incrementa.

.
    """
    puntos_sin_comer = []  # Lista que almacenará los puntos no recogidos
    for point in points:
        # Desempaquetar las coordenadas del punto
        px, py = point
        # crea un rectángulo de 10x10 píxeles centrado en el punto (px, py).
        # px-5 y py-5 se usan para ajustar la posición del rectángulo, de modo que esté centrado en las coordenadas del punto.
        # colliderect(pacman_rect) verifica si el rectángulo creado para el punto se superpone con el rectángulo de Pac-Man, pacman_rect.
        if pygame.Rect(px-5, py-5, 10, 10).colliderect(pacman_rect):
            points_collected += 1 # Incrementa el contador de puntos
        else:
            # Si Pac-Man no ha tocado este punto, lo agregamos a la nueva lista
            puntos_sin_comer.append(point)
    
    
    # Devolver los valores actualizados (nueva lista de puntos y el contador de puntos)
    return puntos_sin_comer, points_collected












corriendo = True

while corriendo: 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            corriendo = False
    
    # Obtener las teclas presionadas
    keys = pygame.key.get_pressed()
    
    # Mover al Pac-Man
    pacman_x, pacman_y = mover_pacman(pacman_x, pacman_y, pacman_speed, keys)
    
    # Actualizar la posicion del pacman
    pacman_rect.topleft = (pacman_x, pacman_y)
    
    # Detectar si come algun punto
    points, points_collected = detectar_comida(pacman_x, pacman_y, points_collected)
    
    # Dibujar el mapa y los puntos
    dibujar_mapa()
    
    # Dibujar Pac-Man usando la imagen cargada
    PANTALLA.blit(pacman_image, pacman_rect)
    
    # Mostrar el marcador
    fuente = pygame.font.SysFont(None, 30)
    texto = fuente.render(f"Puntos: {points_collected}", True, WHITE)
    PANTALLA.blit(texto, (10,10))
    
    
    
    # Actualizar la pantalla
    pygame.display.update()
    
    # Conrol de FPS
    clock.tick(FPS)

pygame.quit()