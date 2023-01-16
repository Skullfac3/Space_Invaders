import pygame
import random
import math
from pygame import mixer

# inicializando  pygame
pygame.init()

# crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption("Invación de Aliens")
icono = pygame.image.load("ufo.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("espacio.jpg")

# Variables del jugador
img_jugador = pygame.image.load("astronave.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# Agregar musica 
mixer.music.load("MusicaFondo.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)

# variables del enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = [] 
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append (pygame.image.load("ovni.png"))
    enemigo_x.append(random.randint(0, 736)) # posicion x del enemigo
    enemigo_y.append(random.randint(50, 200)) 
    enemigo_x_cambio.append (0.5)
    enemigo_y_cambio.append (50)

# variables de la bala
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 0.5
bala_visible = False

# puntaje
puntaje = 0
fuente = pygame.font.Font('Invaders.ttf', 32)
texto_x = 10
texto_y = 10

# texto final de juego
fuente_final = pygame.font.Font('Invaders.ttf', 40)

def texto_final():
    mi_fuente_final = fuente_final.render("GAME OVER", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (200, 250))


# funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# funcion enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))


# funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_1 - y_2, 2))
    if distancia < 27:
        return True
    else:
        return False

# Loop del juego
se_ejecuta = True
while se_ejecuta:

    # imagen de fondo
    pantalla.blit(fondo, (0, 0))

    # Iterar eventos del juego
    for evento in pygame.event.get():

        # Evento de cerrar ventana
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        
    # Evento presionar teclas 
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.1
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound("disparo.mp3")
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)
        
    # Evento soltar flechas
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                    jugador_x_cambio = 0

    # Modificar ubicacion del jugador
    jugador_x += jugador_x_cambio

    # Limitar ubicacion del jugador en pantalla
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):

        # fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

    # Limitar ubicacion del enemigo en pantalla
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.1
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.1
            enemigo_y[e] += enemigo_y_cambio[e]

            # colision
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            sonido_explosion = mixer.Sound("Golpe.mp3")
            sonido_explosion.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            print(puntaje)
            enemigo_x[e] = random.randint(0, 736) # posicion x del enemigo
            enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio


    jugador(jugador_x, jugador_y)
    
    mostrar_puntaje(texto_x, texto_y)

    # Actualizar
    pygame.display.update()


