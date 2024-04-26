# ************************************************
#   Poligonos.py
#   Define a classe Polygon
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import *
import copy

class Polygon:

    def __init__(self):
        self.Vertices = [] # atributo do objeto

    def getNVertices(self):
        return len(self.Vertices)
    
    def insereVertice(self, x: float, y:float, z: float):
        self.Vertices += [Ponto(x,y,z)]

    #def insereVertice(self, P: Ponto):
    #    self.Vertices += [Ponto(P.x,P.y,P.z)]

    def getVertice(self, i):
        temp = copy.deepcopy(self.Vertices[i])
        return temp
        #return self.Vertices[i]
    
    def desenhaPoligono(self):
        #print ("Desenha Poligono - Tamanho:", len(self.Vertices))
        glBegin(GL_LINE_LOOP)
        for V in self.Vertices:
            glVertex3f(V.x,V.y,V.z)
        glEnd();

    def desenhaVertices(self):
        glBegin(GL_POINTS);
        for V in self.Vertices:
            glVertex3f(V.x,V.y,V.z)
        glEnd();

    def imprimeVertices(self):
        for x in self.Vertices:
            x.imprime()

    def getLimits(self):
        Min = copy.deepcopy(self.Vertices[0])
        Max = copy.deepcopy(self.Vertices[0])
        
        for V in self.Vertices:
            if V.x > Max.x:
                Max.x = V.x
            if V.y > Max.y:
                Max.y = V.y
            if V.z > Max.z:
                Max.z = V.z
            if V.x < Min.x:
                Min.x = V.x
            if V.y < Min.y:
                Min.y = V.y
            if V.z < Min.z:
                Min.z = V.z
        #print("getLimits")
        #Min.imprime()
        #Max.imprime()
        return Min, Max
#def setColor()
# ***********************************************************************************
# LePontosDeArquivo(Nome):
#  Realiza a leitura de uam arquivo com as coordenadas do polígono
# ***********************************************************************************
    def LePontosDeArquivo(self, Nome):
        
        Pt = Ponto()
        infile = open(Nome)
        line = infile.readline()
        number = int(line)
        for line in infile:
            words = line.split() # Separa as palavras na linha
            x = float (words[0])
            y = float (words[1])
            self.insereVertice(x,y,0)
            #Mapa.insereVertice(*map(float,line.split))
        infile.close()
        
        #print ("Após leitura do arquivo:")
        #Min.imprime()
        #Max.imprime()
        return self.getLimits()

    def getAresta(self, n):
        P1 = self.Vertices[n]
        n1 = (n+1) % self.getNVertices()
        P2 = self.Vertices[n1]
        return P1, P2

    def desenhaAresta(self, n):
        glBegin(GL_LINES)
        glVertex3f(self.Vertices[n].x,self.Vertices[n].y,self.Vertices[n].z)
        n1 = (n+1) % self.getNVertices()
        glVertex3f(self.Vertices[n1].x,self.Vertices[n1].y,self.Vertices[n1].z)
        glEnd()

    def alteraVertice(self, i, P):
    #int i, Ponto P)
        self.Vertices[i] = P

