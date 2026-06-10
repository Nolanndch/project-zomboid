import settings
from noise import pnoise2

chunks = {}  # { (cx, cy): [[tiles]] }


def generate_chunk(cx, cy):
    chunk = []
    for y in range(settings.taille_chunk):
        ligne = []
        for x in range(settings.taille_chunk):

            noise_x = cx * settings.taille_chunk + x
            noise_y = cy * settings.taille_chunk + y

            # noise1 terre ou mer ?
            n1 = pnoise2(
                noise_x / settings.diviseur_noise,
                noise_y / settings.diviseur_noise,
                base=settings.seed,
                octaves=6,
                persistence=0.40,
            )

            if n1 > 0:
                ligne.append(settings.Tile.EAU)  # c'est l'ocean

            else:  # definition des biomes sur terre grace a un 2eme pnoise
                n2 = pnoise2(
                    noise_x / (settings.diviseur_noise * 1.5),
                    noise_y / (settings.diviseur_noise * 1.5),
                    base=(settings.seed + 1),
                    octaves=6,
                    persistence=0.50,
                )

                if -0.05 < n2 < 0.05:  # biome ville
                    if x % 10 == 0 or y % 10 == 0:
                        ligne.append(settings.Tile.ROUTE)

                    ligne.append(settings.Tile.VILLE)

                elif -0.1 < n2 < 0.1:  # biome campouze

                    ligne.append(settings.Tile.CAMPAGNE)

                else:  # biome foret

                    ligne.append(settings.Tile.FORET)

        chunk.append(ligne)
    return chunk


def get_chunk(cx, cy):
    if (cx, cy) not in chunks:
        new_chunk = generate_chunk(cx, cy)
        chunks[(cx, cy)] = new_chunk
    return chunks[(cx, cy)]
