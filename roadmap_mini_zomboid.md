# 🧟 Mini Project Zomboid — Roadmap de développement
> Python + Pygame + Génération procédurale
> Suis les étapes dans l'ordre — chaque étape est jouable avant de passer à la suivante.

---

## ⚙️ Setup initial

```bash
pip install pygame noise
```

> **Si pygame ne s'installe pas** → [pygame.org/wiki/GettingStarted](https://www.pygame.org/wiki/GettingStarted)  
> **Si tu es sur Mac (Apple Silicon)** → préfère `pip install pygame-ce` (fork communautaire plus stable)

---

## Étape 1 — Socle technique
> *Une fenêtre qui tourne, un perso qui bouge*

### À coder
- [ ] Initialiser pygame + boucle de jeu (`while running: events → update → draw`)
- [ ] Joueur : rectangle ou sprite, déplacement 8 directions
- [ ] Tilemap statique codée en dur (tableau 2D : `0` = herbe, `1` = mur)
- [ ] Caméra centrée sur le joueur (`offset_x = joueur.x - SCREEN_W // 2`)
- [ ] Collision joueur ↔ murs (tuiles de type `1`)

### 💡 Astuces
- Commence avec `pygame.draw.rect()` pour tout — les sprites viennent bien plus tard
- La boucle de jeu a toujours la même structure : **events → update → draw → flip**
- `dt = clock.tick(60) / 1000` → utilise le delta time pour un mouvement fluide indépendant du FPS

### 📚 Ressources si tu bloques
- [Tutoriel boucle pygame (anglais)](https://www.pygame.org/docs/tut/newbieguide.html) — le guide officiel newbie, très clair
- [Clear Code — Pygame for Beginners (YouTube)](https://www.youtube.com/watch?v=AY9MnQ4x3zk) — 3h de tuto, parfait pour poser les bases
- Demande-moi : *"génère-moi le squelette de la boucle de jeu pygame avec caméra"*

---

## Étape 2 — Génération procédurale de la map
> *Une ville différente à chaque partie*

### À coder
- [ ] Découper la map en **chunks** (zones 16×16 tuiles)
- [ ] Génération de routes (grille régulière ou bruit de Perlin)
- [ ] Placement de bâtiments rectangulaires (murs + 1 porte)
- [ ] Seed reproductible : `random.seed(42)` → même seed = même map
- [ ] Charger uniquement les chunks proches du joueur (perf)

### 💡 Astuces
- Pour les bâtiments : génère d'abord une liste de rectangles non-superposés, puis dessine les murs autour
- Le **bruit de Perlin** (`from noise import pnoise2`) donne des terrains organiques, pas du pur random
- Un chunk = un dict `{(cx, cy): [[tiles]]}` chargé à la demande → évite de tout stocker en RAM

### 📚 Ressources si tu bloques
- [Procgen wiki — Terrain generation](https://roguebasin.com/index.php/Terrain_generation) — plein d'algos expliqués simplement
- [Vidéo Perlin noise en Python (YouTube)](https://www.youtube.com/watch?v=ZsEnnB2wrbI)
- [Documentation `noise` (PyPI)](https://pypi.org/project/noise/)
- Demande-moi : *"génère-moi un système de chunks 16x16 avec bruit de Perlin"*

---

## Étape 3 — Zombies & IA basique
> *Des ennemis qui réagissent*

### À coder
- [ ] Classe `Zombie` avec machine à états : `IDLE → WANDER → CHASE → ATTACK`
- [ ] Détection joueur par distance : `if dist(zombie, joueur) < RAYON_VISION`
- [ ] Déplacement vers le joueur (pathfinding direct, pas d'A* pour l'instant)
- [ ] Collision zombies ↔ murs
- [ ] Spawner : faire apparaître les zombies hors champ de vision

### 💡 Astuces
- **Machine à états** = `self.state` + un `if/elif` dans `update()` → simple et lisible
- Le pathfinding direct (`dx = joueur.x - self.x`) suffit tant que les niveaux ne sont pas labyrinthiques
- Pour éviter que les zombies se superposent : ajoute une légère répulsion entre eux (`separation steering`)
- Spawn hors caméra : `if not camera_rect.colliderect(spawn_rect)`

### 📚 Ressources si tu bloques
- [Game AI Pro — Simple Zombie AI](http://www.gameaipro.com/) — gratuit en ligne, chapitres accessibles
- [Tech With Tim — Enemy AI pygame (YouTube)](https://www.youtube.com/results?search_query=pygame+enemy+ai+state+machine)
- [Red Blob Games — pathfinding intro](https://www.redblobgames.com/pathfinding/a-star/introduction.html) — le meilleur site pour comprendre A* quand tu en auras besoin
- Demande-moi : *"génère-moi une machine à états simple pour un zombie pygame"*

---

## Étape 4 — Combat & survie
> *Pouvoir mourir — et survivre*

### À coder
- [ ] Stats joueur : `health`, `stamina`, `hunger` (dégradation dans le temps)
- [ ] Attaque au corps à corps : hitbox temporaire + cooldown + knockback
- [ ] Inventaire minimaliste : liste de dicts `[{"nom": "bandage", "qte": 2}]`
- [ ] Items au sol (sprite ramassable au contact)
- [ ] Écran Game Over + restart propre

### 💡 Astuces
- Le **cooldown** d'attaque = `self.attack_timer -= dt`, attaque possible si `timer <= 0`
- Le **knockback** = une impulsion de vélocité appliquée au zombie pendant quelques frames
- Inventaire : commence par une liste simple, l'UI vient après
- `hunger` qui descend : un `hunger_rate = 0.5` unités/seconde suffit pour sentir la pression

### 📚 Ressources si tu bloques
- [Pygame hitbox & collision (doc officielle)](https://www.pygame.org/docs/ref/rect.html#pygame.Rect.colliderect)
- Demande-moi : *"génère-moi un système de combat au corps à corps avec cooldown et knockback"*

---

## Étape 5 — Exploration & ambiance
> *Donner envie d'explorer*

### À coder
- [ ] **Brouillard de guerre** : tuiles non visitées assombries (overlay semi-transparent)
- [ ] Loot dans les bâtiments (spawn pondéré : `random.choices(items, weights=[...])`)
- [ ] Sons : bruits de pas, grognements, ambiance (`pygame.mixer`)
- [ ] Cycle jour/nuit : filtre de luminosité `pygame.Surface` en mode `BLEND_RGBA_MULT`
- [ ] Mini-map dans un coin (rendu de la map à petite échelle)

### 💡 Astuces
- Brouillard de guerre = un second tableau 2D `visited[][]` mis à jour autour du joueur
- Pour le filtre nuit : un `Surface` noir en 60% d'opacité blitté sur tout l'écran fait l'effet
- Sons gratuits & libres de droits : [freesound.org](https://freesound.org) (cherche "zombie groan", "footstep gravel")
- Mini-map : rendu dans un `Surface` séparé avec `pygame.transform.scale`

### 📚 Ressources si tu bloques
- [pygame.mixer — doc officielle](https://www.pygame.org/docs/ref/mixer.html)
- [Freesound.org](https://freesound.org) — sons gratuits, téléchargement avec compte free
- Demande-moi : *"génère-moi un cycle jour/nuit avec filtre de luminosité pygame"*

---

## Étape 6 — Polish & contenu
> *Que ce soit "vrai"*

### À coder
- [ ] Sprites animés (spritesheet + `pygame.sprite.Sprite`)
- [ ] Plusieurs types de zombies (rapide, lourd, rampant)
- [ ] Sauvegarde : état joueur + seed map en JSON (`import json`)
- [ ] Menu principal + écran pause
- [ ] HUD propre : barres de vie, stamina, hunger

### 💡 Astuces
- Spritesheet : découpe avec `surface.subsurface(pygame.Rect(x, y, w, h))` à chaque frame
- Pour la sauvegarde : sauvegarde uniquement la **seed** + la **position joueur** + l'**inventaire** → la map se régénère identiquement depuis la seed
- Sprites zombies gratuits : [itch.io/tag-zombies](https://itch.io/game-assets/tag-zombies?price=free) (filtrer "free")

### 📚 Ressources si tu bloques
- [Pygame sprites & animation (YouTube — DaFluffyPotato)](https://www.youtube.com/c/DaFluffyPotato) — chaîne dédiée pygame, niveau intermédiaire
- [itch.io assets gratuits](https://itch.io/game-assets/free) — sprites, sons, tilesets
- Demande-moi : *"génère-moi un système de spritesheet animé pour pygame"*

---

## 🗂️ Structure de projet recommandée

```
mini_zomboid/
├── main.py           # Boucle principale
├── settings.py       # Constantes (TILE_SIZE, SCREEN_W, FPS…)
├── player.py         # Classe Player
├── zombie.py         # Classe Zombie + IA
├── world.py          # Génération de la map + chunks
├── items.py          # Items, inventaire, loot
├── camera.py         # Offset caméra
├── ui.py             # HUD, menus, Game Over
├── assets/
│   ├── sprites/
│   └── sounds/
└── saves/
    └── save.json
```

---

## 🧰 Stack complète

| Lib | Usage |
|---|---|
| `pygame` | Rendu, input, son, fenêtre |
| `noise` | Bruit de Perlin pour la génération |
| `json` | Sauvegarde |
| `random` | Tout le reste de la procgen |
| `math` | Distance, angles, vecteurs |

---

## 🆘 Si tu bloques vraiment

1. **Demande-moi directement** avec le contexte : *"à l'étape X, j'essaie de faire Y, voici mon code, ça fait Z"*
2. **Reddit** → [r/pygame](https://www.reddit.com/r/pygame/) — communauté active et bienveillante
3. **Stack Overflow** → tag `[pygame]` — cherche avant de poster, la plupart des bugs courants sont déjà résolus
4. **Discord Pygame** → [discord.gg/pygame](https://discord.gg/pygame)
5. **Doc officielle** → [pygame.org/docs](https://www.pygame.org/docs/) — exhaustive mais dense

---

*Bonne chance — commence par l'étape 1 et ne saute pas d'étapes ! 🧟*
