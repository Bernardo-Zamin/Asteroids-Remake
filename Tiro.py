from ModeloMatricial import *

class Tiro:
    def __init__(self, posicao, direcao, velocidade=0.2):
        self.posicao = posicao
        self.direcao = direcao
        self.ativo = True
        self.velocidade = velocidade
        self.id_modelo = 11  # Define o modelo de tiro, fixo como 11

    def move(self):
        """Move o tiro de acordo com sua direção e velocidade."""
        self.posicao.x += self.direcao.x * self.velocidade
        self.posicao.y += self.direcao.y * self.velocidade

    def get_modelo(self):
        """Retorna o modelo matricial associado ao tiro."""
        return carrega_modelo(self.id_modelo)  # Assumindo que existe uma função para carregar modelos

def carrega_modelo(id_modelo):
    """Função hipotética para carregar um modelo matricial com base em um ID."""
    # Aqui você adicionaria a lógica para carregar o modelo do tiro.
    # Este é apenas um exemplo.
    if id_modelo == 11:
        return ModeloMatricial()  # Retornaria o modelo real do tiro
    else:
        raise ValueError("Modelo não suportado para tiros")
