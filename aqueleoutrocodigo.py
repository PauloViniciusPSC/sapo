
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 18:49:14 2024

@author: paulo
"""

import pygame
import math
import itertools
import numpy as np

# Inicialização do Pygame
pygame.init()

# Configurações da janela
largura, altura = 1100, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Simulacao")

# Cores
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
PRETO = (0, 0, 0)
VERDE = (34, 139, 34)
MARROM = (139, 69, 19)
#cores das bolas 
AMARELO = (255,236,63)#bola1E9
AZUL = (0,74,173) #bola2E10
VERMELHO = (255,0,0) #bola 3E11
ROXO = (214,52,235)#bola4E12
LARANJA = (255,162,3),#bola5E13
VERDE_CLARO = (0,191,99) #bola6E14
MARROM = (221,147,5) #bol7
PRETO = (0,0,0) #bola8
AMARELO = (255,236,63)#bola9
AZUL = (0,74,173) #bola10
cor_da_tabela = (193,255,114)                   
                   
                   
        
#variaveis
raio_do_buraco = 17
margem_dos_buracos = 33
largura_tela = 1100
altura_tela = 600
margem_da_mesa = 50
coeficiente_absorcao_mesa = 0.95 # o quanto de energia a bola perde quando colide com a borda....
#posições iniciais das bolas 



# Classe para bola
class Bola:
    def __init__(self, x, y, cor,numero):
        self.numero = numero
        self.x = x
        self.y = y
        self.cor = cor
        self.raio = 15
        self.vel_x = 0
        self.vel_y = 0
        self.ativa = True  # Para saber se a bola ainda está em jogo
        self.raio_marcacao = 7
        self.cor_marcacao = BRANCO
    def desenhar(self, tela):
        if self.ativa:
            pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
            pygame.draw.circle(tela, self.cor_marcacao, (int(self.x),int(self.y)),self.raio_marcacao)

    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y

        # Atrito simples para desacelerar as bolas
        self.vel_x *= 0.99
        self.vel_y *= 0.99

        # Limites da tela (bordas)
        if self.x - self.raio < 0 or self.x + self.raio > largura:
            self.vel_x = -self.vel_x
        if self.y - self.raio < 0 or self.y + self.raio > altura:
            self.vel_y = -self.vel_y

    def entrou_buraco(self, buracos):
        # Verificar se a bola entrou em um dos buracos
        for buraco in buracos:
            distancia = math.hypot(self.x - buraco[0], self.y - buraco[1])
            
            #a bola cai no buraco se o centro dela colide com a borda do buraco
            if distancia < buraco[2]:  # Raio do buraco
                self.ativa = False  # A bola saiu de jogo
                self.vel_x, self.vel_y = 0, 0
           

class Buraco:
    def __init__(self,nome ,posicao, raio, cor):
        self.posicao = posicao
        self.raio = raio
        self.cor = cor 
        self.nome = nome
    
    
class Tabela():
    '''Isso aqui é so p ingles ver, não vai afetar em nada o nosso código!'''
    def __init__(self,nome,pontos,cor):
        self.nome = nome
        self.pontos = pontos 
        self.cor = cor 
    
    
class Linha():
    def __init__(self,pontoA,pontoB,cor,tipo):
        self.A = pontoA
        self.B = pontoB
        self.cor = cor
        self.tipo = tipo





# Função para detectar colisão entre duas bolas
def detectar_colisao(bola1, bola2):
    distancia = math.hypot(bola2.x - bola1.x, bola2.y - bola1.y)
    if distancia < bola1.raio + bola2.raio:
        return True
    return False


# Funcao para detectar colisao entre bolas e linhas
# Funcao que calcula a distancia entre dois pontos:
def distancia(p1,p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

# Função para projetar um ponto sobre uma linha e verificar se a projeção está dentro do segmento
def projetar_ponto_na_linha(ponto, A, B):
    # Vetores AB e AP
    AB = (B[0] - A[0], B[1] - A[1])
    AP = (ponto[0] - A[0], ponto[1] - A[1])

    # Produto escalar entre AP e AB
    produto_escalar = AP[0] * AB[0] + AP[1] * AB[1]
    comprimento_AB_quadrado = AB[0]**2 + AB[1]**2

    # Parâmetro t da projeção
    t = produto_escalar / comprimento_AB_quadrado

    # t < 0 significa que está fora da linha, antes do ponto A
    # t > 1 significa que está fora da linha, depois do ponto B
    # 0 <= t <= 1 significa que está no segmento de linha
    t = max(0, min(1, t))

    # Coordenadas do ponto projetado no segmento de linha
    ponto_projetado = (A[0] + t * AB[0], A[1] + t * AB[1])
    return ponto_projetado


# Função para detectar a colisão entre um círculo e uma linha (definida por dois pontos A e B)
def colisao_linha_bola(circulo_pos, circulo_raio, A, B):
    # Encontrar o ponto mais próximo do círculo na linha (A, B)
    ponto_projetado = projetar_ponto_na_linha(circulo_pos, A, B)

    # Calcular a distância entre o centro do círculo e o ponto projetado
    distancia_ao_segmento = distancia(circulo_pos, ponto_projetado)

    # Se a distância entre o círculo e a linha for menor ou igual ao raio, há colisão
    if distancia_ao_segmento <= circulo_raio:
        return True
    return False   


# Função para tratar colisão entre duas bolas
def tratar_colisao(bola1, bola2):
    dx = bola2.x - bola1.x
    dy = bola2.y - bola1.y
    distancia = math.hypot(dx, dy)

    # Normalizar vetor de colisão
    if distancia == 0:
        distancia = 1

    nx = dx / distancia
    ny = dy / distancia

    # Calculando o produto escalar para cada bola
    p = 2 * (bola1.vel_x * nx + bola1.vel_y * ny - bola2.vel_x * nx - bola2.vel_y * ny) / 2

    # Aplicando as novas velocidades
    bola1.vel_x -= p * nx
    bola1.vel_y -= p * ny
    bola2.vel_x += p * nx
    bola2.vel_y += p * ny


# Criar os buracos da mesa (posições x, y e raio)
buracos = [(margem_dos_buracos, margem_dos_buracos, raio_do_buraco), 
           (largura_tela/2, margem_dos_buracos, raio_do_buraco), 
           (largura_tela - margem_dos_buracos, margem_dos_buracos, raio_do_buraco), 
           (margem_dos_buracos, altura_tela - margem_dos_buracos, raio_do_buraco), 
           (largura_tela/2, altura_tela - margem_dos_buracos, raio_do_buraco), 
           (largura_tela - margem_dos_buracos, altura_tela - margem_dos_buracos, raio_do_buraco)]

#criando os buracos:
buracoss = []
buracoss.append(Buraco("buraco1",(int(buracos[0][0]),int(buracos[0][1])),raio_do_buraco,PRETO))
buracoss.append(Buraco("buraco2",(int(buracos[1][0]),int(buracos[1][1])),raio_do_buraco,PRETO))
buracoss.append(Buraco("buraco3",(int(buracos[2][0]),int(buracos[2][1])),raio_do_buraco,PRETO))
buracoss.append(Buraco("buraco4",(int(buracos[3][0]),int(buracos[3][1])),raio_do_buraco,PRETO))
buracoss.append(Buraco("buraco5",(int(buracos[4][0]),int(buracos[4][1])),raio_do_buraco,PRETO))
buracoss.append(Buraco("buraco6",(int(buracos[5][0]),int(buracos[5][1])),raio_do_buraco,PRETO))

# Criar as tabelas da mesa( posicoes x e y):
pontos_um = [(26,0),
               (550 - 18,0),
               (550 -18,margem_da_mesa),
               (margem_da_mesa + 26,margem_da_mesa)]
pontos_dois = [(550 + 18,0),
                 (550 + 18,margem_da_mesa),
                 (largura_tela - margem_da_mesa - 26 ,margem_da_mesa),
                 (largura_tela - 26,0)]
pontos_tres = [(0,26),
                 (margem_da_mesa,margem_da_mesa+ 26),
                 (margem_da_mesa,altura_tela - margem_da_mesa - 26),
                 (0,altura_tela -26)]
pontos_quatro = [(largura_tela,26),
                   (largura_tela - margem_da_mesa,margem_da_mesa + 26),
                   (largura_tela - margem_da_mesa,altura_tela - margem_da_mesa - 26),
                   (largura_tela,altura_tela - 26)]
pontos_cinco = [(26,altura_tela),
                  (margem_da_mesa + 26,altura_tela - margem_da_mesa),
                  (550 - 18, altura_tela - margem_da_mesa),
                  (550 - 18,altura_tela)]
pontos_seis = [(550 + 18,altura_tela),
                 (550 + 18,altura_tela - margem_da_mesa),
                 (largura_tela - margem_da_mesa - 26, altura_tela - margem_da_mesa),
                 (largura_tela - 26,altura_tela)]  
#aqui a gente pode criar uma funcao para desenhar as tabelas:



    
#criando as tabelas:
tabelas = []
tabelas.append(Tabela('tabela1',pontos_um,cor_da_tabela))
tabelas.append(Tabela('tabela2',pontos_dois,cor_da_tabela))
tabelas.append(Tabela('tabela3',pontos_tres,cor_da_tabela))
tabelas.append(Tabela('tabela4',pontos_quatro,cor_da_tabela))
tabelas.append(Tabela('tabela5',pontos_cinco,cor_da_tabela))
tabelas.append(Tabela('tabela6',pontos_seis,cor_da_tabela))

#criando uma linha p desenvolvermos a parte das colisoes 
#linhas onde ocorrem as colisoes 
ponto_linha1 = [(margem_da_mesa + 26, margem_da_mesa),
               ((largura_tela/2) - 18, margem_da_mesa)]
ponto_linha2 = [(margem_da_mesa,margem_da_mesa + 26),
                (margem_da_mesa,altura_tela - margem_da_mesa - 26)]
ponto_linha3 = [(margem_da_mesa + 26, altura_tela - margem_da_mesa),
                (largura_tela/2 - 18, altura_tela - margem_da_mesa)]
ponto_linha4 = [(largura_tela - margem_da_mesa, margem_da_mesa + 26),
                (largura_tela - margem_da_mesa, altura_tela - margem_da_mesa - 26)]
ponto_linha5 = [(largura_tela/2 + 18, margem_da_mesa),
                (largura_tela - margem_da_mesa - 26, margem_da_mesa)]
ponto_linha6 = [(largura_tela/2 + 18, altura_tela - margem_da_mesa),
                (largura_tela - margem_da_mesa - 26, altura_tela - margem_da_mesa)]
#aqui serao as linhas que ficam nas bordas das cacapas.
#linhas da cacapa superior esquerda 
ponto_linha7 = [(26,0),
                (margem_da_mesa + 26, margem_da_mesa)]
ponto_linha8 = [(0,26),
                (margem_da_mesa,margem_da_mesa + 26)]
#linhas da cacapa inferior esquerda
ponto_linha9 = [(0,altura_tela - 26),
                (margem_da_mesa,altura_tela - margem_da_mesa - 26)]
ponto_linha10 = [(26,altura_tela),
                 (margem_da_mesa + 26, altura_tela - margem_da_mesa)]
#linhas da cacapa do meio superior 
ponto_linha11 = [(largura_tela/2 - 18, 0),
                 (largura_tela/2 - 18, margem_da_mesa)]
ponto_linha12 = [(largura_tela/2 + 18, 0),
                 (largura_tela/2 + 18, margem_da_mesa)]
#linhas da cacapa do meio inferior
ponto_linha13 = [(largura_tela/2 - 18, altura_tela - margem_da_mesa),
                 (largura_tela/2 - 18, altura_tela)]
ponto_linha14 = [(largura_tela/2 + 18, altura_tela - margem_da_mesa),
                 (largura_tela/2 + 18, altura_tela)]
#linhas da cacapa superior direita 
ponto_linha15 = [(largura_tela - margem_da_mesa - 26, margem_da_mesa),
                 (largura_tela - 26,0)]
ponto_linha16 = [(largura_tela-margem_da_mesa,margem_da_mesa + 26),
                 (largura_tela,26)]
#linhas da cacapa inferior direita 
ponto_linha17 = [(largura_tela - margem_da_mesa, altura_tela - margem_da_mesa - 26),
                 (largura_tela, altura_tela - 26)]
ponto_linha18 = [(largura_tela - margem_da_mesa - 26, altura_tela - margem_da_mesa),
                 (largura_tela - 26,altura_tela)]


linhas = []
linhas.append(Linha(ponto_linha1[0], ponto_linha1[1], PRETO, "superior"))
linhas.append(Linha(ponto_linha2[0], ponto_linha2[1], PRETO,"lateral_esquerda"))
linhas.append(Linha(ponto_linha3[0], ponto_linha3[1], PRETO, "inferior"))
linhas.append(Linha(ponto_linha4[0], ponto_linha4[1], PRETO, "lateral_direita"))
linhas.append(Linha(ponto_linha5[0], ponto_linha5[1], PRETO, "superior"))
linhas.append(Linha(ponto_linha6[0], ponto_linha6[1], PRETO, "inferior"))
#linhas da cacapa superior esquerda
linhas.append(Linha(ponto_linha7[0], ponto_linha7[1], PRETO, "superior"))
linhas.append(Linha(ponto_linha8[0], ponto_linha8[1], PRETO, "inferior"))
#linhas da cacapa inferior esquerda
linhas.append(Linha(ponto_linha9[0], ponto_linha9[1], PRETO, "superior"))
linhas.append(Linha(ponto_linha10[0], ponto_linha10[1], PRETO, "inferior"))
#linhas da cacapa do meio superior
linhas.append(Linha(ponto_linha11[0], ponto_linha11[1], PRETO, "lateral_esquerda"))
linhas.append(Linha(ponto_linha12[0], ponto_linha12[1], PRETO, "lateral_direita"))
#linhas da cacapa do meio inferior 
linhas.append(Linha(ponto_linha13[0], ponto_linha13[1], PRETO, "lateral_esquerda"))
linhas.append(Linha(ponto_linha14[0], ponto_linha14[1], PRETO, "lateral_direita"))
#linhas da cacapa superior direita
linhas.append(Linha(ponto_linha15[0], ponto_linha15[1], PRETO, "superior"))
linhas.append(Linha(ponto_linha16[0], ponto_linha16[1], PRETO, "inferior"))
#linhas da cacapa inferior direita 
linhas.append(Linha(ponto_linha17[0], ponto_linha17[1], PRETO, "superior"))
linhas.append(Linha(ponto_linha18[0], ponto_linha18[1], PRETO, "inferior"))


# Função para desenhar o taco
def desenhar_taco(tela, bola, mouse_pos, força):
    # Calcula o ângulo entre a bola e o mouse
    dx = mouse_pos[0] - bola.x
    dy = mouse_pos[1] - bola.y
    angulo = math.atan2(dy, dx)

    # Posição final do taco (20 pixels além da bola)
    taco_x = bola.x - math.cos(angulo) * (bola.raio + força)
    taco_y = bola.y - math.sin(angulo) * (bola.raio + força)

    # Desenha o taco (linha)
    pygame.draw.line(tela, MARROM, (bola.x, bola.y), (taco_x, taco_y), 8)

# Criando as bolas
bola_branca = Bola(400, 300, BRANCO,0)
bola_um = Bola(500, 300, AMARELO,1)
bola_dois = Bola(300, 300, AZUL,2)
bolas = [bola_branca, bola_um, bola_dois]

# Variáveis de controle do taco
taco_ativo = False
força = 0
força_max = 250
força_incremento = 2

# Variável de controle do jogo
jogando = True
clock = pygame.time.Clock()

# Loop principal do jogo
while jogando:
    # Limitando o FPS
    clock.tick(60)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogando = False

        # Controla quando o taco está ativo (clicando com o mouse)
        if event.type == pygame.MOUSEBUTTONDOWN:
            taco_ativo = True
            força = 0  # Reinicia a força

        if event.type == pygame.MOUSEBUTTONUP:
            taco_ativo = False
            # Aplica a força na bola branca quando o taco é liberado
            dx = pygame.mouse.get_pos()[0] - bola_branca.x
            dy = pygame.mouse.get_pos()[1] - bola_branca.y
            dist = math.hypot(dx, dy)
            bola_branca.vel_x = (dx / dist) * força / 10
            bola_branca.vel_y = (dy / dist) * força / 10
            força = 0

    # Movimento das bolas
    for bola in bolas:
        bola.mover()

    # Colisao entre as bolas
    for i in range(len(bolas)):
        for j in range(i + 1, len(bolas)):
            if bolas[i].ativa and bolas[j].ativa:
                if detectar_colisao(bolas[i], bolas[j]):
                    tratar_colisao(bolas[i], bolas[j])

    # Colisao entre bolas e as linhas
    # primeiro tem que ver se a bola colidiu com a linha 
    #se a bola colidir com a linha, a gente faz a colisão acontecer... 
    for combinacao_linha_bola in itertools.product(linhas, bolas):
        if colisao_linha_bola((combinacao_linha_bola[1].x, combinacao_linha_bola[1].y),
                             combinacao_linha_bola[1].raio,
                             combinacao_linha_bola[0].A, combinacao_linha_bola[0].B):
            #daria p fazer essa parte de uma forma mais técnica, mas estava dando muito erro e tals... 
            #abordagem mais direta!
            #se a bola colidir com uma linha superior:
            if combinacao_linha_bola[0].tipo == "superior":
                if combinacao_linha_bola[1].vel_x > 0 and combinacao_linha_bola[1].vel_y < 0:
                    combinacao_linha_bola[1].vel_x = combinacao_linha_bola[1].vel_x*0.95
                    combinacao_linha_bola[1].vel_y = combinacao_linha_bola[1].vel_y*-0.95
                elif combinacao_linha_bola[1].vel_x < 0 and combinacao_linha_bola[1].vel_y < 0:
                    combinacao_linha_bola[1].vel_x = combinacao_linha_bola[1].vel_x*0.95
                    combinacao_linha_bola[1].vel_y = combinacao_linha_bola[1].vel_y*-0.95
            #se a bola colidir com a linha lateral esquerda
            elif combinacao_linha_bola[0].tipo == "lateral_esquerda":    
                if combinacao_linha_bola[1].vel_x < 0 and combinacao_linha_bola[1].vel_y > 0:
                    combinacao_linha_bola[1].vel_x = combinacao_linha_bola[1].vel_x*-0.95
                    combinacao_linha_bola[1].vel_y = combinacao_linha_bola[1].vel_y*0.95
                elif combinacao_linha_bola[1].vel_x < 0 and combinacao_linha_bola[1].vel_y < 0:
                    combinacao_linha_bola[1].vel_x = combinacao_linha_bola[1].vel_x*-0.95
                    combinacao_linha_bola[1].vel_y = combinacao_linha_bola[1].vel_y*0.95
            #se a bola colidir com a linha lateral direita 
            elif combinacao_linha_bola[0].tipo == "lateral_direita":    
                if combinacao_linha_bola[1].vel_x > 0 and combinacao_linha_bola[1].vel_y > 0:
                    combinacao_linha_bola[1].vel_x = combinacao_linha_bola[1].vel_x*-0.95
                    combinacao_linha_bola[1].vel_y = combinacao_linha_bola[1].vel_y*0.95
                elif combinacao_linha_bola[1].vel_x > 0 and combinacao_linha_bola[1].vel_y < 0:
                    combinacao_linha_bola[1].vel_x = combinacao_linha_bola[1].vel_x*-0.95
                    combinacao_linha_bola[1].vel_y = combinacao_linha_bola[1].vel_y*0.95
            #se a bola colidir com uma linha inferior:
            elif combinacao_linha_bola[0].tipo == "inferior":    
                if combinacao_linha_bola[1].vel_x < 0 and combinacao_linha_bola[1].vel_y > 0:
                    combinacao_linha_bola[1].vel_x = combinacao_linha_bola[1].vel_x*0.95
                    combinacao_linha_bola[1].vel_y = combinacao_linha_bola[1].vel_y*-0.95
                elif combinacao_linha_bola[1].vel_x > 0 and combinacao_linha_bola[1].vel_y > 0:
                    combinacao_linha_bola[1].vel_x = combinacao_linha_bola[1].vel_x*0.95
                    combinacao_linha_bola[1].vel_y = combinacao_linha_bola[1].vel_y*-0.95
    
    # Verificar se as bolas entram nos buracos
    for bola in bolas:
        bola.entrou_buraco(buracos)

    # Aumenta a força enquanto o taco está ativo
    if taco_ativo:
        força = min(força + força_incremento, força_max)

    # Desenhar o fundo da mesa
    tela.fill(VERDE)

    # Desenhar os buracos
    for buraco in buracos:
        pygame.draw.circle(tela, PRETO, (buraco[0], buraco[1]), buraco[2])

    # Desenhar as tabelas:
    for tabela in tabelas:
        
        pygame.draw.polygon(tela,tabela.cor, tabela.pontos)    
    '''
    pygame.draw.polygon(tela,VERDE_CLARO, pontos_dois)    
    pygame.draw.polygon(tela,VERDE_CLARO, pontos_tres)    
    pygame.draw.polygon(tela,VERDE_CLARO, pontos_quatro)    
    pygame.draw.polygon(tela,VERDE_CLARO, pontos_cinco)    
    pygame.draw.polygon(tela,VERDE_CLARO, pontos_seis)    
    '''    
    for linha in linhas:
        pygame.draw.line(tela, linha.cor, linha.A, linha.B,)
        
    # Desenhar as bolas
    for bola in bolas:
        bola.desenhar(tela)

    # Desenhar o taco apenas se o jogador está mirando
    if taco_ativo or força > 0:
        desenhar_taco(tela, bola_branca, pygame.mouse.get_pos(), força)

    # Atualizar a tela
    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()
