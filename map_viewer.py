"""
map_viewer.py — Debug map viewer
À placer dans le même dossier que settings.py, world.py, etc.
Importe directement ton projet : toute modif de world.py / settings.py est reflétée ici.

Contrôles :
    Flèches / ZQSD   Déplacement
    +  /  -          Zoom (taille pixel par tuile)
    F5               Screenshot PNG
    Échap            Quitter

Options CLI :
    --seed N      Force une seed (sinon utilise celle de settings.py si déjà set, sinon aléatoire)
    --tile N      Pixels par tuile au démarrage (défaut: 4)
    --cx N        Chunk central X au démarrage (défaut: 0)
    --cy N        Chunk central Y au démarrage (défaut: 0)
"""

import sys
import argparse
import random
import pygame

# ── Import du projet ──────────────────────────────────────────────────────────
import settings
import world

# Palette : lit les couleurs directement depuis settings
# On mappe les valeurs de settings.Tile aux couleurs de settings.*
TILE_COLORS = {
    settings.Tile.EAU: settings.BLEU,
    settings.Tile.VILLE: settings.GRIS,
    settings.Tile.ROUTE: settings.NOIR,
    settings.Tile.MAISON: settings.ROUGE,
    settings.Tile.MAISONETTE: settings.ROUGE_CLAIR,
    settings.Tile.APPART: settings.BLANC,
    settings.Tile.PARC: settings.VERT_CLAIR,
    settings.Tile.CAMPAGNE: settings.GRIS_CLAIR,
    settings.Tile.FORET: settings.VERT,
    settings.Tile.ARBRE: settings.VERT_FONCE,
}

TILE_LABELS = {
    settings.Tile.EAU: "eau",
    settings.Tile.VILLE: "ville",
    settings.Tile.ROUTE: "route",
    settings.Tile.MAISON: "maison",
    settings.Tile.MAISONETTE: "maisonette",
    settings.Tile.APPART: "appartement",
    settings.Tile.PARC: "parc",
    settings.Tile.CAMPAGNE: "campagne",
    settings.Tile.FORET: "forêt",
    settings.Tile.ARBRE: "arbre",
}

STEP = 8  # tuiles par pression de touche


def render_map(map_surf, origin_tx, origin_ty, w_tiles, h_tiles, tile_px):
    """Dessine toutes les tuiles visibles via world.get_chunk (ton vrai système de chunks)."""
    map_surf.fill((30, 30, 30))

    for dy in range(h_tiles):
        for dx in range(w_tiles):
            tx = origin_tx + dx
            ty = origin_ty + dy

            cx = tx // settings.taille_chunk
            cy = ty // settings.taille_chunk
            lx = tx % settings.taille_chunk
            ly = ty % settings.taille_chunk

            # Gère les coordonnées négatives (modulo Python est toujours positif)
            if lx < 0:
                lx += settings.taille_chunk
                cx -= 1
            if ly < 0:
                ly += settings.taille_chunk
                cy -= 1

            chunk = world.get_chunk(cx, cy)
            tile = chunk[ly][lx]

            color = TILE_COLORS.get(tile, (255, 0, 255))  # magenta = tuile inconnue
            pygame.draw.rect(
                map_surf, color, (dx * tile_px, dy * tile_px, tile_px, tile_px)
            )

    # Grille chunk (optionnel, utile pour débugger)
    if tile_px >= 3:
        for dy in range(h_tiles):
            for dx in range(w_tiles):
                tx = origin_tx + dx
                ty = origin_ty + dy
                if tx % settings.taille_chunk == 0 or ty % settings.taille_chunk == 0:
                    pygame.draw.rect(
                        map_surf,
                        (0, 0, 0, 80),
                        (dx * tile_px, dy * tile_px, tile_px, tile_px),
                        1,
                    )


def draw_hud(screen, seed, origin_tx, origin_ty, w_tiles, h_tiles, tile_px, font):
    """Overlay : infos + légende."""
    pad = 8
    lines = [
        f"seed: {seed}",
        f"origine tuile : ({origin_tx}, {origin_ty})",
        f"vue : {w_tiles} x {h_tiles} tuiles  |  zoom : {tile_px}px/tuile",
        f"chunks en cache : {len(world.chunks)}",
        f"[flèches/ZQSD] déplacer   [+/-] zoom   [F5] screenshot   [Échap] quitter",
    ]

    # fond semi-transparent
    hud_h = len(lines) * (font.get_linesize() + 2) + pad * 2
    hud_surf = pygame.Surface((screen.get_width(), hud_h), pygame.SRCALPHA)
    hud_surf.fill((0, 0, 0, 150))
    screen.blit(hud_surf, (0, 0))

    y = pad
    for line in lines:
        surf = font.render(line, True, (220, 220, 220))
        screen.blit(surf, (pad, y))
        y += font.get_linesize() + 2

    # légende à droite
    leg_x = screen.get_width() - 155
    leg_y = pad
    leg_surf = pygame.Surface((150, len(TILE_LABELS) * 18 + pad * 2), pygame.SRCALPHA)
    leg_surf.fill((0, 0, 0, 150))
    screen.blit(leg_surf, (leg_x - 4, leg_y))

    for tile, label in TILE_LABELS.items():
        color = TILE_COLORS[tile]
        pygame.draw.rect(screen, color, (leg_x, leg_y, 12, 12))
        pygame.draw.rect(screen, (200, 200, 200), (leg_x, leg_y, 12, 12), 1)
        txt = font.render(label, True, (220, 220, 220))
        screen.blit(txt, (leg_x + 16, leg_y))
        leg_y += 18


def main():
    parser = argparse.ArgumentParser(
        description="Debug map viewer — importe directement ton projet"
    )
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--tile", type=int, default=4)
    parser.add_argument("--cx", type=int, default=0)
    parser.add_argument("--cy", type=int, default=0)
    args = parser.parse_args()

    # Seed : CLI > settings déjà set > aléatoire
    if args.seed is not None:
        settings.seed = args.seed
    elif not hasattr(settings, "seed") or settings.seed is None:
        settings.seed = random.randint(0, 100)

    seed = settings.seed
    tile_px = max(1, args.tile)

    # Taille de fenêtre initiale (80% de l'écran)
    pygame.init()
    info = pygame.display.Info()
    win_w = int(info.current_w * 0.85)
    win_h = int(info.current_h * 0.85)
    screen = pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)
    pygame.display.set_caption(f"Debug Map Viewer  |  seed {seed}")
    font = pygame.font.SysFont("monospace", 12)
    clock = pygame.time.Clock()

    w_tiles = win_w // tile_px
    h_tiles = win_h // tile_px

    # Centrage sur le chunk de départ
    origin_tx = args.cx * settings.taille_chunk - w_tiles // 2
    origin_ty = args.cy * settings.taille_chunk - h_tiles // 2

    map_surf = pygame.Surface((win_w, win_h))
    dirty = True

    print(
        f"[map_viewer] seed={seed} | chunk départ=({args.cx},{args.cy}) | tuile={tile_px}px"
    )

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key in (pygame.K_LEFT, pygame.K_q):
                    origin_tx -= STEP
                    dirty = True
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    origin_tx += STEP
                    dirty = True
                elif event.key in (pygame.K_UP, pygame.K_z):
                    origin_ty -= STEP
                    dirty = True
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    origin_ty += STEP
                    dirty = True

                elif event.key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                    tile_px = min(tile_px + 1, 20)
                    w_tiles = win_w // tile_px
                    h_tiles = win_h // tile_px
                    dirty = True

                elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    tile_px = max(tile_px - 1, 1)
                    w_tiles = win_w // tile_px
                    h_tiles = win_h // tile_px
                    dirty = True

                elif event.key == pygame.K_F5:
                    fname = f"map_seed{seed}_{origin_tx}_{origin_ty}.png"
                    pygame.image.save(screen, fname)
                    print(f"[map_viewer] Screenshot → {fname}")

            elif event.type == pygame.VIDEORESIZE:
                win_w, win_h = event.w, event.h
                w_tiles = win_w // tile_px
                h_tiles = win_h // tile_px
                map_surf = pygame.Surface((win_w, win_h))
                dirty = True

        if dirty:
            pygame.display.set_caption(f"Debug Map Viewer  |  seed {seed}  |  rendu...")
            render_map(map_surf, origin_tx, origin_ty, w_tiles, h_tiles, tile_px)
            pygame.display.set_caption(
                f"Debug Map Viewer  |  seed {seed}  |  ({origin_tx},{origin_ty})"
            )
            dirty = False

        screen.blit(map_surf, (0, 0))
        draw_hud(screen, seed, origin_tx, origin_ty, w_tiles, h_tiles, tile_px, font)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
