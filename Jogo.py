# ***********************************************************************************
# ExibePoligonos.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa cria um conjunto de INSTANCIAS
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
# ***********************************************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Poligonos import *
from Instancia import *
from ModeloMatricial import *
from ListaDeCoresRGB import *
from Meteoros import *
from Tiro import *
from datetime import datetime
import time
import random
from os import system, name

# ***********************************************************************************

# Modelos de Objetos
MeiaSeta = Polygon()
Mastro = Polygon()

# Limites da Janela de Seleção
Min = Ponto()
Max = Ponto()

# lista de instancias do Personagens
Personagens = [Instancia() for x in range(500)]

AREA_DE_BACKUP = 50

Modelos = []
meteoros = []

angulo = 0.0
PersonagemAtual = -1
nInstancias = 0
imprimeEnvelope = False
LarguraDoUniverso = 250.0

TempoInicial = time.time()
TempoTotal = time.time()
TempoAnterior = time.time()

vidas = 3
tiros = []
max_tiros = 10
tiros_ativos = []
tiros_disparados = 0
tempo_de_recarga = 1.5
recarregando = False
pontos = 0

GAME_STATE_INICIO = 0
GAME_STATE_JOGANDO = 1
GAME_STATE_FIM = 2

game_state = GAME_STATE_INICIO


# ***********************************************************************************
def init():
    global Min, Max
    global TempoInicial, LarguraDoUniverso
    glClearColor(0, 0, 0, 1)

    clear()
    CarregaModelos()
    CriaInstancias()
    CriaMeteoros()

    LarguraDoUniverso = 150
    Min = Ponto(-LarguraDoUniverso, -LarguraDoUniverso)
    Max = Ponto(LarguraDoUniverso, LarguraDoUniverso)

    TempoInicial = time.time()
    print("Inicio: ", datetime.now())
    print("TempoInicial", TempoInicial)


def animate():
    global angulo, meteoros
    angulo += 1

    atualizar_meteoros()
    atualiza_tiros()
    rand = random.randint(0, 100)
    if rand <= 35:
        dispara_tiros_inimigos()

    glutPostRedisplay()


def atualizar_meteoros():
    global meteoros, LarguraDoUniverso
    for meteoro in meteoros:
        meteoro.posicao.x += meteoro.velocidade * meteoro.direcao.x
        meteoro.posicao.y += meteoro.velocidade * meteoro.direcao.y
        if abs(meteoro.posicao.x) > LarguraDoUniverso or abs(meteoro.posicao.y) > LarguraDoUniverso:
            meteoro.posicao = GeraPosicaoAleatoria()


# ***********************************************************************************
def reshape(w, h):

    global Min, Max
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    glOrtho(Min.x, Max.x, Min.y, Max.y, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def DesenhaTexto(string, x, y, tamanho=GLUT_BITMAP_TIMES_ROMAN_24):
    glRasterPos2f(x, y)
    for char in string:
        glutBitmapCharacter(tamanho, ord(char))


def display_start_screen():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glColor3f(0, 1, 0)

    DesenhaTexto("Asteroids Remake", -30, 80, GLUT_BITMAP_TIMES_ROMAN_24)
    DesenhaTexto("Pressione W para mover para frente",
                 -50, 40, GLUT_BITMAP_HELVETICA_18)
    DesenhaTexto("Pressione S para mover para trás",
                 -50, 30, GLUT_BITMAP_HELVETICA_18)
    DesenhaTexto("Pressione A para rotacionar para a esquerda",
                 -50, 20, GLUT_BITMAP_HELVETICA_18)
    DesenhaTexto("Pressione D para rotacionar para a direita",
                 -50, 10, GLUT_BITMAP_HELVETICA_18)
    DesenhaTexto("Pressione R para começar", -50, 0, GLUT_BITMAP_HELVETICA_18)
    DesenhaTexto("Pressione ESPAÇO para atirar",
                 -50, -10, GLUT_BITMAP_HELVETICA_18)

    DesenhaTexto("Objetivo: Fazer o máximo de pontos possíveis e não morrer para as naves inimigas",
                 -100, -50, GLUT_BITMAP_HELVETICA_18)
    DesenhaTexto("Caso queira a movimentação pelas setas do teclado também funcionam",
                 -100, -60, GLUT_BITMAP_HELVETICA_18)
    DesenhaTexto("Caso deseja enxergar a hitbox dos elementos pressione E",
                 -100, -70, GLUT_BITMAP_HELVETICA_18)
    glutSwapBuffers()


def display_game_over():
    global pontos

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glColor3f(1, 0, 0)

    DesenhaTexto(f"Game Over", -30, 40, GLUT_BITMAP_TIMES_ROMAN_24)
    DesenhaTexto(f"Pontos: {pontos}", -30, 20, GLUT_BITMAP_HELVETICA_18)
    DesenhaTexto(f"Pressione R para jogar novamente", -
                 30, 10, GLUT_BITMAP_HELVETICA_18)
    DesenhaTexto(f"Pressione ESC para sair", -30, 0, GLUT_BITMAP_HELVETICA_18)

    glutSwapBuffers()


def display():
    global TempoInicial, TempoTotal, TempoAnterior, pontos, game_state

    if game_state == GAME_STATE_INICIO:
        display_start_screen()
        return
    elif game_state == GAME_STATE_FIM:
        display_game_over()
        return

    TempoAtual = time.time()
    TempoTotal = TempoAtual - TempoInicial
    DiferencaDeTempo = TempoAtual - TempoAnterior

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glColor3f(1, 1, 1)
    DesenhaMeteoros()

    DesenhaPersonagens()
    AtualizaPersonagens(DiferencaDeTempo)
    DesenhaTiros()

    glColor3f(0, 1, 0)

    DesenhaTexto(f"Pontos: {pontos}", -10, 140)

    glutSwapBuffers()
    TempoAnterior = TempoAtual


# ***********************************************************************************
# The function called whenever a key is pressed.
# Note the use of Python tuples to pass in: (key, x, y)
# ESCAPE = '\033'
ESCAPE = b'\x1b'


def keyboard(*args):
    global imprimeEnvelope, tiros, max_tiros, Personagens, game_state
    key = args[0]

    if game_state == GAME_STATE_INICIO:
        if key == b'r':
            game_state = GAME_STATE_JOGANDO
        elif key == ESCAPE:
            os._exit(0)
        return
    elif game_state == GAME_STATE_FIM:
        if key == b'r':
            reiniciar_jogo()
        elif key == ESCAPE:
            os._exit(0)
    else:
        if key == b'w':
            Personagens[0].Posicao += Personagens[0].Direcao * 10
        if key == b's':
            Personagens[0].Posicao -= Personagens[0].Direcao * 10
        if key == b'a':
            Personagens[0].Rotacao += 10
            Personagens[0].Direcao.rotacionaZ(+10)
        if key == b'd':
            Personagens[0].Rotacao -= 10
            Personagens[0].Direcao.rotacionaZ(-10)
        if key == b' ':
            dispara_tiro_jogador()
            atualiza_tiros()

        if key == b'e':
            imprimeEnvelope = not imprimeEnvelope

        if key == ESCAPE:
            os._exit(0)
        glutPostRedisplay()


# **********************************************************************
#  arrow_keys ( a_keys: int, x: int, y: int )
# **********************************************************************
def arrow_keys(a_keys: int, x: int, y: int):
    if a_keys == GLUT_KEY_UP:         # Se pressionar UP
        Personagens[0].Posicao += Personagens[0].Direcao * 10
    if a_keys == GLUT_KEY_DOWN:       # Se pressionar DOWN
        Personagens[0].Posicao -= Personagens[0].Direcao * 10
        pass
    if a_keys == GLUT_KEY_LEFT:       # Se pressionar LEFT
        Personagens[0].Rotacao += 10
        Personagens[0].Direcao.rotacionaZ(+10)

    if a_keys == GLUT_KEY_RIGHT:      # Se pressionar RIGHT
        Personagens[0].Rotacao -= 10
        Personagens[0].Direcao.rotacionaZ(-10)

    glutPostRedisplay()

# ***********************************************************************************
#
# ***********************************************************************************


def mouse(button: int, state: int, x: int, y: int):
    global PontoClicado
    if (state != GLUT_DOWN):
        return
    if (button != GLUT_RIGHT_BUTTON):
        return
    # print ("Mouse:", x, ",", y)
    # Converte a coordenada de tela para o sistema de coordenadas do
    # Personagens definido pela glOrtho
    vport = glGetIntegerv(GL_VIEWPORT)
    mvmatrix = glGetDoublev(GL_MODELVIEW_MATRIX)
    projmatrix = glGetDoublev(GL_PROJECTION_MATRIX)
    realY = vport[3] - y
    worldCoordinate1 = gluUnProject(x, realY, 0, mvmatrix, projmatrix, vport)

    PontoClicado = Ponto(
        worldCoordinate1[0], worldCoordinate1[1], worldCoordinate1[2])
    PontoClicado.imprime("Ponto Clicado:")

    glutPostRedisplay()

# ***********************************************************************************


def mouseMove(x: int, y: int):
    # glutPostRedisplay()
    return


# define uma funcao de limpeza de tela
def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
        print("*******************")
        print("PWD: ", os.getcwd())


def reiniciar_jogo():
    global game_state, pontos, Personagens, TempoInicial, meteoros, vidas, tiros_disparados, recarregando, nInstancias

    game_state = GAME_STATE_JOGANDO
    pontos = 0
    vidas = 3
    tiros_disparados = 0
    recarregando = False

    Personagens = [Instancia() for x in range(500)]
    meteoros = []

    CriaInstancias()
    CriaMeteoros()

    TempoInicial = time.time()

    glutDisplayFunc(display)
    glutPostRedisplay()


def CriaMeteoros():
    for i in range(170):
        posicao = GeraPosicaoAleatoria()
        tamanho = random.uniform(0.1, 0.5)

        velocidade = random.uniform(0.01, 0.015)
        direcao = Ponto(random.uniform(-1, 1),
                        random.uniform(-1, 1))
        meteoros.append(Meteoro(posicao, tamanho, velocidade, direcao))


def DesenhaMeteoros():
    for meteoro in meteoros:
        glPushMatrix()
        glTranslate(meteoro.posicao.x, meteoro.posicao.y, 0)
        DesenhaMeteoro(meteoro.tamanho)
        glPopMatrix()


def DesenhaMeteoro(tamanho):
    glBegin(GL_QUADS)
    glVertex2f(-tamanho, -tamanho)
    glVertex2f(-tamanho, tamanho)
    glVertex2f(tamanho, tamanho)
    glVertex2f(tamanho, -tamanho)
    glEnd()


def DesenhaLinha(P1, P2):
    glBegin(GL_LINES)
    glVertex3f(P1.x, P1.y, P1.z)
    glVertex3f(P2.x, P2.y, P2.z)
    glEnd()

# ****************************************************************


def RotacionaAoRedorDeUmPonto(alfa: float, P: Ponto):
    glTranslatef(P.x, P.y, P.z)
    glRotatef(alfa, 0, 0, 1)
    glTranslatef(-P.x, -P.y, -P.z)


# **************************************************************
def DesenhaEixos():
    global Min, Max

    Meio = Ponto()
    Meio.x = (Max.x+Min.x)/2
    Meio.y = (Max.y+Min.y)/2
    Meio.z = (Max.z+Min.z)/2

    glBegin(GL_LINES)
    #  eixo horizontal
    glVertex2f(Min.x, Meio.y)
    glVertex2f(Max.x, Meio.y)
    #  eixo vertical
    glVertex2f(Meio.x, Min.y)
    glVertex2f(Meio.x, Max.y)
    glEnd()

# ***********************************************************************************


def TestaColisaoNaves():
    global Personagens, game_state, vidas, pontos
    abatido = False
    for inimigo in [p for p in Personagens if p.tipo == 'Inimigo' and p.ativo]:
        if TestaColisao(Personagens[0], inimigo):
            Personagens[0].ativo = True
            inimigo.ativo = False
            pontos += 10
            abatido = True
            if abatido:
                GeraNovosInimigos()
            return


def ColisaoTiroPersonagem(tiro, personagem):

    tiro_min_x = min(p.x for p in tiro.Envelope)
    tiro_max_x = max(p.x for p in tiro.Envelope)
    tiro_min_y = min(p.y for p in tiro.Envelope)
    tiro_max_y = max(p.y for p in tiro.Envelope)

    personagem_min_x = min(p.x for p in personagem.Envelope)
    personagem_max_x = max(p.x for p in personagem.Envelope)
    personagem_min_y = min(p.y for p in personagem.Envelope)
    personagem_max_y = max(p.y for p in personagem.Envelope)

    if (tiro_min_x < personagem_max_x and
        tiro_max_x > personagem_min_x and
        tiro_min_y < personagem_max_y and
            tiro_max_y > personagem_min_y):
        return True

    return False


def TestaColisaoTirosInimigos():
    global Personagens, pontos
    for tiro in [p for p in Personagens if p.tipo == 'TiroJogador' and p.ativo]:
        for inimigo in [p for p in Personagens if p.tipo == 'Inimigo' and p.ativo]:
            if ColisaoTiroPersonagem(tiro, inimigo):
                tiro.ativo = False
                inimigo.ativo = False
                pontos += 10
                print(
                    f"Inimigo {inimigo.IdDoModelo} destruído por tiro em {tiro.Posicao.x}, {tiro.Posicao.y}")
                GeraNovosInimigos()


def TestaColisaoTirosJogador():
    global Personagens, vidas, game_state

    for tiro in [p for p in Personagens if p.tipo == 'TiroInimigo' and p.ativo]:
        if Personagens[0].ativo and ColisaoTiroPersonagem(tiro, Personagens[0]):
            tiro.ativo = False
            vidas -= 1
            # Desativar um coração (vida) da tela
            vida_para_desativar = next(
                (p for p in Personagens if p.tipo == 'Vida' and p.ativo), None)
            if vida_para_desativar:
                vida_para_desativar.ativo = False

            if vidas <= 0:
                game_state = GAME_STATE_FIM
                glutDisplayFunc(display_game_over)
            return


def TestaColisao(P1, P2) -> bool:
    global Personagens
    # cout << "\n-----\n" << endl;
    # Personagens[Objeto1].ImprimeEnvelope("Envelope 1: ", "\n");
    # Personagens[Objeto2].ImprimeEnvelope("\nEnvelope 2: ", "\n");
    # cout << endl;
    # Testa todas as arestas do envelope de
    # um objeto contra as arestas do outro

    if P1.ativo and P2.ativo:
        for i in range(4):
            A = P1.Envelope[i]
            B = P1.Envelope[(i+1) % 4]
            for j in range(4):
                # print ("Testando ", i," contra ",j)
                # Personagens[Objeto1].ImprimeEnvelope("\nEnvelope 1: ", "\n");
                # Personagens[Objeto2].ImprimeEnvelope("Envelope 2: ", "\n");
                C = P2.Envelope[j]
                D = P2.Envelope[(j+1) % 4]
                # A.imprime("A:","\n");
                # B.imprime("B:","\n");
                # C.imprime("C:","\n");
                # D.imprime("D:","\n\n");
                if HaInterseccao(A, B, C, D):
                    return True
    return False


# ***********************************************************************************
def AtualizaEnvelope(i):
    global Personagens
    if Personagens[i].ativo:
        id = Personagens[i].IdDoModelo
        MM = Modelos[id]

        P = Personagens[i]
        V = P.Direcao * (MM.nColunas / 2.0)
        V.rotacionaZ(90)
        A = P.PosicaoDoPersonagem + V
        B = A + P.Direcao * MM.nLinhas

        V = P.Direcao * MM.nColunas
        V.rotacionaZ(-90)
        C = B + V

        V = P.Direcao * -1 * MM.nLinhas
        D = C + V

        if imprimeEnvelope:
            SetColor(Red)
            glBegin(GL_LINE_LOOP)
            glVertex2f(A.x, A.y)
            glVertex2f(B.x, B.y)
            glVertex2f(C.x, C.y)
            glVertex2f(D.x, D.y)
            glEnd()

            # A.imprime("A:")
            # B.imprime("B:")
            # C.imprime("C:")
            # D.imprime("D:")
            # print("")

        Personagens[i].Envelope[0] = A
        Personagens[i].Envelope[1] = B
        Personagens[i].Envelope[2] = C
        Personagens[i].Envelope[3] = D


# ***********************************************************************************
# Gera sempre uma posicao na metade de baixo da tela


def GeraPosicaoAleatoria():
    global LarguraDoUniverso
    x = random.randint(-LarguraDoUniverso, LarguraDoUniverso)
    y = random.randint(-LarguraDoUniverso, LarguraDoUniverso)
    return Ponto(x, y)


# ***********************************************************************************
def AtualizaJogo():
    global Personagens, nInstancias
    TestaColisaoTirosInimigos()
    TestaColisaoTirosJogador()
    TestaColisaoNaves()
    for i in range(0, nInstancias):
        if Personagens[i].ativo:
            AtualizaEnvelope(i)


def AtualizaPersonagens(tempoDecorrido):
    global nInstancias
    LarguraDoUniverso = 150
    jogador_atualizado = False

    for i in range(0, nInstancias):
        if Personagens[i].ativo:
            if i == 0:
                if not jogador_atualizado:
                    jogador_atualizado = True
                    Personagens[i].AtualizaPosicao(tempoDecorrido)

                    if Personagens[i].Posicao.x > LarguraDoUniverso:
                        Personagens[i].Posicao.x -= 2 * LarguraDoUniverso
                    elif Personagens[i].Posicao.x < -LarguraDoUniverso:
                        Personagens[i].Posicao.x += 2 * LarguraDoUniverso

                    if Personagens[i].Posicao.y > LarguraDoUniverso:
                        Personagens[i].Posicao.y -= 2 * LarguraDoUniverso
                    elif Personagens[i].Posicao.y < -LarguraDoUniverso:
                        Personagens[i].Posicao.y += 2 * LarguraDoUniverso

            else:
                Personagens[i].AtualizaPosicao(tempoDecorrido)

                if Personagens[i].Posicao.x > LarguraDoUniverso:
                    Personagens[i].Posicao.x -= 2 * LarguraDoUniverso
                elif Personagens[i].Posicao.x < -LarguraDoUniverso:
                    Personagens[i].Posicao.x += 2 * LarguraDoUniverso

                if Personagens[i].Posicao.y > LarguraDoUniverso:
                    Personagens[i].Posicao.y -= 2 * LarguraDoUniverso
                elif Personagens[i].Posicao.y < -LarguraDoUniverso:
                    Personagens[i].Posicao.y += 2 * LarguraDoUniverso

    AtualizaJogo()


# ***********************************************************************************
def DesenhaPersonagens():
    global PersonagemAtual, nInstancias
    existe = False
    for p in Personagens:
        if p.IdDoModelo == 0 and p.ativo == True:
            existe = True
            break

    for i in range(0, nInstancias):
        if Personagens[i].ativo:
            PersonagemAtual = i
            Personagens[i].Desenha()

        if Personagens[0].ativo and not existe:
            PersonagemAtual = 0
            Personagens[0].Desenha()


# ***********************************************************************************
def CarregaModelos():
    global Modelos
    Modelos.append(ModeloMatricial())
    Modelos[0].leModelo("MatrizNave.txt")
    Modelos.append(ModeloMatricial())
    Modelos[1].leModelo("NaveInimiga.txt")
    Modelos.append(ModeloMatricial())
    Modelos[2].leModelo("NaveInimiga1.txt")
    Modelos.append(ModeloMatricial())
    Modelos[3].leModelo("NaveInimiga2.txt")
    Modelos.append(ModeloMatricial())
    Modelos[4].leModelo("NaveInimiga3.txt")
    Modelos.append(ModeloMatricial())
    Modelos[5].leModelo("NaveInimiga.txt")
    Modelos.append(ModeloMatricial())
    Modelos[6].leModelo("NaveInimiga1.txt")
    Modelos.append(ModeloMatricial())
    Modelos[7].leModelo("NaveInimiga2.txt")
    Modelos.append(ModeloMatricial())
    Modelos[8].leModelo("NaveInimiga3.txt")
    Modelos.append(ModeloMatricial())
    Modelos[9].leModelo("Vida.txt")
    Modelos.append(ModeloMatricial())
    Modelos[10].leModelo("VidaPos.txt")
    Modelos.append(ModeloMatricial())
    Modelos[11].leModelo("Tiro.txt")
    Modelos.append(ModeloMatricial())
    Modelos[12].leModelo("TiroInimigo.txt")

    print("Modelo 0")
    Modelos[0].Imprime()
    print("Modelo 1")
    Modelos[1].Imprime()
    print("Modelo 2")
    Modelos[2].Imprime()
    print("Modelo 3")
    Modelos[3].Imprime()
    print("Modelo 4")
    Modelos[4].Imprime()
    print("Modelo 5")
    Modelos[5].Imprime()
    print("Modelo 6")
    Modelos[6].Imprime()
    print("Modelo 7")
    Modelos[7].Imprime()
    print("Modelo 8")
    Modelos[8].Imprime()
    print("Modelo 9")
    Modelos[9].Imprime()
    print("Modelo 10")
    Modelos[10].Imprime()
    print("Modelo 11")
    Modelos[11].Imprime()
    print("Modelo 12")
    Modelos[12].Imprime()


def DesenhaCelula():
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(0, 1)
    glVertex2f(1, 1)
    glVertex2f(1, 0)
    glEnd()
    pass


def DesenhaBorda():
    glBegin(GL_LINE_LOOP)
    glVertex2f(0, 0)
    glVertex2f(0, 1)
    glVertex2f(1, 1)
    glVertex2f(1, 0)
    glEnd()

# ***********************************************************************************


def DesenhaPersonagemMatricial():
    global PersonagemAtual, count

    MM = ModeloMatricial()

    ModeloDoPersonagem = Personagens[PersonagemAtual].IdDoModelo

    MM = Modelos[ModeloDoPersonagem]
    # MM.Imprime("Matriz:")

    glPushMatrix()
    larg = MM.nColunas
    alt = MM.nLinhas
    # print (alt, " LINHAS e ", larg, " COLUNAS")
    for i in range(alt):
        glPushMatrix()
        for j in range(larg):
            cor = MM.getColor(alt-1-i, j)
            if cor != -1:  # nao desenha celulas com -1 (transparentes)
                SetColor(cor)
                DesenhaCelula()
                # SetColor(Wheat)   # AS DUAS LINHAS COMENTADAS PARA QUE NAO DESENHE A BORDA DE CADA PIXEL DOS PERSONAGENS
                # DesenhaBorda()    #
            glTranslatef(1, 0, 0)
        glPopMatrix()
        glTranslatef(0, 1, 0)
    glPopMatrix()


# ***********************************************************************************
# Esta função deve instanciar todos os personagens do cenário
# ***********************************************************************************
def CriaInstancias():
    global Personagens, nInstancias

    # Jogador
    i = 0
    ang = 360.0
    modelo_nave = Modelos[0]
    centro_pivot_nave = Ponto(modelo_nave.nColunas / 2,
                              modelo_nave.nLinhas * 0.1)
    Personagens[i].Posicao = Ponto(-2.5, 0)
    Personagens[i].Escala = Ponto(1, 1)
    Personagens[i].Rotacao = ang
    Personagens[i].IdDoModelo = 0
    Personagens[i].Modelo = DesenhaPersonagemMatricial
    Personagens[i].Pivot = centro_pivot_nave
    Personagens[i].Direcao = Ponto(0, 1)
    Personagens[i].Direcao.rotacionaZ(ang)
    Personagens[i].Velocidade = 10
    Personagens[i].tipo = 'Jogador'
    Personagens[i].ativo = True
    # Personagens[i+AREA_DE_BACKUP] = copy.deepcopy(Personagens[i])  caso descomente ira duplicar o personagem ????????

    modelo_inimigo = Modelos[1]
    centro_pivot_nave_inimigo = Ponto(
        modelo_inimigo.nColunas / 2, modelo_inimigo.nLinhas * 0.02)
    # Nave Inimiga
    for j in range(1, 9):
        i += 1
        ang = random.randint(-180, 180)
        Personagens[i].tipo = 'Inimigo'
        Personagens[i].Posicao = GeraPosicaoAleatoria()
        Personagens[i].Escala = Ponto(1, 1)
        Personagens[i].Rotacao = ang
        Personagens[i].IdDoModelo = j
        Personagens[i].Modelo = DesenhaPersonagemMatricial
        Personagens[i].Pivot = centro_pivot_nave_inimigo
        Personagens[i].Direcao = Ponto(0, 1)
        Personagens[i].Direcao.rotacionaZ(ang)
        Personagens[i].Velocidade = 10
        Personagens[i].ativo = True
        Personagens[i+AREA_DE_BACKUP] = copy.deepcopy(Personagens[i])

    # Corações
    LarguraDoUniverso = 150
    x = LarguraDoUniverso - 18
    y = LarguraDoUniverso - 14
    for k in range(3):
        i += 1
        Personagens[i].Posicao = Ponto(x, y)
        Personagens[i].Escala = Ponto(0.9, 0.9)
        Personagens[i].Rotacao = 0
        Personagens[i].IdDoModelo = 9
        Personagens[i].Modelo = DesenhaPersonagemMatricial
        Personagens[i].Pivot = Ponto(0, 0)
        Personagens[i].Direcao = Ponto(0, 0)
        Personagens[i].Direcao.rotacionaZ(0)
        Personagens[i].Velocidade = 0
        Personagens[i].tipo = 'Vida'
        Personagens[i].ativo = True
        x -= 18

    modelo_tiro = Modelos[11]
    centro_pivot_tiro = Ponto(modelo_tiro.nColunas / 2,
                              modelo_tiro.nLinhas * 0.5)
    # Tiros do Jogador
    for k in range(max_tiros):
        i += 1
        Personagens[i] = Instancia()
        Personagens[i].ativo = False
        Personagens[i].Posicao = Ponto(0, 0)
        Personagens[i].Direcao = Ponto(0, 1)
        Personagens[i].Escala = Ponto(1, 1)
        Personagens[i].Pivot = centro_pivot_tiro
        Personagens[i].Rotacao = 0
        Personagens[i].IdDoModelo = 11
        Personagens[i].Modelo = DesenhaPersonagemMatricial
        Personagens[i].tipo = 'TiroJogador'
        Personagens[i].Velocidade = 5

    # Tiros Inimigos
    for k in range(max_tiros):
        i += 1
        Personagens[i] = Instancia()
        Personagens[i].ativo = False
        Personagens[i].Posicao = Ponto(0, 0)
        Personagens[i].Direcao = Ponto(0, -1)
        Personagens[i].Escala = Ponto(1, 1)
        Personagens[i].Pivot = centro_pivot_tiro
        Personagens[i].Rotacao = 0
        Personagens[i].IdDoModelo = 12
        Personagens[i].Modelo = DesenhaPersonagemMatricial
        Personagens[i].tipo = 'TiroInimigo'
        Personagens[i].Velocidade = 2.0
        Personagens.append(Personagens[i])

    nInstancias = len(Personagens)


def GeraNovosInimigos():
    global Personagens, Modelos

    modelo_inimiga = Modelos[1]
    centro_pivot_nave_inimiga = Ponto(
        modelo_inimiga.nColunas / 2, modelo_inimiga.nLinhas * 0.1)
    for i in range(1, 9):
        if not Personagens[i].ativo:
            ang = random.randint(-180, 180)
            Personagens[i].Posicao = GeraPosicaoAleatoria()
            Personagens[i].Escala = Ponto(1, 1)
            Personagens[i].Rotacao = ang
            Personagens[i].IdDoModelo = i
            Personagens[i].Modelo = DesenhaPersonagemMatricial
            Personagens[i].Pivot = centro_pivot_nave_inimiga
            Personagens[i].Direcao = Ponto(0, 1)
            Personagens[i].Direcao.rotacionaZ(ang)
            Personagens[i].Velocidade = 15
            Personagens[i].ativo = True
            Personagens[i+AREA_DE_BACKUP] = copy.deepcopy(Personagens[i])


def atualiza_tiros():
    global Personagens, LarguraDoUniverso
    for tiro in [p for p in Personagens if p.tipo.startswith('Tiro') and p.ativo]:
        tiro.Posicao += tiro.Direcao * tiro.Velocidade
        if abs(tiro.Posicao.x) > LarguraDoUniverso or abs(tiro.Posicao.y) > LarguraDoUniverso:
            tiro.ativo = False
            # print(f"Tiro desativado em {tiro.Posicao.x}, {tiro.Posicao.y}")


def dispara_tiro_jogador():
    global Personagens, tiros_disparados, recarregando, tempo_de_recarga

    if recarregando:
        tempo_atual = time.time()
        if tempo_atual - tempo_de_recarga >= 2:
            recarregando = False
            tiros_disparados = 0
        else:
            return

    jogador = Personagens[0]
    ponta_nave = Ponto(jogador.Envelope[1].x, jogador.Envelope[1].y)

    offset = Ponto(17.5, -15)
    offset.rotacionaZ(jogador.Rotacao)
    ponta_nave += offset

    if tiros_disparados < 10:
        tiro_disponivel = next(
            (t for t in Personagens if t.tipo == 'TiroJogador' and not t.ativo), None)
        if tiro_disponivel:
            tiro_disponivel.ativo = True
            tiro_disponivel.Posicao = Ponto(ponta_nave.x, ponta_nave.y)
            tiro_disponivel.Direcao = Ponto(
                jogador.Direcao.x, jogador.Direcao.y)
            tiro_disponivel.Velocidade = 8
            tiros_disparados += 1
            if tiros_disparados == 10:
                recarregando = True
                tempo_de_recarga = time.time()


def dispara_tiros_inimigos():
    global Personagens

    for inimigo in [p for p in Personagens if p.tipo == 'Inimigo' and p.ativo]:
        if random.random() < 0.05:
            tiro_disponivel = next(
                (t for t in Personagens if t.tipo == 'TiroInimigo' and not t.ativo), None)
            if tiro_disponivel:
                tiro_disponivel.ativo = True
                tiro_disponivel.Posicao = Ponto(
                    inimigo.Posicao.x, inimigo.Posicao.y)
                tiro_disponivel.Direcao = Ponto(
                    inimigo.Direcao.x, inimigo.Direcao.y)
                tiro_disponivel.Velocidade = 0.5
                # print(
                # f"Tiro disparado por inimigo em {inimigo.Posicao.x}, {inimigo.Posicao.y}")


def DesenhaTiros():
    for tiro in Personagens:
        if tiro.tipo == 'Tiro' and tiro.ativo:
            glPushMatrix()
            glTranslate(tiro.Posicao.x, tiro.Posicao.y, 0)
            tiro.Modelo()
            glPopMatrix()


# ***********************************************************************************
# Programa Principal
# ***********************************************************************************
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(100, 100)
wind = glutCreateWindow("Exemplo de Criacao de Instancias")
glutDisplayFunc(display)
glutIdleFunc(animate)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutSpecialFunc(arrow_keys)
glutMouseFunc(mouse)
init()

try:
    glutMainLoop()
except SystemExit:
    pass


# https://github.com/Bernardo-Zamin/T1-CG.git
