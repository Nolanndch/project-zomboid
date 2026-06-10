import settings
from noise import pnoise2
import pygame
import player
import world


def game(screen):
    screen.fill(settings.BLEU_CLAIR)


def afficher_joueur(surface):
    color = (255, 0, 0)  # rouge pour le moment
    taille = settings.taille_joueur
    pygame.draw.rect(
        surface, color, (settings.ecran_x, settings.ecran_y, taille, taille)
    )


def afficher_map(surface, offset_x, offset_y):

    cx = player.joueur.x // settings.tile_size // settings.taille_chunk
    cy = player.joueur.y // settings.tile_size // settings.taille_chunk

    # genere les 9x9 premiers chunks
    for cdx in range(-3, 4):
        for cdy in range(-2, 3):
            world.get_chunk(cx + cdx, cy + cdy)

    chunk_a_supprimer = []
    for cx2, cy2 in world.chunks.keys():
        if abs(cx2 - cx) > 3 or abs(cy2 - cy) > 2:
            chunk_a_supprimer.append((cx2, cy2))

    for key in chunk_a_supprimer:
        del world.chunks[key]

    # dessine les chunks generés
    for (cx, cy), tiles in world.chunks.items():
        for tile_y, ligne in enumerate(tiles):
            for tile_x, tuile in enumerate(ligne):

                # position des tiles
                tile_pos_x = (
                    cx * settings.taille_chunk + tile_x
                ) * settings.tile_size - offset_x
                tile_pos_y = (
                    cy * settings.taille_chunk + tile_y
                ) * settings.tile_size - offset_y

                if tuile == "ville":
                    color = settings.GRIS
                if tuile == "campagne":
                    color = settings.GRIS_CLAIR
                if tuile == "foret":
                    color = settings.VERT
                if tuile == "eau":
                    color = settings.BLEU
                if tuile == "route":
                    color = settings.NOIR

                pygame.draw.rect(
                    surface,
                    color,
                    (
                        tile_pos_x,
                        tile_pos_y,
                        settings.tile_size,
                        settings.tile_size,
                    ),
                )
