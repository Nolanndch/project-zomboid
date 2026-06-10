import pygame

pygame.init()

screen = pygame.display.set_mode()
largeur_ecran, hauteur_ecran = screen.get_size()
ecran_x = largeur_ecran // 2
ecran_y = hauteur_ecran // 2

clock = pygame.time.Clock()

taille_map = 200
tile_size = 20

taille_chunk = 16

game_state = "game"

seed = 0

diviseur_noise = 500

taille_joueur = tile_size


class Tile:
    EAU = "eau"
    EAU_PROFONDE = "eau_profonde"
    FORET = "foret"
    VILLE = "ville"
    CAMPAGNE = "campagne"
    ROUTE = "route"


# couleurs :

NOIR = (0, 0, 0)
GRIS_FONCE = (30, 30, 30)
GRIS = (60, 60, 60)
GRIS_CLAIR = (120, 120, 120)
BLANC = (230, 230, 230)
ROUGE_FONCE = (120, 40, 40)
ROUGE = (200, 80, 80)
ROUGE_CLAIR = (230, 120, 120)
VERT_FONCE = (40, 120, 80)
VERT = (80, 200, 120)
VERT_CLAIR = (140, 230, 180)
BLEU_FONCE = (40, 80, 120)
BLEU = (100, 150, 220)
BLEU_CLAIR = (160, 200, 240)
JAUNE_FONCE = (160, 130, 50)
JAUNE = (230, 180, 70)
JAUNE_CLAIR = (250, 220, 150)
VIOLET_FONCE = (90, 60, 120)
VIOLET = (150, 110, 190)
VIOLET_CLAIR = (200, 160, 230)
MARRON = (120, 90, 60)
ORANGE = (220, 140, 60)
CYAN = (80, 200, 200)
