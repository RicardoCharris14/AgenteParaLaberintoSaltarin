from abc import ABC, abstractmethod

FILA = 1
COLUMNA = 0

class Bot(ABC):
    def __init__(self):
        self.laberinto = None
        self.pos = None
        self.revisados = None
        self.width = None
        self.height = None
        self.camino = None
    
    def seleccionarLaberinto(self, laberinto, pos):
        self.laberinto = laberinto
        self.pos = pos
        self.revisados = [[False for _ in laberinto[0]] for _ in laberinto]
        self.width = len(laberinto[0])
        self.height = len(laberinto)
        self.camino = []

    @abstractmethod
    def resolverLaberinto(self):
        pass

class BotDFS(Bot):
    def __init__(self):
        super().__init__()
        self.vecinos = None
    
    def seleccionarLaberinto(self, laberinto, pos):
        super().seleccionarLaberinto(laberinto, pos)
        self.vecinos = []
        
    def resolverLaberinto(self):
        while True:
            self.revisados[self.pos[FILA]][self.pos[COLUMNA]] = True
            self.camino.append((self.pos[0], self.pos[1]))
            salto = self.laberinto[self.pos[FILA]][self.pos[COLUMNA]]

            if (salto == 0):
                return self.camino

            for i in range(-1, 2, 2):
                x = self.pos[0] + i*salto
                y = self.pos[1]
                if (0 <= x < self.width):
                    if (not self.revisados[y][x]):
                        self.vecinos.append(((x, y), (self.pos[0], self.pos[1])))
                        self.revisados[y][x] = True

            for i in range(-1, 2, 2):
                x = self.pos[0]
                y = self.pos[1] + i*salto
                if (0 <= y < self.height):
                    if (not self.revisados[y][x]):
                        self.vecinos.append(((x, y), (self.pos[0], self.pos[1])))
                        self.revisados[y][x] = True
            
            if (self.vecinos and (self.vecinos[-1][1][0] != self.pos[0] or  self.vecinos[-1][1][1] != self.pos[1]) and self.camino):
                self.camino.pop()
                self.pos = self.camino[-1]
                continue

            if (self.vecinos):
                sigVecino = self.vecinos.pop()
                self.pos = (sigVecino[0][0], sigVecino[0][1])
            else:
                return []
            