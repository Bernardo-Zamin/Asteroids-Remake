# ***********************************************************************************
#   ExibePoligonos.py
#       Autor: Márcio Sarroglia Pinho
#       pinho@pucrs.br
#   Este programa cria um conjunto de INSTANCIAS
#   Para construir este programa, foi utilizada a biblioteca PyOpenGL, disponível em
#   http://pyopengl.sourceforge.net/documentation/index.html
#
#   Sugere-se consultar também as páginas listadas
#   a seguir:
#   http://bazaar.launchpad.net/~mcfletch/pyopengl-demo/trunk/view/head:/PyOpenGL-Demo/NeHe/lesson1.py
#   http://pyopengl.sourceforge.net/documentation/manual-3.0/index.html#GLUT
#
#   No caso de usar no MacOS, pode ser necessário alterar o arquivo ctypesloader.py,
#   conforme a descrição que está nestes links:
#   https://stackoverflow.com/questions/63475461/unable-to-import-opengl-gl-in-python-on-macos
#   https://stackoverflow.com/questions/6819661/python-location-on-mac-osx
#   Veja o arquivo Patch.rtf, armazenado na mesma pasta deste fonte.
# ***********************************************************************************

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Poligonos import *
from Instancia import *
from ModeloMatricial import *
from ListaDeCoresRGB import *
from Meteoros import *
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

AREA_DE_BACKUP = 50  # posicao a partir da qual sao armazenados backups dos personagens

# lista de modelos
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

# tempo_para_mudar_direcao = 2.0  # tempo em segundos para mudar de direção
# tempo_desde_ultima_mudanca = 0.0

# ***********************************************************************************


def init():
    global Min, Max
    global TempoInicial, LarguraDoUniverso
    # Define a cor do fundo da tela (AZUL)
    glClearColor(0, 0, 0, 1)

    clear()  # limpa o console
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
    angulo = angulo + 1

    # Atualiza a posição dos meteoros
    for meteoro in meteoros:
        meteoro.posicao.x += meteoro.velocidade * meteoro.direcao.x
        meteoro.posicao.y += meteoro.velocidade * meteoro.direcao.y
        
        # Se o meteoro sair da tela, reinicialize sua posição
        if meteoro.posicao.x > LarguraDoUniverso or meteoro.posicao.x < -LarguraDoUniverso:
            meteoro.posicao.x = GeraPosicaoAleatoria().x
        if meteoro.posicao.y > LarguraDoUniverso or meteoro.posicao.y < -LarguraDoUniverso:
            meteoro.posicao.y = GeraPosicaoAleatoria().y

    glutPostRedisplay()



# ***********************************************************************************
def reshape(w, h):

    global Min, Max
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # Cria uma folga na Janela de Selecão, com 10% das dimensoes do poligono
    BordaX = abs(Max.x-Min.x)*0.1
    BordaY = abs(Max.y-Min.y)*0.1
    # glOrtho(Min.x-BordaX, Max.x+BordaX, Min.y-BordaY, Max.y+BordaY, 0.0, 1.0)
    glOrtho(Min.x, Max.x, Min.y, Max.y, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# ***********************************************************************************


def display():

    global TempoInicial, TempoTotal, TempoAnterior

    TempoAtual = time.time()

    TempoTotal = TempoAtual - TempoInicial

    DiferencaDeTempo = TempoAtual - TempoAnterior

    # Limpa a tela coma cor de fundo
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glColor3f(1, 1, 1)
    DesenhaMeteoros()

    DesenhaPersonagens()
    AtualizaPersonagens(DiferencaDeTempo)


    glutSwapBuffers()
    TempoAnterior = TempoAtual


# ***********************************************************************************
# The function called whenever a key is pressed.
# Note the use of Python tuples to pass in: (key, x, y)
# ESCAPE = '\033'
ESCAPE = b'\x1b'


def keyboard(*args):
    global imprimeEnvelope
    key = args[0]
    #print(key)

    # Configurações para as teclas WASD
    if key == b'w':  # W - Move para frente
        Personagens[0].Posicao += Personagens[0].Direcao * 10
    elif key == b's':  # S - Move para trás
        Personagens[0].Posicao -= Personagens[0].Direcao * 10
    elif key == b'a':  # A - Rotaciona para esquerda
        Personagens[0].Rotacao += 10
        Personagens[0].Direcao.rotacionaZ(+10)
    elif key == b'd':  # D - Rotaciona para direita
        Personagens[0].Rotacao -= 5
        Personagens[0].Direcao.rotacionaZ(-10)

    # Para alternar o estado de visualização do envelope de colisão
    if key == b'e':
        imprimeEnvelope = not imprimeEnvelope

    # Comandos adicionais, como antes
    if key == b'q' or key == ESCAPE:
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



def CriaMeteoros():
    for i in range(170):  # Cria 170x11 meteoros
        posicao = GeraPosicaoAleatoria()
        tamanho = random.uniform(0.1, 0.5)  # Tamanho aleatório para cada meteoro
        velocidade = random.uniform(0.01, 0.015)  # Velocidade muito pequena para movimento sutil
        direcao = Ponto(random.uniform(-1, 1), random.uniform(-1, 1))  # Direção aleatória
        meteoros.append(Meteoro(posicao, tamanho, velocidade, direcao))


def DesenhaMeteoros():
    for meteoro in meteoros:
        glPushMatrix()
        glTranslate(meteoro.posicao.x, meteoro.posicao.y, 0)  # Posiciona o meteoro
        DesenhaMeteoro(meteoro.tamanho)  # Desenha o meteoro
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


def TestaColisao(P1, P2) -> bool:

    # cout << "\n-----\n" << endl;
    # Personagens[Objeto1].ImprimeEnvelope("Envelope 1: ", "\n");
    # Personagens[Objeto2].ImprimeEnvelope("\nEnvelope 2: ", "\n");
    # cout << endl;

    # Testa todas as arestas do envelope de
    # um objeto contra as arestas do outro
    for i in range(4):
        A = Personagens[P1].Envelope[i]
        B = Personagens[P1].Envelope[(i+1) % 4]
        for j in range(4):
            # print ("Testando ", i," contra ",j)
            # Personagens[Objeto1].ImprimeEnvelope("\nEnvelope 1: ", "\n");
            # Personagens[Objeto2].ImprimeEnvelope("Envelope 2: ", "\n");
            C = Personagens[P2].Envelope[j]
            D = Personagens[P2].Envelope[(j+1) % 4]
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
    id = Personagens[i].IdDoModelo
    MM = Modelos[id]

    P = Personagens[i]
    V = P.Direcao * (MM.nColunas/2.0)
    V.rotacionaZ(90)
    A = P.PosicaoDoPersonagem + V
    B = A + P.Direcao*MM.nLinhas

    V = P.Direcao * MM.nColunas
    V.rotacionaZ(-90)
    C = B + V

    V = P.Direcao * -1 * MM.nLinhas
    D = C + V

    # Desenha o envelope
    # !!!!!!!!!!!!!!!!!!!!!!!!!!! Comentei aqui para que o envelope(hitbox) não seja desenhado !!!!!!!!!!!!!!!!!!!!!!!!!!!
    # SetColor(Red)
    # glBegin(GL_LINE_LOOP)
    # glVertex2f(A.x, A.y)
    # glVertex2f(B.x, B.y)
    # glVertex2f(C.x, C.y)
    # glVertex2f(D.x, D.y)
    # glEnd()
    # if (imprimeEnvelope):
    #     A.imprime("A:");
    #     B.imprime("B:");
    #     C.imprime("C:");
    #     D.imprime("D:");
    #     print("");

    Personagens[i].Envelope[0] = A
    Personagens[i].Envelope[1] = B
    Personagens[i].Envelope[2] = C
    Personagens[i].Envelope[3] = D

# ***********************************************************************************
# Gera sempre uma posicao na metade de baixo da tela


def GeraPosicaoAleatoria():
    x = random.randint(-LarguraDoUniverso, LarguraDoUniverso)
    y = random.randint(-LarguraDoUniverso, LarguraDoUniverso)
    return Ponto(x, y)


# ***********************************************************************************
def AtualizaJogo():
    global imprimeEnvelope, nInstancias, Personagens
    #  Esta funcao deverá atualizar todos os elementos do jogo
    #  em funcao das novas posicoes dos personagens
    #  Entre outras coisas, deve-se:

    #   - calcular colisões
    #  Para calcular as colisoes eh preciso fazer o calculo do envelopes de
    #  todos os personagens

    for i in range(0, nInstancias):
        AtualizaEnvelope(i)
        if (imprimeEnvelope):  # pressione E para alterar esta flag
            print("Envelope ", i)
            Personagens[i].ImprimeEnvelope("", "")
    imprimeEnvelope = False

    # Feito o calculo, eh preciso testar todos os tiros e
    # demais personagens contra o jogador
    for i in range(1, nInstancias):
        if TestaColisao(0, i):
            # neste exemplo, a posicao do tiro é gerada aleatoriamente apos a colisao
            Personagens[i] = copy.deepcopy(Personagens[i+AREA_DE_BACKUP])
            Personagens[i].Posicao = GeraPosicaoAleatoria()
            Personagens[i].Posicao.imprime("Nova posicao:")
            ang = random.randint(0, 360)
            Personagens[i].Rotacao = ang
            Personagens[i].Direcao = Ponto(0, 1)
            Personagens[i].Direcao.rotacionaZ(ang)
            print("Nova Orientacao: ", ang)

        else:
            pass
            # print ("SEM Colisao")


def AtualizaPersonagens(tempoDecorrido):
    global nInstancias
    for i in range(0, nInstancias):
        Personagens[i].AtualizaPosicao(tempoDecorrido)

        # if i == 0:  # Lógica de envolvimento para a nave do jogador
        # Lógica horizontal
        if Personagens[i].Posicao.x > LarguraDoUniverso:
            Personagens[i].Posicao.x -= 2 * LarguraDoUniverso
        elif Personagens[i].Posicao.x < -LarguraDoUniverso:
            Personagens[i].Posicao.x += 2 * LarguraDoUniverso

        # Lógica vertical
        if Personagens[i].Posicao.y > LarguraDoUniverso:
            Personagens[i].Posicao.y -= 2 * LarguraDoUniverso
        elif Personagens[i].Posicao.y < -LarguraDoUniverso:
            Personagens[i].Posicao.y += 2 * LarguraDoUniverso
        # else:  # Lógica para naves inimigas
        #     if Personagens[i].Posicao.x > LarguraDoUniverso or Personagens[i].Posicao.x < -LarguraDoUniverso:
        #         Personagens[i].Posicao.x = LarguraDoUniverso/2
        #         Personagens[i].Posicao.y = LarguraDoUniverso/2
        #         # Personagens[i].Rotacao = (Personagens[i].Rotacao + 180) % 360  # Ajusta a rotação para oposta
        #     if Personagens[i].Posicao.y > LarguraDoUniverso or Personagens[i].Posicao.y < -LarguraDoUniverso:
        #         Personagens[i].Posicao.x = LarguraDoUniverso/2
        #         Personagens[i].Posicao.y = LarguraDoUniverso/2  # Inverte a direção vertical
        #         # Personagens[i].Rotacao = (Personagens[i].Rotacao  + 180) % 360  # Ajusta a rotação para oposta

        #     # Normaliza a direção após a mudança
        #     magnitude = math.sqrt(Personagens[i].Direcao.x**2 + Personagens[i].Direcao.y**2)
        #     if magnitude > 0:
        #         Personagens[i].Direcao.x /= magnitude
        #         Personagens[i].Direcao.y /= magnitude

            # Ajuste para manter a nave dentro dos limites do universo
            Personagens[i].Posicao.x = max(min(Personagens[i].Posicao.x, LarguraDoUniverso), -LarguraDoUniverso)
            Personagens[i].Posicao.y = max(min(Personagens[i].Posicao.y, LarguraDoUniverso), -LarguraDoUniverso)

    AtualizaJogo()



# ***********************************************************************************
def DesenhaPersonagens():
    global PersonagemAtual, nInstancias

    for i in range(0, nInstancias):
        PersonagemAtual = i
        Personagens[i].Desenha()


# ***********************************************************************************
def CarregaModelos():
    global Modelos
    # Nave tem q ser o modelo 0 por conta da alteracao q fiz na rotacao de Z


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
    Modelos[5].leModelo("Vida.txt")
    Modelos.append(ModeloMatricial())
    Modelos[6].leModelo("VidaPos.txt")



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

    i = 0
    ang = -90.0
    modelo_nave = Modelos[0]  # Supondo que o Modelo 0 é a nave
    # !!!!!!!!!!!!!!!!! Aqui onde altera aonde a nave é rotacionada !!!!!!!!!!!!!!!!!
    centro_pivot_nave = Ponto(modelo_nave.nColunas / 2,
                              modelo_nave.nLinhas * 0.1)

    Personagens[i].Posicao = Ponto(-2.5, 0)
    Personagens[i].Escala = Ponto(1, 1)
    Personagens[i].Rotacao = ang
    Personagens[i].IdDoModelo = 0
    Personagens[i].Modelo = DesenhaPersonagemMatricial
    # Aqui define o ponto central como pivot
    Personagens[i].Pivot = centro_pivot_nave
    Personagens[i].Direcao = Ponto(0, 1)
    Personagens[i].Direcao.rotacionaZ(ang)
    Personagens[i].Velocidade = 5

    # Salva os dados iniciais do personagem i na area de backup
    Personagens[i+AREA_DE_BACKUP] = copy.deepcopy(Personagens[i])

    # Personagens[0].ImprimeEnvelope("Envelope:")

    i = i + 1
    ang = 90
    Personagens[i].Posicao = Ponto(13.5, 0)
    Personagens[i].Escala = Ponto(1, 1)
    Personagens[i].Rotacao = ang
    Personagens[i].IdDoModelo = 1
    Personagens[i].Modelo = DesenhaPersonagemMatricial
    Personagens[i].Pivot = Ponto(0.5, 0)
    Personagens[i].Direcao = Ponto(0, 1)  # direcao do movimento para a cima
    Personagens[i].Direcao.rotacionaZ(ang)  # direcao alterada para a direita
    Personagens[i].Velocidade = 15   # move-se a 3 m/s

    # Salva os dados iniciais do personagem i na area de backup
    Personagens[i+AREA_DE_BACKUP] = copy.deepcopy(Personagens[i])

    for j in range(1, 4):  # Começando de 1 até 3, evitando o modelo 0 da nave espacial
        i += 1
        Personagens[i].Posicao = GeraPosicaoAleatoria()
        Personagens[i].Escala = Ponto(0, 5)
        Personagens[i].Rotacao = random.randint(0, 360)
        Personagens[i].IdDoModelo = j + 1  # Agora 'j' será 1 ou 2, correspondendo aos modelos inimigos
        Personagens[i].Modelo = DesenhaPersonagemMatricial
        Personagens[i].Pivot = Ponto(0.5, 0)  # Pivot no centro
        Personagens[i].Direcao = Ponto(0, 1)
        Personagens[i].Direcao.rotacionaZ(Personagens[i].Rotacao)
        Personagens[i].Velocidade = 15  # Velocidade aleatória
        Personagens[i+AREA_DE_BACKUP] = copy.deepcopy(Personagens[i])
    
       

        # Espaçamento entre os corações
        espacamento = 5
        largura_coracao = 18
        altura_coracao = 14
        LarguraDoUniverso = 150 
        # Posição inicial dos corações no canto superior direito
        x = LarguraDoUniverso - largura_coracao - espacamento
        y = LarguraDoUniverso - altura_coracao - espacamento

        for k in range(1, 4):
            i += 1 
            Personagens[i].Posicao = Ponto(x, y)
            Personagens[i].Escala = Ponto(1, 1)
            Personagens[i].Rotacao = 0
            Personagens[i].IdDoModelo = 5
            Personagens[i].Modelo = DesenhaPersonagemMatricial
            Personagens[i].Pivot = Ponto(0, 0)  # Pivot no centro
            Personagens[i].Direcao = Ponto(0, 0)
            Personagens[i].Direcao.rotacionaZ(Personagens[i].Rotacao)
            Personagens[i].Velocidade = 0  # Velocidade aleatória
            Personagens[i+AREA_DE_BACKUP] = copy.deepcopy(Personagens[i])
            
            x -= largura_coracao + espacamento  # Muda a posição X para o próximo coração
    
    nInstancias = i + 1 


# ***********************************************************************************
# Programa Principal
# ***********************************************************************************
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA)
# Define o tamanho inicial da janela grafica do programa
glutInitWindowSize(800, 800)
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
