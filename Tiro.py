class Tiro:
    def __init__(self, posicao, direcao):
        self.posicao = posicao
        self.direcao = direcao
        self.ativo = True

    def move(self):
        self.posicao.x += self.direcao.x * 0.2  # Velocidade do tiro
        self.posicao.y += self.direcao.y * 0.2