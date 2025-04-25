import pygame, sys
from bot import BotDFS, BotCU
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
BEIGE = pygame.Color(255, 245, 200)
LIME_GREEN = pygame.Color(50, 205, 50)
VICTORY_OVAL = pygame.Color(255, 165, 100, 175)
GAME_COMPLETED_OVAL = pygame.Color(100, 255, 100, 175)
TOP_BAR = pygame.Color(100, 100, 100)
BOTON_CAMBLAB_HOLD = pygame.Color(200, 255, 200)
BOTON_CAMLAB = pygame.Color(100, 255, 100)
NOMBRE_JUEGO = pygame.Color(255, 215, 0)
BOTONES_MENU = pygame.Color(50, 205, 50)
BOTONES_MENU_HOLD = pygame.Color(100, 205, 100)

def esperar(tiempo_ms):
    tiempo_inicial = pygame.time.get_ticks()
    while pygame.time.get_ticks() - tiempo_inicial < tiempo_ms:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

class Boton:
    def __init__(self, pos, dim, accion, text, color = BOTON_CAMLAB, colorSeleccionado = BOTON_CAMBLAB_HOLD, colorTexto = BLACK):
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
        self.start = start
        self.matriz = matriz
        self.movimientos = 0
        self.completo = False
        self.nFilas = len(matriz)
        self.nColumnas = len(matriz[0])
        self.nLab = nLab
        self.menu = menu

        #variables para dibujar el laberinto
        self.window = None
        self.topBarHeight = 100
        self.tamanoCelda = max(80 - 10* (max(self.nFilas, self.nColumnas)//5), 20)
        self.interEspaciadoCelda = 5
        self.inicioCuadriculaX = 11
        self.inicioCuadriculaY = self.topBarHeight + 11
        self.windowHeight = self.inicioCuadriculaY - 1 + self.nFilas * (self.tamanoCelda + self.interEspaciadoCelda) + 5
        self.windowWidth = self.inicioCuadriculaX - 1 + self.nColumnas * (self.tamanoCelda + self.interEspaciadoCelda) + 5

        #botones
        self.botonAnterior = Boton((5*self.windowWidth//80, 5*self.topBarHeight//10), (5*self.windowWidth//20, 3*self.topBarHeight//10), self.menu.laberintoAnterior, "Anterior")
        self.botonSiguiente = Boton((55*self.windowWidth//80, 5*self.topBarHeight//10), (5*self.windowWidth//20, 3*self.topBarHeight//10), self.menu.laberintoSiguiente, "Siguiente")
        self.botonMenu = Boton((30*self.windowWidth//80, 5*self.topBarHeight//10), (5*self.windowWidth//20, 3*self.topBarHeight//10), self.menu.volverAMenu, "Menú")
        

        
    def iniciarLaberinto(self):
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    self.click(event.pos)
                    if (self.nLab != 1):
                        if self.botonAnterior.handle_event(event.pos):
                           return False
                    if (self.nLab != self.menu.numLaberintos):
                        if self.botonSiguiente.handle_event(event.pos):
                            return False
                    if self.botonMenu.handle_event(event.pos):
                        return False
                    

            self.verificarVictoria()
            self.draw()
            if(self.completo):
                self.menu.setMovLab(self.movimientos, self.nLab)
                self.menu.completarLaberinto(self.nLab)
                esperar(3000)
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
    
    def mostrarSolucionBot(self, solucion):
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        if solucion:
            for i in range(len(solucion)):
                self.posicion = solucion[i]
                self.draw()
                pygame.display.update()
                esperar(500)
            
            fuente = pygame.font.Font(None, max(35 - 3*(max(self.nFilas, self.nColumnas)//10), 15))
            tamOvalo = (200, 100)
            
            superficieOvalo = pygame.Surface(tamOvalo, pygame.SRCALPHA)
            pygame.draw.ellipse(superficieOvalo, VICTORY_OVAL, (0, 0, *tamOvalo))

            texto = fuente.render(f"{len(solucion) - 1} movimientos", True, BLACK)
            rectTexto = texto.get_rect(center=(tamOvalo[0]//2, tamOvalo[1]//2 - 10))
            superficieOvalo.blit(texto, rectTexto)
            texto = fuente.render("realizados", True, BLACK)
            rectTexto = texto.get_rect(center=(tamOvalo[0]//2, tamOvalo[1]//2 + 10))
            superficieOvalo.blit(texto, rectTexto)

            self.window.blit(superficieOvalo, ((self.windowWidth - tamOvalo[0])//2, (self.windowHeight - tamOvalo[1])//2))
            pygame.display.update()
            self.posicion = self.start
            esperar(2000)
            
        else:
            self.draw()
            fuente = pygame.font.Font(None, max(35 - 3*(max(self.nFilas, self.nColumnas)//10), 15))
            tamOvalo = (200, 100)
            
            superficieOvalo = pygame.Surface(tamOvalo, pygame.SRCALPHA)
            pygame.draw.ellipse(superficieOvalo, VICTORY_OVAL, (0, 0, *tamOvalo))

            texto = fuente.render("No hay solución", True, BLACK)
            rectTexto = texto.get_rect(center=(tamOvalo[0]//2, tamOvalo[1]//2))
            superficieOvalo.blit(texto, rectTexto)

            self.window.blit(superficieOvalo, ((self.windowWidth - tamOvalo[0])//2, (self.windowHeight - tamOvalo[1])//2))
            pygame.display.update()
            esperar(2000)

    def verificarVictoria(self):
        if(self.posicion[0] == self.end[0] and self.posicion[1] == self.end[1]):
            self.completo = True

    def draw(self):
        fuente = pygame.font.Font(None, max(35 - 3*(max(self.nFilas, self.nColumnas)//10), 15))
        self.window.fill(GREY)

        #Dibuja la barra superior
        pygame.draw.rect(self.window, TOP_BAR, pygame.Rect((0, 0), (self.windowWidth, self.topBarHeight)))

        texto = fuente.render(f"Laberinto {self.nLab}", True, BLACK)
        rectTexto = texto.get_rect(center=(self.windowWidth//2, self.topBarHeight//4))

        self.window.blit(texto, rectTexto)

        #Dibuja los botones
        if (self.nLab != 1):
            self.botonAnterior.draw(self.window)
        if (self.nLab != self.menu.numLaberintos):
            self.botonSiguiente.draw(self.window)
        self.botonMenu.draw(self.window)

        #Dibuja la cuadricula
        for i in range(self.nFilas):
            for j in range(self.nColumnas):
                x = self.inicioCuadriculaX+(self.tamanoCelda+self.interEspaciadoCelda)*j
                y = self.inicioCuadriculaY+(self.tamanoCelda+self.interEspaciadoCelda)*i

                #Dibuja la celda
                if (i == self.end[1] and j == self.end[0]):
                    if (self.posicion == self.end):
                        pygame.draw.rect(self.window, LIME_GREEN, pygame.Rect((x, y), (self.tamanoCelda, self.tamanoCelda)))
                    else:
                        pygame.draw.rect(self.window, RED, pygame.Rect((x, y), (self.tamanoCelda, self.tamanoCelda)))
                elif (i == self.posicion[1] and j == self.posicion[0]):
                    pygame.draw.rect(self.window, LIGHT_BLUE, pygame.Rect((x, y), (self.tamanoCelda, self.tamanoCelda)))
                else:
                    pygame.draw.rect(self.window, WHITE, pygame.Rect((x, y), (self.tamanoCelda, self.tamanoCelda)))
                
                #Dibuja el numero correspondiente a cada cuadricula
                numero = str(self.matriz[i][j])
                if numero == "0":
                    numero = "G"
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
        self.enMenu = True

        #Elementos de pygame
        self.window = None
        self.windowWidth = 600
        self.windowHeight = 400
        buttonWidth = self.windowWidth//6
        buttonHeight = buttonWidth//2

        #botones
        self.botonJugar = Boton((self.windowWidth//2-buttonWidth//2, 8*self.windowHeight//10), (buttonWidth,buttonHeight), self.jugarLaberinto, "Jugar", BOTONES_MENU, BOTONES_MENU_HOLD)
        self.botonBotDFS = Boton((self.windowWidth//8, 8*self.windowHeight//10), (buttonWidth, buttonHeight), self.ejecutarBotDFS, "Bot DFS", BOTONES_MENU, BOTONES_MENU_HOLD)
        self.botonBotCostoU = Boton((self.windowWidth - (buttonWidth + self.windowWidth//8), 8*self.windowHeight//10), (buttonWidth, buttonHeight), self.ejecutarBotCU, "Bot CU", BOTONES_MENU, BOTONES_MENU_HOLD)
        
    
    def jugarLaberinto(self):
        self.enMenu = False
        while not self.enMenu:
            for i in range(self.numLaberintos):
                if (not self.isLabCompleted[i]):
                    break
                if (i == self.numLaberintos - 1):
                    self.juegoCompletado()
                    pygame.time.wait(10000)
                    pygame.quit()
                    sys.exit()

            if(self.laberintos[self.labActual].iniciarLaberinto()):
                for i in range(self.labActual+1, self.labActual+self.numLaberintos):
                    if (not self.isLabCompleted[i%self.numLaberintos]):
                        self.labActual = i%self.numLaberintos
                        break
        
    def ejecutarBotDFS(self):
        botDFS = BotDFS()
        solucion = None
        soluciones = []
        for i in range(self.numLaberintos):
            laberinto = self.laberintos[i]
            if (i == 1):
                pass
            botDFS.seleccionarLaberinto(laberinto.matriz, laberinto.posicion)
            solucion = botDFS.resolverLaberinto()
            if solucion:
                soluciones.append(solucion)
            else:
                soluciones.append("No hay solución")

            laberinto.mostrarSolucionBot(solucion)
        
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.mostrarResultadosBot(soluciones)
    
    def ejecutarBotCU(self):
        botCU = BotCU()
        solucion = None
        soluciones = []
        for i in range(self.numLaberintos):
            laberinto = self.laberintos[i]
            if (i == 1):
                pass
            botCU.seleccionarLaberinto(laberinto.matriz, laberinto.posicion)
            solucion = botCU.resolverLaberinto()
            if solucion:
                soluciones.append(solucion)
            else:
                soluciones.append("No hay solución")

            laberinto.mostrarSolucionBot(solucion)
        
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        self.mostrarResultadosBot(soluciones)
    
    def mostrarResultadosBot(self, soluciones):
        #Setea una imagen de fondo
        fondo = pygame.image.load("imagenes\maze.jpg")
        fondo = pygame.transform.scale(fondo, (self.windowWidth, self.windowHeight))
        self.window.blit(fondo, (0, 0))

        fuenteResultados = pygame.font.Font(None, 25)
    
        for i, resultado in enumerate(soluciones):
            if (resultado == "No hay solución"):
                texto_sombra = fuenteResultados.render(f"Laberinto {i+1}: "+resultado, True, (0, 0, 0))
                texto = fuenteResultados.render(f"Laberinto {i+1}: "+resultado, True, BEIGE)
            else:
                texto_sombra = fuenteResultados.render(f"Laberinto {i+1}: Solución lograda con {len(resultado)-1} movimientos.", True, (0, 0, 0))
                texto = fuenteResultados.render(f"Laberinto {i+1}: Solución lograda con {len(resultado)-1} movimientos.", True, BEIGE)
            
            rectTexto = texto.get_rect(topleft=(self.windowWidth//10, 2*self.windowHeight//20 + 30*i))
            self.window.blit(texto_sombra, (rectTexto.topleft[0]+3, rectTexto.topleft[1]+3))
            self.window.blit(texto, rectTexto)
        
        pygame.display.flip()
        esperar(5000)

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
        self.window = pygame.display.set_mode((600,400))
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

    def iniciarMenu(self):
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.botonJugar.handle_event(event.pos)
                    self.botonBotCostoU.handle_event(event.pos)
                    self.botonBotDFS.handle_event(event.pos)

            self.dibujarMenu()

            pygame.display.update()
            FramesPerSecond.tick(FPS)

    def volverAMenu(self):
        self.enMenu = True
        self.window = pygame.display.set_mode((self.windowWidth, self.windowHeight))
        return True
        
    def dibujarMenu(self):
        fuenteTitulo = pygame.font.Font(None, 60)
        fuenteTituloInstrucciones = pygame.font.Font(None, 40)
        fuenteInstrucciones = pygame.font.Font(None, 25)

        #Setea una imagen de fondo
        fondo = pygame.image.load("imagenes\maze.jpg")
        fondo = pygame.transform.scale(fondo, (self.windowWidth, self.windowHeight))
        self.window.blit(fondo, (0, 0))

        #Titulo del juego
        texto = fuenteTitulo.render("Laberinto Saltarin", True, NOMBRE_JUEGO)
        rectTexto = texto.get_rect(center=(self.windowWidth//2, 1*self.windowHeight//10))
        self.window.blit(texto, rectTexto)

        #Instrucciones
        texto = fuenteTituloInstrucciones.render("Instrucciones", True, WHITE)
        rectTexto = texto.get_rect(center=(self.windowWidth//2, 2*self.windowHeight//10))
        self.window.blit(texto, rectTexto)

        instrucciones = "* Tu posición actual es la casilla azul.\n* Solo puedes moverte a casillas que esten a una distancia\n  igual al número de tu casilla actual.\n* Solo se permiten movimientos horizontales o verticales.\n* Tu objetivo es llegar a la casilla roja en el menor número\n  de movimientos.\n* Ganas al resolver todos los laberintos."
        instrucciones = instrucciones.splitlines()
        for i, line in enumerate(instrucciones):
            texto_sombra = fuenteInstrucciones.render(line, True, (0, 0, 0))
            texto = fuenteInstrucciones.render(line, True, BEIGE)
            rectTexto = texto.get_rect(topleft=(self.windowWidth//10, 5*self.windowHeight//20 + 30*i))
            self.window.blit(texto_sombra, (rectTexto.topleft[0]+3, rectTexto.topleft[1]+3))
            self.window.blit(texto, rectTexto)
            
        
        #Dibujar boton jugar
        self.botonJugar.draw(self.window)
        self.botonBotCostoU.draw(self.window)
        self.botonBotDFS.draw(self.window)

def cargarLaberintos(ruta):
    #Recibe un archivo con las descripciones de los laberintos
    file = open(ruta, 'r')
    laberintos = []
    n = 0
    menu = MenuPrincipal()

    while(True):
        laberinto = file.readline()
        if (laberinto == "0"):
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
    
    return menu

def main():
    ruta = "archivoEntrada.txt"
    menu = cargarLaberintos(ruta)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        menu.iniciarMenu()

        pygame.display.update()
        FramesPerSecond.tick(FPS)





if __name__=="__main__":
    main()