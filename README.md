# Mini Project Zomboid

Au départ, je voulais faire un vrai jeu de survie inspiré de *Project Zomboid* : une ville
différente à chaque partie, des zombies, un inventaire et tout le reste. Au final, je me suis
surtout pris au jeu de la génération de la carte, et le projet est devenu ma mise en pratique de
la **génération procédurale** en Python. La partie jeu (zombies, objets) est restée à l'état
d'ébauche.

Ma feuille de route de départ est dans [`roadmap_mini_zomboid.md`](roadmap_mini_zomboid.md).

## Ce qui marche

- **Un monde infini découpé en chunks** de 16×16 tuiles. Un chunk n'est généré que quand le
  joueur s'en approche, puis il reste en mémoire.
- **Plusieurs couches de bruit de Perlin** (`noise.pnoise2`) :
  1. un premier bruit décide si une tuile est de la terre ou de l'océan ;
  2. un deuxième répartit les biomes sur la terre : ville, campagne ou forêt ;
  3. dans les villes, les routes forment une grille (une route toutes les 10 tuiles) et un
     troisième bruit place des quartiers de maisons, d'appartements et de parcs. En campagne et
     en forêt, un tirage aléatoire par tuile place des maisonnettes et des arbres.
- **Une seed** : la même seed redonne toujours exactement la même carte.
- **Un joueur** qui se déplace dans le monde, avec la caméra centrée sur lui.
- **Un visualiseur de carte** (`map_viewer.py`) pour parcourir le monde généré, zoomer et faire
  des captures d'écran.

## Lancer le projet

```bash
pip install pygame noise
python main.py         # se balader dans le monde (flèches, Échap pour quitter)
python map_viewer.py   # explorer la carte
```

Dans le visualiseur, on se déplace avec les flèches ou ZQSD, on zoome avec `+` et `-`, F5 fait
une capture PNG et Échap quitte. On peut aussi lui passer des options : `--seed N`, `--tile N`
(pixels par tuile), `--cx N` et `--cy N` (chunk de départ).

## Comment le code est organisé

- `world.py` : la génération des chunks et des biomes
- `settings.py` : la taille des chunks et des tuiles, la seed, les types de tuiles et les couleurs
- `main.py` : la boucle de jeu et la caméra
- `player.py` : les déplacements du joueur
- `ui.py` : l'affichage de la carte et du joueur
- `map_viewer.py` : l'outil pour visualiser la carte
- `zombie.py`, `item.py`, `function.py` : les débuts de la partie jeu, que je n'ai pas continués
