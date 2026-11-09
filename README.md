# Mini Project Zomboid : génération procédurale

Au départ, ce projet devait devenir un **jeu de survie complet** inspiré de *Project Zomboid* :
une ville générée à chaque partie, des zombies, un inventaire et de la survie. Il est finalement
devenu un **exercice pratique de génération procédurale de cartes** en Python et Pygame. La partie
jeu (zombies, objets) est restée au stade d'ébauche.

La feuille de route d'origine se trouve dans [`roadmap_mini_zomboid.md`](roadmap_mini_zomboid.md).

## Ce qui fonctionne

- **Un monde infini découpé en chunks** de 16×16 tuiles. Un chunk n'est généré que lorsqu'on
  s'en approche, puis il est gardé en mémoire.
- **Du bruit de Perlin à plusieurs couches** (`noise.pnoise2`) :
  1. Le premier bruit décide si une tuile est de la terre ou de l'océan.
  2. Le deuxième bruit répartit les biomes sur la terre : ville, campagne et forêt.
  3. Les villes ont des routes en grille, toutes les 10 tuiles, et un troisième bruit y répartit
     des quartiers de maisons, d'appartements et de parcs. En campagne et en forêt, un tirage
     aléatoire par tuile, toujours le même pour une seed donnée, place des maisonnettes et des arbres.
- **Une seed reproductible** : la même seed donne toujours la même carte.
- **Un joueur** qui se déplace dans le monde, avec une caméra centrée sur lui.
- **Un visualiseur de carte** (`map_viewer.py`) pour parcourir et zoomer sur le monde généré,
  et faire des captures d'écran.

## Lancer le projet

```bash
pip install pygame noise
python main.py           # se déplacer dans le monde (flèches, Échap pour quitter)
python map_viewer.py     # explorer la carte générée
```

Options du visualiseur : `--seed N`, `--tile N` (pixels par tuile), `--cx N` et `--cy N`
(chunk de départ). Commandes : flèches ou ZQSD pour se déplacer, `+` et `-` pour zoomer,
F5 pour une capture PNG, Échap pour quitter.

## Organisation du code

| Fichier | Rôle |
|---------|------|
| `world.py` | Génération des chunks et des biomes (bruit de Perlin) |
| `settings.py` | Taille des chunks et des tuiles, seed, types de tuiles, couleurs |
| `main.py` | Boucle de jeu et caméra |
| `player.py` | Déplacement du joueur |
| `ui.py` | Affichage de la carte et du joueur |
| `map_viewer.py` | Outil de débogage pour visualiser la carte |
| `zombie.py`, `item.py`, `function.py` | Ébauches de la partie jeu, jamais terminées |
