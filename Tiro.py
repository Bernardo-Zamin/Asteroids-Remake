from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class Tiro:
    def __init__(self, posicao, direcao):
        self.posicao = posicao
        self.direcao = direcao
        self.ativo = True

    def move(self):
        if self.ativo:
            self.posicao += self.direcao

    def desenha(self):
        if self.ativo:
            glPushMatrix()
            glTranslate(self.posicao.x, self.posicao.y, 0)
            DesenhaTiro()
            glPopMatrix()



def DesenhaTiro():
    glColor3f(1, 0, 0)  # Tiro vermelho para alta visibilidade
    glBegin(GL_QUADS)
    glVertex2f(-0.5, -0.5)  # Você pode ajustar o tamanho aqui conforme necessário
    glVertex2f(-0.5, 0.5)
    glVertex2f(0.5, 0.5)
    glVertex2f(0.5, -0.5)
    glEnd()
