import settings
import world


class Player:
    def __init__(self, x, y, life=100, strengh=10):
        self.life = life
        self.strengh = strengh
        self.x = x
        self.y = y
        self.vitesse = 200

    def move(self, direction, delta):
        if direction == "up":
            self.y = self.y - (self.vitesse * delta)
        elif direction == "down":
            self.y = self.y + (self.vitesse * delta)
        elif direction == "left":
            self.x = self.x - (self.vitesse * delta)
        else:
            self.x = self.x + (self.vitesse * delta)


joueur = Player(0, 0)
