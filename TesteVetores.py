from InstanciaVT1 import *
import copy

Personagens = [Instancia() for x in range(100)]

def CriaInstancias():
    global Personagens, nInstancias

    print ("Tamanho antes: ", len(Personagens))
    i = 0
    ang = -45.0
    #Personagens.append(Instancia())
    Personagens[i].Posicao = Ponto (-10,0)
    Personagens[i].Escala = Ponto (1,1)
    Personagens[i].Rotacao = ang
    Personagens[i].IdDoModelo = 0
    #Personagens[i].Modelo = DesenhaPersonagemMatricial
    Personagens[i].Pivot = Ponto(2.5,0)
    Personagens[i].Direcao = Ponto(0,1) # direcao do movimento para a cima
    Personagens[i].Direcao.rotacionaZ(ang) # direcao alterada para a direita
    Personagens[i].Velocidade = 5 # move-se a 5 m/s

    #Personagens[0].ImprimeEnvelope("Envelope:")

    #Personagens.append(Instancia()) 
    i = i + 1
    ang = 60
    Personagens[i].Posicao = Ponto (-0.5,0)
    Personagens[i].Escala = Ponto (1,1)
    Personagens[i].Rotacao = ang
    Personagens[i].IdDoModelo = 1
    #Personagens[i].Modelo = DesenhaPersonagemMatricial
    Personagens[i].Pivot = Ponto(0.5,0)
    Personagens[i].Direcao = Ponto(0,1) # direcao do movimento para a cima
    Personagens[i].Direcao.rotacionaZ(ang) # direcao alterada para a direita
    Personagens[i].Velocidade = 3    # move-se a 3 m/s

    # Salva os dados iniciais do personagem i na area de backup
    # Personagens[i+AREA_DE_BACKUP] = Personagens[i];
    nInstancias = i+1;
    print ("Tamanho depois: ", len(Personagens))

Personagens[0].Direcao = Ponto (4,5,6)
Personagens[30] = copy.deepcopy(Personagens[0]) 

Personagens[0].Direcao = Ponto (3,3,3)

Personagens[0].Direcao.imprime("P0")
Personagens[30].Direcao.imprime("P30")

