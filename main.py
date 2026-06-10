import pygame
import settings
import player
import ui
import random

settings.seed = random.randint(0, 100)

dt = settings.clock.tick(60) / 1000

run = True

while run:
    offset_x = player.joueur.x - (settings.largeur_ecran // 2)
    offset_y = player.joueur.y - (settings.hauteur_ecran // 2)

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                run = False

    if settings.game_state == "game":

        # game logic
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            player.joueur.move("up", dt)

        if keys[pygame.K_DOWN]:
            player.joueur.move("down", dt)

        if keys[pygame.K_LEFT]:
            player.joueur.move("left", dt)

        if keys[pygame.K_RIGHT]:
            player.joueur.move("right", dt)

        # game render
        ui.game(settings.screen)
        ui.afficher_map(settings.screen, offset_x, offset_y)
        ui.afficher_joueur(settings.screen)

    pygame.display.flip()

pygame.quit()
