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
- [✅] Initialiser pygame + boucle de jeu (`while running: events → update → draw`)
- [✅] Joueur : rectangle ou sprite, déplacement 8 directions
- [✅] Tilemap statique codée en dur (tableau 2D : `0` = herbe, `1` = mur)
- [✅] Caméra centrée sur le joueur (`offset_x = joueur.x - SCREEN_W // 2`)
- [✅] Collision joueur ↔ murs (tuiles de type `1`)

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
- [✅] Découper la map en **chunks** (zones 16×16 tuiles)
- [✅] Génération de routes (grille régulière ou bruit de Perlin)
- [ ] Placement de bâtiments rectangulaires (murs + 1 porte)
- [✅] Seed reproductible : `random.seed(42)` → même seed = même map
- [✅] Charger uniquement les chunks proches du joueur (perf)

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

## Étape 5 — Cycle jour / nuit & lumière
> *La nuit, tout devient hostile — la lampe devient vitale*

Ce système se décompose en **4 sous-étapes** à faire dans l'ordre.

---

### 5a — L'overlay de nuit (obscurité globale)

**Objectif :** l'écran s'assombrit progressivement quand la nuit tombe.

#### À coder
- [ ] Variable `time_frac` qui avance avec `dt / DAY_DURATION` et boucle sur `% 1.0`
- [ ] Calcul de `ambient_alpha` selon la fraction du jour (0 = midi, 210 = minuit)
- [ ] Surface SRCALPHA remplie avec la couleur nuit + alpha calculé
- [ ] Blitter cet overlay **après** le monde et le joueur, **avant** le HUD

#### 💡 Astuces
- `time_frac` va de 0 à 1 : 0 = minuit, 0.25 = aube, 0.5 = midi, 0.75 = crépuscule
- Transitions douces : utilise un `lerp` (interpolation linéaire) entre les paliers
- `DAY_DURATION = 60` pour tester vite, monte à `600` pour une vraie ambiance
- **Ordre de rendu critique :** `world → player → overlay_nuit → HUD`
  Si le HUD passe sous l'overlay, il sera assombri lui aussi !

#### 📚 Ressources si tu bloques
- [pygame.Surface avec SRCALPHA (doc)](https://www.pygame.org/docs/ref/surface.html)
- Demande-moi : *"génère-moi un overlay jour/nuit avec transitions douces"*

---

### 5b — La zone de lumière (trou dans l'obscurité)

**Objectif :** le joueur voit uniquement dans un petit rayon autour de lui la nuit.

#### À coder
- [ ] Créer un `light_mask` : surface SRCALPHA, opaque partout sauf au centre
- [ ] Gradient du centre (transparent) vers le bord (opaque) avec des cercles concentriques
- [ ] Blitter le masque sur l'overlay avec `pygame.BLEND_RGBA_MIN`
- [ ] Centrer le trou sur la position écran du joueur

#### 💡 Astuces
- `BLEND_RGBA_MIN` prend le **minimum** des deux alpha : là où le masque a 0, l'overlay devient 0 (trou)
- Le gradient se crée en dessinant des cercles pleins **du plus grand au plus petit**, chaque cercle écrasant le précédent avec un alpha plus faible → le centre finit presque transparent
- **Met le masque en cache** (dict `radius → Surface`) : le recalculer chaque frame tue les perfs
- Le joueur est toujours au centre de l'écran → `player_screen_pos = (SCREEN_W//2, SCREEN_H//2)`

#### 📚 Ressources si tu bloques
- [BLEND_RGBA_MIN expliqué (pygame doc)](https://www.pygame.org/docs/ref/surface.html#pygame.Surface.blit)
- Demande-moi : *"génère-moi un masque de lumière circulaire avec gradient pour pygame"*

---

### 5c — La lampe (item qui étend la vision)

**Objectif :** trouver une lampe dans le monde change radicalement le gameplay.

#### À coder
- [ ] Booléen `lamp_on` dans le joueur ou le `LightingSystem`
- [ ] Touche `[F]` pour allumer/éteindre
- [ ] Deux constantes : `RADIUS_NIGHT = TILE_SIZE * 3` et `RADIUS_LAMP = TILE_SIZE * 9`
- [ ] Le rayon du trou de lumière change selon `lamp_on`
- [ ] (Bonus) La lampe consomme une batterie qui se vide avec le temps

#### 💡 Astuces
- Commence par un toggle au clavier, lie-le à l'inventaire à l'étape 6
- Quand la lampe change de rayon, invalide le cache des masques (ou garde les deux en cache dès le départ)
- Pour la batterie : `battery -= dt * DRAIN_RATE`, `lamp_on = False` si `battery <= 0`

#### 📚 Ressources si tu bloques
- Demande-moi : *"génère-moi un système de lampe avec batterie qui se vide"*

---

### 5d — Comportement des zombies la nuit

**Objectif :** la nuit est vraiment dangereuse.

#### À coder
- [ ] Les zombies ont un `detection_radius` plus grand la nuit (`x2`)
- [ ] Vitesse légèrement augmentée la nuit
- [ ] (Bonus) Les zombies sont attirés par la lumière de la lampe (inverse de la discrétion)
- [ ] Spawn rate plus élevé la nuit

#### 💡 Astuces
- Passe `lighting.is_night` au `Spawner` pour ajuster le spawn rate
- Pour l'attraction à la lampe : si `lamp_on`, les zombies dans un grand rayon s'orientent vers le joueur même sans ligne de vue directe

---

## Étape 6 — Exploration & ambiance
> *Donner envie d'explorer*

### À coder
- [ ] **Brouillard de guerre** : tuiles non visitées assombries (overlay semi-transparent)
- [ ] Loot dans les bâtiments (spawn pondéré : `random.choices(items, weights=[...])`)
- [ ] Sons : bruits de pas, grognements, ambiance (`pygame.mixer`)
- [ ] Mini-map dans un coin (rendu de la map à petite échelle)

### 💡 Astuces
- Brouillard de guerre = un second tableau 2D `visited[][]` mis à jour autour du joueur
- Sons gratuits & libres de droits : [freesound.org](https://freesound.org) (cherche "zombie groan", "footstep gravel")
- Mini-map : rendu dans un `Surface` séparé avec `pygame.transform.scale`

### 📚 Ressources si tu bloques
- [pygame.mixer — doc officielle](https://www.pygame.org/docs/ref/mixer.html)
- [Freesound.org](https://freesound.org) — sons gratuits, téléchargement avec compte free
- Demande-moi : *"génère-moi un brouillard de guerre simple avec tableau visited[][]*"

---

## Étape 7 — Polish & contenu
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
├── settings.py       # Constantes (TILE_SIZE, SCREEN_W, FPS, DAY_DURATION…)
├── player.py         # Classe Player
├── zombie.py         # Classe Zombie + IA
├── world.py          # Génération de la map + chunks
├── items.py          # Items, inventaire, loot
├── camera.py         # Offset caméra
├── lighting.py       # Cycle jour/nuit, overlay, masque de lumière, lampe
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
