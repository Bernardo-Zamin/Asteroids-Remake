# ************************************************
#   ModeloMatricial.py
#   Define a classe ModeloMatricial
#   Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
# ************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Ponto import *

""" Classe ModeloMatricial """
class ModeloMatricial:   

    def __init__(self):
        self.Matriz = [] #[[0 for col in range(5)] for row in range(5)]
        # nro de linhas e colunas do modelo
        self.nLinhas = -1
        self.nColunas = -1
    
    def leModelo(self,nome):
        pass
    
    def getColor(self, i, j): # retorna a cor do modelo na celula [i][j]
        return self.Matriz[i][j]

    def Imprime(self, msg1=None): # imprime a matriz com as cores do modelo
        #print (self.Matriz)
        if msg1 is not None:
            print (msg1)
        for row in self.Matriz:
            print(row)

    # ***********************************************************************************
# LePontosDeArquivo(Nome):
#  Realiza a leitura de uam arquivo com as coordenadas do polígono
# ***********************************************************************************
    def leModelo(self, Nome):

        infile = open(Nome)
        line = infile.readline()
        words = line.split() # Separa as palavras na linha
        self.nLinhas = int(words[0])
        self.nColunas = int(words[1])

        # Loop pelas linhas restantes do arquivo
        for _ in range(self.nLinhas):
            # Leia a proxima linha do arquivo
            line = infile.readline()
            # Separa os valores na linha e converta para ponto flutuante
            row = [int(val) for val in line.split()]
            # Adicione a linha matriz
            self.Matriz.append(row)
        infile.close()


# M = ModeloMatricial()
# M.leModelo("MatrizExemplo0.txt")

# M.Imprime()
# print ("----")
# for i in range(M.nLinhas):
#     for j in range (M.nColunas):
#         print (M.getColor(i, j), end=" ")
#     print ("\n")