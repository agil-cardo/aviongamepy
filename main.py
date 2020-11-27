import pygame  # pygame modul pour faire des jeux en 2D
from game import Game
from input_box import InputBox, FONT
import time
import math
from Utilities.functions import save_score, lecture

pygame.init()

# generer la fenetre du jeu
# donner un nom à la fenetre
pygame.display.set_caption("Battle Ship")

# donner une taille à la fenetre
width = 1280
height = 720
# Fram par seconde
FPS = 60
title = 'Space Ship Battle'
# Fonts
pygame.font.init()
myfont = pygame.font.SysFont('Roboto', 80)
myfont2 = pygame.font.SysFont("monospace", 20)

screen = pygame.display.set_mode((width, height))
# screen_log = pygame.display.set_mode((width, height))

# Title
title_display = myfont.render(title, True, (20, 150, 250))
text_width, text_height = myfont.size(title)
title_pos_x, title_pos_y = (
    (screen.get_width() - text_width) / 2, (screen.get_height() - text_height) / 2)

# importer un fond
background = pygame.image.load(
    "assets/background/futurCity.jpg").convert_alpha()
# background = pygame.transform.scale(background, (width, height))

# importer charger notre bannière
banner = pygame.image.load("assets/home/ship.png").convert_alpha()
banner_rect = banner.get_rect()


# importer charger le bouton pour la partie
play_button = pygame.image.load(
    "assets/home/playNowButton1.png").convert_alpha()
play_button_rect = play_button.get_rect()

input_info = myfont2.render("Entrez votre pseudo", True, (250, 250, 250))

box = InputBox(math.ceil((width-200)/2),
               math.ceil((height - title_pos_y) + 32) + 20, 200, 32)


# instance d'avion
game = Game(box, width, height)

# on crée un boucle infini pour que la fenetre apparaisse tout le temps
running = True

# on regle l'image par seconde
clock = pygame.time.Clock()
pygame.mixer.music.load("assets/sounds/retro.ogg")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(3, 1)
while running:

    clock.tick(FPS)
    # Time
    seconds = int(pygame.time.get_ticks() / 1000)
    time_display = myfont2.render(
        f"Time in space : {seconds} s", 1, (50, 200, 50))
    time_width, time_height = myfont.size(f"Time in space : {seconds} s")
    time_pos_x = (screen.get_width()-time_width)/2

    # Score
    score = game.player.score
    last_score = game.player.last_score
    lv = game.player.lv
    score_display = myfont2.render(f"Score : {score}", 1, (50, 200, 50))
    last_score_display = myfont2.render(
        f"Derniere partie : {last_score} pts", 1, (50, 200, 50))

    # on injecte le fond à la fenetre du jeu

    if game.is_running:
        total_score = game.player.total
        total_score_display = myfont2.render(
            f"Total score : {total_score} pts", 1, (50, 200, 50))
        game.time += seconds
        n_player = myfont2.render(
            f"Joueur : {game.name_player}", 1, (50, 200, 50))
        lv_player = myfont2.render(
            f"lv : {lv}", 1, (50, 200, 50))
        screen.blit(background, (0, 0))
        game.start_game(screen)
        screen.blit(time_display, (350, 0))
        screen.blit(score_display, (350, 20))
        screen.blit(n_player, (screen.get_width()/2, 0))
        screen.blit(lv_player, (screen.get_width()/2, 20))
        screen.blit(total_score_display, (screen.get_width()-350, 0))
        screen.blit(last_score_display, (screen.get_width()-350, 20))
    else:
        screen.fill((0, 0, 0))
        screen.blit(banner, (banner_rect))
        screen.blit(title_display, (title_pos_x, title_pos_y))
        banner_rect.x = math.ceil(
            (screen.get_width()-banner.get_width()) / 2)
        banner_rect.y = math.ceil(
            (screen.get_height()-title_pos_y-text_height-banner.get_height())/2)
        screen.blit(play_button, (play_button_rect))
        play_button_rect.x = math.ceil(
            (screen.get_width()-play_button.get_width()) / 2)
        play_button_rect.y = screen.get_height() - math.ceil(
            screen.get_height() - box.rect.y - box.rect.h - play_button.get_height() / 2)
        if seconds % 2 == 0:
            screen.blit(input_info, (width / 2 -
                                     input_info.get_width() / 2,  height / 4*2.35))
        box.update()
        box.draw(screen)
        if box.is_error:
            box.error_surface = FONT.render(
                box.error, True, (255, 255, 255))
        else:
            box.error_surface = FONT.render(
                box.error, True, (0, 0, 0))
        game.name_player = box.text.strip()
        screen.blit(box.error_surface, (math.ceil((screen.get_width()-box.error_surface.get_width())/2), box.rect.y + box.rect.h + math.ceil(
            (play_button_rect.y-(box.rect.y+box.rect.h)-32)/2)))

    pygame.display.flip()

    # si le on ferme la fenetre
    for event in pygame.event.get():
        box.handle_event(event)
        box.verif(event, play_button_rect)
        # event de fermeture de la fenetre
        if event.type == pygame.QUIT:
            game.game_over()
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and box.is_error == False:
                game.start()
            game.keybord[event.key] = True
        elif event.type == pygame.KEYUP:
            game.keybord[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN and box.is_error == False:
            if play_button_rect.collidepoint(event.pos):
                game.start()
