# ************************************************
#   Instancia.py
#   Define a classe Instancia
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import *

#import numpy as np


""" Classe Instancia """
class Instancia:   
    def __init__(self):
        
        self.Posicao = Ponto (0,0,0) 
        self.Escala = Ponto (1,1,1)
        self.Rotacao:float = 0.0
        self.Modelo = None
        self.t = 0.0

        self.IdDoModelo = 0;
        self.Pivot = Ponto (0,0,0) 
        self.Velocidade:float = 0.0
        self.Envelope = []
        self.Direcao = Ponto(0,0,0)
        self.PosicaoDoPersonagem = Ponto(0,0,0)
        for i in range(4):
            self.Envelope += [Ponto()]
        

    """ Imprime os valores dos atributos da instancia """
    # Faz a impressao usando sobrecarga de funcao
    # https://www.educative.io/edpresso/what-is-method-overloading-in-python
    def imprime(self, msg=None):
        if msg is not None:
            pass 
        else:
            print ("Rotacao:", self.rotacao)

    """ Define o modelo a ser usada para a desenhar """
    def setModelo(self, func):
        self.modelo = func

    def setOrientacao(self, ang):
        self.Rotacao = ang

    def Desenha(self):

        if self.Modelo is None:
            #print ("Modelo invalido")
            return

        # Aplica as transformacoes geometricas no modelo
        glPushMatrix()
        glTranslatef(self.Posicao.x, self.Posicao.y, self.Posicao.z)
        glTranslatef(self.Pivot.x, self.Pivot.y, 0)
        glRotatef(self.Rotacao, 0, 0, 1)
        glScalef(self.Escala.x, self.Escala.y, self.Escala.z)
        glTranslatef(-self.Pivot.x, -self.Pivot.y, self.Pivot.z)

        # Obtem a posicao do ponto 0,0,0 no SRU
        # Nao eh usado aqui, mas eh util para detectar colisoes
        # self.PosicaoDoPersonagem = self.InstanciaPonto(Ponto(0,0,0)+self.Pivot);
        self.PosicaoDoPersonagem = self.InstanciaPonto(self.Pivot)

        self.Modelo()
        glPopMatrix()
        

        # self.Modelo() # Desenha a instancia
        # glPopMatrix()

    def ImprimeEnvelope(self, msg1=None, msg2=None):
        if msg1 is not None:
            print (msg1, end="")
        self.Envelope[0].imprime()
        self.Envelope[1].imprime()
        self.Envelope[2].imprime()
        self.Envelope[3].imprime()
        if msg2 is not None:
            print (msg2)
        print (flush=True)

    def InstanciaPonto (self, P:Ponto):
        matriz_gl = glGetFloatv(GL_MODELVIEW_MATRIX)
        
        ponto_novo = []
        for i in range(4):
            ponto_novo.append(
                                matriz_gl[0][i] * P.x +
                                matriz_gl[1][i] * P.y +
                                matriz_gl[2][i] * P.z +
                                matriz_gl[3][i]
                            )
        temp = Ponto(ponto_novo[0],ponto_novo[1],ponto_novo[2])
        return temp

    def AtualizaPosicao(self, tempoDecorrido):
        self.Posicao = self.Posicao + self.Direcao*tempoDecorrido*self.Velocidade