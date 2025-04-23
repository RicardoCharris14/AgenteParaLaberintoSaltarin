import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 60
FramesPerSecond = pygame.time.Clock()

#tamaño de la pantalla
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 300

#colores
GREY = pygame.Color(150, 150, 150)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
LIGHT_BLUE = pygame.Color(50, 50, 255)

DISPLAY = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class Laberinto:
    def __init__(self, matriz, start, end):
        #variables inherentes al laberinto
        self.end = end
        self.posicion = start
        self.matriz = matriz
        self.movimientos = 0
        self.completo = False

        #variables para dibujar el laberinto
        self.tamanoCelda = 50
        self.interEspaciadoCelda = 5
        self.inicioCuadricula = 11


    def iniciarJuego(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.exit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    self.click(event.pos)

            self.draw()

            pygame.display.update()
            FramesPerSecond.tick(60)
    
    def click(self, pos):
        distanciaMov = self.matriz[self.posicion[1]][self.posicion[0]]

        # Se verifica que el click sea dentro de una casilla y que la casilla este a una distancia de la casilla actual igual al numero de la casilla actual, en tal caso se realiza el movimiento
        x = (pos[0]-self.inicioCuadricula)//(self.tamanoCelda+self.interEspaciadoCelda)
        y = (pos[1]-self.inicioCuadricula)//(self.tamanoCelda+self.interEspaciadoCelda)
        if ((x - (pos[0]-(self.tamanoCelda+self.inicioCuadricula))//(self.tamanoCelda+self.interEspaciadoCelda)) != 0 and (y - (pos[1]-(self.tamanoCelda+self.inicioCuadricula))//(self.tamanoCelda+self.interEspaciadoCelda)) != 0):
            if ((abs(self.posicion[0] - x) == distanciaMov and self.posicion[1] == y) or (abs(self.posicion[1] - y) == distanciaMov and self.posicion[0] == x)):
                self.posicion[0] = x
                self.posicion[1] = y
                self.movimientos+=1

    
    def draw(self):
        fuente = pygame.font.Font(None, 24)
        DISPLAY.fill(GREY)
        #Dibuja la cuadricula
        for i in range(len(self.matriz)):
            for j in range(len(self.matriz[0])):
                x = self.inicioCuadricula+(self.tamanoCelda+self.interEspaciadoCelda)*j
                y = self.inicioCuadricula+(self.tamanoCelda+self.interEspaciadoCelda)*i

                #Dibuja la celda
                if (i == self.end[0] and j == self.end[1]):
                    pygame.draw.rect(DISPLAY, RED, pygame.Rect((x, y), (self.tamanoCelda, self.tamanoCelda)))
                elif (i == self.posicion[1] and j == self.posicion[0]):
                    pygame.draw.rect(DISPLAY, LIGHT_BLUE, pygame.Rect((x, y), (self.tamanoCelda, self.tamanoCelda)))
                else:
                    pygame.draw.rect(DISPLAY, WHITE, pygame.Rect((x, y), (self.tamanoCelda, self.tamanoCelda)))

                #Dibuja el numero correspondiente a cada cuadricula
                numero = str(self.matriz[i][j])
                superficieTexto = fuente.render(numero, True, BLACK)
                rectTexto = superficieTexto.get_rect(center=(x+self.tamanoCelda//2, y+self.tamanoCelda//2))
                DISPLAY.blit(superficieTexto, rectTexto)

                


class Juego:
    def __init__(self, laberintos):
        self.laberintos = laberintos
        self.labActual = 0
        self.estadoLaberintos = [False] * len(laberintos)
    
    def jugarLaberinto(self):
        self.laberintos[self.labActual].iniciarJuego()

    def draw(self):
        #Llama a la funcion draw del laberinto actual
        self.laberintos[self.labActual].draw()

def main():
    #Recibe un archivo con las descripciones de los laberintos
    file = open("archivoEntrada.txt", 'r')
    laberintos = []
    while(True):
        laberinto = file.readline()
        if (laberinto == ""):
            break
        laberinto = laberinto.split()
        filas = int(laberinto[0])
        columnas = int(laberinto[1])
        inicio = [int(laberinto[2]), int(laberinto[3])]
        final = (int(laberinto[4]), int(laberinto[5]))
        matriz = [[0 for _ in range(columnas)] for _ in range(filas)]
        #Se lee la matriz desde el archivo
        for i in range(filas):
            laberinto = file.readline()
            laberinto = laberinto.split()
            for j in range(columnas):
                matriz[i][j] = int(laberinto[j])
        
        laberintoI = Laberinto(matriz, inicio, final)
        laberintos.append(laberintoI)

    juego = Juego(laberintos)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.exit()
                sys.exit()
        
        juego.jugarLaberinto()

        pygame.display.update()
        FramesPerSecond.tick(FPS)





if __name__=="__main__":
    main()