import settings
import random
from noise import pnoise2

chunks = {}  # { (cx, cy): [[tiles]] }


def set_biome_tuile(tuile_x, tuile_y, biome):

    if biome == "ville":  # placement du contenu des villes

        n3 = pnoise2(
            (tuile_x // 10) / 1.5,
            (tuile_y // 10) / 1.5,
            base=(settings.seed + 2),
        )

        if tuile_x % 10 == 0 or tuile_y % 10 == 0:
            return settings.Tile.ROUTE  # definition d'une route sur la ville
        elif n3 > 0.2:
            return settings.Tile.PARC
        elif n3 < -0.2:
            return settings.Tile.APPART
        elif 0.15 > n3 > -0.15:
            return settings.Tile.MAISON
        else:
            return settings.Tile.VILLE

    elif biome == "campagne":  # placement du contenu de la campagne
        r = random.Random(str((tuile_x, tuile_y, settings.seed)))

        if 0.3 > r.random() > 0.2:
            return settings.Tile.MAISONETTE
        else:
            return settings.Tile.CAMPAGNE

    elif biome == "foret":  # placement du contenu de la foret
        r = random.Random(str((tuile_x, tuile_y, settings.seed)))

        if 0.4 > r.random() > 0.1:
            return settings.Tile.ARBRE
        else:
            return settings.Tile.FORET


def generate_chunk(cx, cy):
    chunk = []
    for y in range(settings.taille_chunk):
        ligne = []
        for x in range(settings.taille_chunk):

            tuile_x = cx * settings.taille_chunk + x
            tuile_y = cy * settings.taille_chunk + y

            # noise1 terre ou mer ?
            n1 = pnoise2(
                tuile_x / settings.diviseur_noise,
                tuile_y / settings.diviseur_noise,
                base=settings.seed,
                octaves=3,
                persistence=0.40,
            )

            if n1 > 0:
                ligne.append(settings.Tile.EAU)  # c'est l'ocean

            else:  # definition des biomes sur terre grace a un 2eme pnoise
                n2 = pnoise2(
                    tuile_x / (settings.diviseur_noise * 1.5),
                    tuile_y / (settings.diviseur_noise * 1.5),
                    base=(settings.seed + 1),
                    octaves=6,
                    persistence=0.50,
                )

                if -0.05 < n2 < 0.05:  # biome ville

                    biome = "ville"

                elif -0.2 < n2 < 0.1:  # biome campouze
                    biome = "campagne"

                else:  # biome foret
                    biome = "foret"

                ligne.append(set_biome_tuile(tuile_x, tuile_y, biome))

        chunk.append(ligne)
    return chunk


def get_chunk(cx, cy):
    if (cx, cy) not in chunks:
        new_chunk = generate_chunk(cx, cy)
        chunks[(cx, cy)] = new_chunk
    return chunks[(cx, cy)]
