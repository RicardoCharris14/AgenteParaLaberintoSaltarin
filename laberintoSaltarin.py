import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 60
FramesPerSecond = pygame.time.Clock()

#colores
GREY = pygame.Color(150, 150, 150)
WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
LIGHT_BLUE = pygame.Color(50, 50, 255)
VICTORY_OVAL = pygame.Color(255, 165, 100, 175)
GAME_COMPLETED_OVAL = pygame.Color(100, 255, 100, 175)
TOP_BAR = pygame.Color(100, 100, 100)
BOTON_SELECCIONADO = pygame.Color(200, 255, 200)
BOTON = pygame.Color(100, 255, 100)


class Boton:
    def __init__(self, pos, dim, accion, text, color = BOTON, colorSeleccionado = BOTON_SELECCIONADO, colorTexto = BLACK):
        self.rectangulo = pygame.Rect(pos[0], pos[1], dim[0], dim[1])
        self.font = pygame.font.Font(None, 24)
        self.text = text
        self.accion = accion
        self.color = color
        self.colorSeleccionado = colorSeleccionado
        self.colorTexto = colorTexto
    
    def draw(self, superficie):
        mouse = pygame.mouse.get_pos()
        color = self.colorSeleccionado if (self.rectangulo.collidepoint(mouse)) else self.color 
        pygame.draw.rect(superficie, color, self.rectangulo)

        texto = self.font.render(self.text, True, self.colorTexto)
        rectTexto = texto.get_rect(center=(self.rectangulo.center))
        superficie.blit(texto, rectTexto)

    def handle_event(self, posicionClick):
        if (self.rectangulo.collidepoint(posicionClick)):
            return self.accion()

class Laberinto:
    def __init__(self, menu, matriz, start, end, nLab = 0):
        #variables inherentes al laberinto
        self.end = end
        self.posicion = start
        self.matriz = matriz
        self.movimientos = 0
        self.completo = False
        self.nFilas = len(matriz)
        self.nColumnas = len(matriz[0])
        self.nLab = nLab
        self.menu = menu

        #variables para dibujar el laberinto
        self.window = None
        self.topBarHeight = 50
        self.tamanoCelda = 60
        self.interEspaciadoCelda = 5
        self.inicioCuadriculaX = 11
        self.inicioCuadriculaY = self.topBarHeight + 11
        self.windowHeight = self.inicioCuadriculaY - 1 + self.nFilas * (self.tamanoCelda + self.interEspaciadoCelda) + 5
        self.windowWidth = self.inicioCuadriculaX - 1 + self.nColumnas * (self.tamanoCelda + self.interEspaciadoCelda) + 5

        #botones
        self.botonAnterior = Boton((self.windowWidth//20, self.topBarHeight//5), (5*self.windowWidth//20, 3*self.topBarHeight//5), self.menu.laberintoAnterior, "Anterior")
        self.botonSiguiente = Boton((14*self.windowWidth//20, self.topBarHeight//5), (5*self.windowWidth//20, 3*self.topBarHeight//5), self.menu.laberintoSiguiente, "Siguiente")
        self.botones = [self.botonAnterior, self.botonSiguiente]

        
    def iniciarLaberinto(self):
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.exit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.click(event.pos)
                    for boton in self.botones:
                        if(boton.handle_event(event.pos)):
                            return False

            self.verificarVictoria()
            self.draw()
            if(self.completo):
                self.menu.setMovLab(self.movimientos, self.nLab)
                self.menu.completarLaberinto(self.nLab)
                pygame.time.wait(3000)
                return True

            pygame.display.update()
            FramesPerSecond.tick(60)
    
    def click(self, pos):
        distanciaMov = self.matriz[self.posicion[1]][self.posicion[0]]

        # Se verifica que el click sea dentro de una casilla y que la casilla este a una distancia de la casilla actual igual al numero de la casilla actual, en tal caso se realiza el movimiento
        x = (pos[0]-self.inicioCuadriculaX)//(self.tamanoCelda+self.interEspaciadoCelda)
        y = (pos[1]-self.inicioCuadriculaY)//(self.tamanoCelda+self.interEspaciadoCelda)
        if ((x - (pos[0]-(self.tamanoCelda+self.inicioCuadriculaX))//(self.tamanoCelda+self.interEspaciadoCelda)) != 0 and (y - (pos[1]-(self.tamanoCelda+self.inicioCuadriculaY))//(self.tamanoCelda+self.interEspaciadoCelda)) != 0):
            if ((abs(self.posicion[0] - x) == distanciaMov and self.posicion[1] == y) or (abs(self.posicion[1] - y) == distanciaMov and self.posicion[0] == x)):
                if((0 <= x < len(self.matriz[0])) and (0 <= y < len(self.matriz))):
                    self.posicion[0] = x
                    self.posicion[1] = y
                    self.movimientos+=1

    def verificarVictoria(self):
        if(self.posicion[0] == self.end[0] and self.posicion[1] == self.end[1]):
            self.completo = True

    def draw(self):
        fuente = pygame.font.Font(None, 24)
        self.window.fill(GREY)

        #Dibuja la barra superior
        pygame.draw.rect(self.window, TOP_BAR, pygame.Rect((0, 0), (self.windowWidth, self.topBarHeight)))

        texto = fuente.render(f"Laberinto {self.nLab}", True, BLACK)
        rectTexto = texto.get_rect(center=(self.windowWidth//2, self.topBarHeight//2))

        self.window.blit(texto, rectTexto)

        #Dibuja los botones
        if (self.nLab != 1):
            self.botonAnterior.draw(self.window)
        if (self.nLab != self.menu.numLaberintos):
            self.botonSiguiente.draw(self.window)

        #Dibuja la cuadricula
        for i in range(self.nFilas):
            for j in range(self.nColumnas):
                x = self.inicioCuadriculaX+(self.tamanoCelda+self.interEspaciadoCelda)*j
                y = self.inicioCuadriculaY+(self.tamanoCelda+self.interEspaciadoCelda)*i

                #Dibuja la celda
                if (i == self.end[1] and j == self.end[0]):
                    pygame.draw.rect(self.window, RED, pygame.Rect((x, y), (self.tamanoCelda, self.tamanoCelda)))
                elif (i == self.posicion[1] and j == self.posicion[0]):
                    pygame.draw.rect(self.window, LIGHT_BLUE, pygame.Rect((x, y), (self.tamanoCelda, self.tamanoCelda)))
                else:
                    pygame.draw.rect(self.window, WHITE, pygame.Rect((x, y), (self.tamanoCelda, self.tamanoCelda)))

                #Dibuja el numero correspondiente a cada cuadricula
                numero = str(self.matriz[i][j])
                texto = fuente.render(numero, True, BLACK)
                rectTexto = texto.get_rect(center=(x+self.tamanoCelda//2, y+self.tamanoCelda//2))
                self.window.blit(texto, rectTexto)
        
        #Notifica que el nivel fue completado
        if(self.completo):
            tamOvalo = (200, 100)
            #crea una superficie con transparencia
            superficieOvalo = pygame.Surface(tamOvalo, pygame.SRCALPHA)

            #Dibuja el ovalo en la superficie
            pygame.draw.ellipse(superficieOvalo, VICTORY_OVAL, (0, 0, *tamOvalo))

            #renderiza el texto
            texto = fuente.render("¡Nivel completado!", True, BLACK)
            rectTexto = texto.get_rect(center=(tamOvalo[0]//2, tamOvalo[1]//2))
            
            #dibuja el texto en el ovalo
            superficieOvalo.blit(texto, rectTexto)

            #dibuja ovalo en la pantalla principal
            self.window.blit(superficieOvalo, ((self.windowWidth - tamOvalo[0])//2, (self.windowHeight - tamOvalo[1])//2))
            pygame.display.update()


class MenuPrincipal:
    def __init__(self, laberintos = []):
        self.laberintos = laberintos
        self.numLaberintos = len(laberintos)
        self.labActual = 0
        self.movimientosPorLaberinto = [0] * self.numLaberintos
        self.isLabCompleted = [False] * self.numLaberintos

        #Elementos de pygame
        self.window = None
        self.windowWidth = 600
        self.windowHeight = 400
        
    
    def jugarLaberinto(self):
        for i in range(self.numLaberintos):
            if (not self.isLabCompleted[i]):
                break
            if (i == self.numLaberintos - 1):
                self.juegoCompletado()
                pygame.time.wait(8000)
                return True

        if(self.laberintos[self.labActual].iniciarLaberinto()):
            for i in range(self.labActual+1, self.labActual+self.numLaberintos):
                if (not self.isLabCompleted[i%self.numLaberintos]):
                    self.labActual = i%self.numLaberintos
            

    def addLaberinto(self, laberinto):
        self.laberintos.append(laberinto)
        self.numLaberintos+=1
        self.movimientosPorLaberinto.append(0)
        self.isLabCompleted.append(False)
    
    def setMovLab(self, nMov, nLab):
        self.movimientosPorLaberinto[nLab-1] = nMov

    def completarLaberinto(self, nLab):
        self.isLabCompleted[nLab-1] = True
    
    def laberintoAnterior(self):
        if (self.labActual - 1 >= 0):
            self.labActual-=1
            return True
        return False
    
    def laberintoSiguiente(self):
        if (self.labActual + 1 < self.numLaberintos):
            self.labActual+=1
            return True
        return False

    def juegoCompletado(self):
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        fuente = pygame.font.Font(None, 24)

        #Setea una imagen de fondo
        fondo = pygame.image.load("imagenes\maze.jpg")
        fondo = pygame.transform.scale(fondo, (self.windowWidth, self.windowHeight))
        self.window.blit(fondo, (0, 0))

        #Dibuja el mensaje de felicitaciones
        tamOvalo = (330, 150)
        superficieOvalo = pygame.Surface(tamOvalo, pygame.SRCALPHA)

        pygame.draw.ellipse(superficieOvalo, VICTORY_OVAL, (0, 0, *tamOvalo))

        texto = "¡Felicitaciones!\n¡Has completado todos los laberintos!"
        lineas = texto.splitlines()
        for idx, linea in enumerate(lineas):
            texto_renderizado = fuente.render(linea, True, BLACK)
            rectTexto = texto_renderizado.get_rect(center=(tamOvalo[0] // 2, 45 + idx * 30))  # Ajusta la posición vertical
            superficieOvalo.blit(texto_renderizado, rectTexto)

        self.window.blit(superficieOvalo, ((self.windowWidth - tamOvalo[0])//2, (self.windowHeight - tamOvalo[1])//2))

        pygame.display.update()

    def draw(self):
        pass


def main():
    #Recibe un archivo con las descripciones de los laberintos
    file = open("archivoEntrada.txt", 'r')
    laberintos = []
    n = 0
    menu = MenuPrincipal()

    while(True):
        laberinto = file.readline()
        if (laberinto == ""):
            break
        laberinto = laberinto.split()
        filas = int(laberinto[0])
        columnas = int(laberinto[1])
        inicio = [int(laberinto[3]), int(laberinto[2])]
        final = (int(laberinto[5]), int(laberinto[4]))
        matriz = [[0 for _ in range(columnas)] for _ in range(filas)]
        #Se lee la matriz desde el archivo
        for i in range(filas):
            laberinto = file.readline()
            laberinto = laberinto.split()
            for j in range(columnas):
                matriz[i][j] = int(laberinto[j])

        n+=1
        menu.addLaberinto(Laberinto(menu, matriz, inicio, final, n))


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.exit()
                sys.exit()
        
        if(menu.jugarLaberinto()):
            pygame.exit()
            sys.exit()

        pygame.display.update()
        FramesPerSecond.tick(FPS)





if __name__=="__main__":
    main()