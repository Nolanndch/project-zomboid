class zombie :
    def __init__(self, x, y):
        self.life = 50
        self.strengh = 10
        self.x = x
        self.y = y
        self.vitesse = 80
        

    def move(self, direction, delta):
        if direction == "up":
            self.y = self.y - (self.vitesse * delta)
        elif direction == "down":
            self.y = self.y + (self.vitesse * delta)
        elif direction == "left":
            self.x = self.x - (self.vitesse * delta)
        else:
            self.x = self.x + (self.vitesse * delta)
    
    def attaquer(self,cible):
        cible.life - self.strengh 
        
    def __repr__(self):
        return f"pos : {self.x,self.y} /n life : {self.life}"
    
    def __str__(self):
        return f"pos : {self.x,self.y} /n life : {self.life}"