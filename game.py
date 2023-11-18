import pygame
import random
import math
import sys 
import os 

#Inicializar pygame code 
pygame.init()



#Establece el tamano de la pantalla
screen_width = 800
screen_height = 650
screen = pygame.display.set_mode((screen_width, screen_height))

#Funcion para obtener la ruta de los recursos 

def resource_path(relative_path):
    try: 
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
#Cargar imagen de fondo 
    
asset_background = resource_path('assets/images/background1.png')
background = pygame.image.load(asset_background)

#Cargar icono de ventana     
    
asset_icon = resource_path('assets/images/ufo.png')
icon = pygame.image.load(asset_icon)

#Cargar sonido de fondo     
    
asset_sound = resource_path('assets/audios/background_music.mp3')
background_sound = pygame.mixer.music.load(asset_sound)


#Cargar imagen del jugador     
    
asset_playering = resource_path('assets/images/space-invaders.png')
playering = pygame.image.load(asset_playering)

#Cargar imagen de bala     
    
asset_bulleting = resource_path('assets/images/bullet.png')
bulleting = pygame.image.load(asset_bulleting)

#Cargar fuente de texto game over     
    
asset_over_font = resource_path('assets/fonts/RAVIE.TTF')
over_font = pygame.font.Font(asset_over_font, 60)


#Cargar fuente de texto de puntuaje      
    
asset_font = resource_path('assets/fonts/comicbd.ttf')
font = pygame.font.Font(asset_font, 32)

# Establecer titulo de ventana

pygame.display.set_caption("Space black (Jesus Morillo)")

#Establecer icono de ventana

pygame.display.set_icon(icon)


#reproducior sonido de fondo en loop

pygame.mixer.music.play(-1)

#crear reloj para controlar la velociad del juego 

clock = pygame.time.Clock()

#Pocision inicial del jugar

playerX = 370
playerY = 470
playerx_change = 0 
playery_change = 0 

#Lista para almacenar pocisiones de los enemigos 

enemying = [] 
enemyX = [] 
enemyY = [] 
enemyX_change = []
enemyY_change = []
no_of_enemies = 10  

#Se inician las variables para guardar las pocisiones de los enemigos 

for i in  range(no_of_enemies):
    enemy1 = resource_path('assets/images/enemy1.png')
    enemying.append(pygame.image.load(enemy1))

    enemy2 = resource_path('assets/images/enemy2.png')
    enemying.append(pygame.image.load(enemy2))

    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(0,150))

    enemyX_change.append(5)
    enemyY_change.append(20)

    #SE INICIAN LAS VARIABLES PARA GUARDAR LA POSICION DE LAS BALAS 

    bulletX = 0
    bulletY = 480
    bulletX_change = 0 
    bulletY_change = 10 
    bullet_state = "ready"

    # se inicia la puntuacion en 0 

    score = 0 

    #funcion para mostrar la puntuacion en patalla


    
    def show_score():
        score_value = font.render("SCORE " + str(score), True, (255, 255, 255))
        screen.blit(score_value, (10, 10))

    #funcion dibujar jugador en pantalla
    def player(x , y ):
        screen.blit(playering, (x , y))   

    #funcion para dibujar al enemigo en la pantalla
    def enemy(x, y, i):
        screen.blit(enemying[i], (x , y))

    #fincion para disparar la bala
    def fire_bullet(x, y):
        global bullet_state

        bullet_state = "fire"
        screen.blit(bulleting, (x + 16, y + 10) )

    # funcion para combrobar si ocurrio una colision entre la bala y el enemigo 
    def isCollision(enemyX, enemyY, bulletX, bulletY):
        distance = math.sqrt((math.pow(enemyX-bulletX, 2)) +
                             (math.pow(enemyY-bulletY, 2)))
        if distance < 27:
            return True
        else:
            return False
    
    #funcion para mostrar texto game over  
    def game_over_text():
        over_text = over_font.render("GAME OVER", True, (255, 255, 255))
        text_rect = over_text.get_rect(
            center=(int(screen_width/2), int(screen_width/2)))
        screen.blit(over_text, text_rect)


    #Funcion principal del juego
    def gameloop():

        #declarar variables globales
        global score
        global playerX
        global playerx_change
        global bulletX
        global bulletY
        global Collision
        global bullet_state

        in_game = True
        while in_game:
            #Maneja eventos, actualiza y renderiza el juego 
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    in_game = False
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    #Movimientos del jguador y disparo
                    if event.key == pygame.K_LEFT:
                        playerx_change = -5
                    
                    if event.key == pygame.K_RIGHT:
                         playerx_change = 5 

                    if event.key == pygame.K_SPACE:
                        if bullet_state == "ready":
                            bulletX = playerX
                            fire_bullet(bulletX, bulletY)

                    if event.type == pygame.KEYUP:
                        playerx_change = 0 

            #Aqui se esta actualizndo la posicion del jugador 
            playerX += playerx_change

            if playerX <= 0:      
               playerX = 0
            elif playerX >= 736:
                playerX = 736

            #bucle que se ejecuta para cada enemigo 
            for i in range(no_of_enemies): 
                if enemyY[i] > 440:
                    for j in range(no_of_enemies):
                        enemyY[j] = 2000
                    game_over_text()

                enemyX[i] += enemyX_change[i]
                if enemyX[i] <= 0:
                    enemyX_change[i] = 5
                    enemyY[i] += enemyY_change[i] 
                elif enemyX[i] >= 736:
                    enemyX_change[i] = -5
                    enemyY[i] += enemyY_change[i]
            
                 #colision entre la bala y el enemigo 
            
                collison = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
                if collison:
                    bulletY = 454
                    bullet_state = "ready"
                    score += 1 
                    enemyX[i] = random.randint(0, 736)
                    enemyY[i] = random.randint(0, 150)
                enemy(enemyX[i], enemyY[i], i)

            if  bulletY < 0:
                 bulletY = 454
                 bullet_state = "ready"
            if bullet_state == "fire":
                fire_bullet(bulletX, bulletY)
                bulletY -= bulletY_change

            player(playerX, playerY)
            show_score()

            pygame.display.update()

            clock.tick(120)      
import pygame
import sys

pygame.init()

screen_width = 800
screen_height = 650

window = pygame.display.set_mode((screen_width, screen_height))

# Cargar imagen de fondo
background_image = pygame.image.load('assets/images/background2.png').convert()

def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Salir del menú y comenzar el juego
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        window.fill((0, 0, 0))  # Limpia la pantalla

        # Dibujar imagen de fondo primero
        window.blit(background_image, (0, 0))

        # Cargar la fuente RAVIE.TTF
        menu_font = pygame.font.Font('assets/fonts/RAVIE.TTF', 36)

        # Dibujar elementos del menú centrados en la ventana
        title_text = menu_font.render("Space Black (Jesus Morillo)", True, (255, 255, 255))
        title_text_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        window.blit(title_text, title_text_rect)

        start_text = menu_font.render("Presiona ENTER para comenzar", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        window.blit(start_text, start_text_rect)

        pygame.display.update()


main_menu()

gameloop()


                   




        
        































