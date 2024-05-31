from ModeloMatricial import *

class Tiro:
    def __init__(self, posicao, direcao, velocidade=0.2):
        self.posicao = posicao
        self.direcao = direcao
        self.ativo = True
        self.velocidade = velocidade
        self.id_modelo = 11

    def move(self):
        self.posicao.x += self.direcao.x * self.velocidade
        self.posicao.y += self.direcao.y * self.velocidade

    def get_modelo(self):
        return carrega_modelo(self.id_modelo)

def carrega_modelo(id_modelo):
    if id_modelo == 11:
        return ModeloMatricial() 
    else:
        raise ValueError("Modelo não suportado para tiros")
