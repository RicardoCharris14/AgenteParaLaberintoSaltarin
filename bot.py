from abc import ABC, abstractmethod
import heapq

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
        self.end = None
    
    def seleccionarLaberinto(self, laberinto, start, end):
        self.laberinto = laberinto
        self.pos = start
        self.revisados = [[False for _ in laberinto[0]] for _ in laberinto]
        self.width = len(laberinto[0])
        self.height = len(laberinto)
        self.camino = []
        self.end = end

    @abstractmethod
    def resolverLaberinto(self):
        pass


class BotDFS(Bot):
    def __init__(self):
        super().__init__()
        self.vecinos = None
    
    def seleccionarLaberinto(self, laberinto, start, end):
        super().seleccionarLaberinto(laberinto, start, end)
        self.vecinos = []
        
    def resolverLaberinto(self):
        while True:
            self.revisados[self.pos[FILA]][self.pos[COLUMNA]] = True
            self.camino.append((self.pos[0], self.pos[1]))
            salto = self.laberinto[self.pos[FILA]][self.pos[COLUMNA]]

            if (self.end[0] == self.pos[0] and self.end[1] == self.pos[1]):
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
                self.camino.pop()
                continue

            if (self.vecinos):
                sigVecino = self.vecinos.pop()
                self.pos = (sigVecino[0][0], sigVecino[0][1])
            else:
                return []


class BotCU(Bot):
    def __init__(self):
        super().__init__()
        self.heap = None
        self.ancestros = None

    def seleccionarLaberinto(self, laberinto, start, end):
        super().seleccionarLaberinto(laberinto, start, end)
        self.heap = []
        self.ancestros = {}

    def resolverLaberinto(self):
        heapq.heappush(self.heap, (0, self.pos))
        while True:
            if (self.heap):
                peso, self.pos = heapq.heappop(self.heap)
            else:
                return []
            
            if (self.end[0] == self.pos[0] and self.end[1] == self.pos[1]):
                return [(self.pos[0], self.pos[1])]
            
            salto = self.laberinto[self.pos[FILA]][self.pos[COLUMNA]]
            for dx, dy in [(-salto, 0), (salto, 0), (0, -salto), (0, salto)]:
                x = self.pos[0] + dx
                y = self.pos[1] + dy
                if (0 <= x < self.width and 0 <= y < self.height):
                    if (not self.revisados[y][x]):
                        if (self.end[0] == x and self.end[1] == y):
                            self.camino = [None]*(peso+2)
                            self.camino[peso+1] = (x, y)
                            self.camino[peso] = (self.pos[0], self.pos[1])
                            aux = (self.pos[0], self.pos[1])
                            for i in range(peso-1, -1, -1):
                                anterior = self.ancestros[aux]
                                self.camino[i] = anterior
                                aux = anterior
                            return self.camino

                        heapq.heappush(self.heap, (peso+1, (x,y)))
                        self.ancestros[(x, y)] = (self.pos[0], self.pos[1])
                        self.revisados[y][x] = True


        
            