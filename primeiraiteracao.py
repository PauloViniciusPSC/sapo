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

# --- Configurações da Janela ---
largura, altura = 1100, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Simulacao")

# --- Cores ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (34, 139, 34)
MARROM = (139, 69, 19)
AMARELO = (255,236,63)
AZUL = (0,74,173)
VERMELHO = (255,0,0)
ROXO = (214,52,235)
LARANJA = (255,162,3)
VERDE_CLARO = (0,191,99) 
# Cor da tabela para as bordas (será usada como a cor de um retângulo para as bordas)
cor_da_tabela = (193,255,114)                   
                   
# --- Variáveis de Jogo ---
raio_do_buraco = 17
largura_tela = 1100
altura_tela = 600
margem_da_mesa = 50
coeficiente_absorcao_mesa = 0.95 

# Classe para bola
class Bola:
    def __init__(self, x, y, cor, numero):
        self.numero = numero
        self.pos = pygame.Vector2(x, y) # Usando Vector2 para facilitar a matemática
        self.cor = cor
        self.raio = 15
        self.velocidade = pygame.Vector2(0, 0)
        self.ativa = True
        self.raio_marcacao = 7
        self.cor_marcacao = BRANCO
    
    def desenhar(self, tela):
        if self.ativa:
            pygame.draw.circle(tela, self.cor, (int(self.pos.x), int(self.pos.y)), self.raio)
            # Desenha a marcação da bola (se necessário)
            pygame.draw.circle(tela, self.cor_marcacao, (int(self.pos.x), int(self.pos.y)), self.raio_marcacao)

    def mover(self):
        self.pos += self.velocidade
        
        # Atrito
        self.velocidade *= 0.99
        
        if self.velocidade.length() < 0.1:
            self.velocidade = pygame.Vector2(0, 0)
    
    # --- Nova lógica de colisão com as bordas da mesa ---
    def colisao_com_bordas(self):
        # Colisão com as bordas laterais
        if self.pos.x - self.raio <= margem_da_mesa or self.pos.x + self.raio >= largura - margem_da_mesa:
            self.velocidade.x *= -coeficiente_absorcao_mesa
            # Ajusta a posição para evitar que a bola "grude" na parede
            if self.pos.x - self.raio <= margem_da_mesa:
                self.pos.x = margem_da_mesa + self.raio
            if self.pos.x + self.raio >= largura - margem_da_mesa:
                self.pos.x = largura - margem_da_mesa - self.raio
        
        # Colisão com as bordas superior e inferior
        if self.pos.y - self.raio <= margem_da_mesa or self.pos.y + self.raio >= altura - margem_da_mesa:
            self.velocidade.y *= -coeficiente_absorcao_mesa
            # Ajusta a posição para evitar que a bola "grude" na parede
            if self.pos.y - self.raio <= margem_da_mesa:
                self.pos.y = margem_da_mesa + self.raio
            if self.pos.y + self.raio >= altura - margem_da_mesa:
                self.pos.y = altura - margem_da_mesa - self.raio

    def entrou_buraco(self, buracos):
        for buraco in buracos:
            distancia = self.pos.distance_to(buraco.posicao)
            if distancia < buraco.raio:
                self.ativa = False
                self.velocidade = pygame.Vector2(0, 0)

class Buraco:
    def __init__(self, nome, posicao, raio, cor):
        self.posicao = posicao
        self.raio = raio
        self.cor = cor 
        self.nome = nome

# --- Funções de Colisão ---
def detectar_colisao(bola1, bola2):
    distancia = bola1.pos.distance_to(bola2.pos)
    if distancia <= bola1.raio + bola2.raio:
        return True
    return False
'''
def tratar_colisao(bola1, bola2):
    # Vetor de colisão
    normal_vetor = bola2.pos - bola1.pos
    distancia = normal_vetor.length()
    
    # Para evitar erros de divisão por zero se as bolas estiverem na mesma posição
    if distancia == 0:
        return

    normal_vetor.normalize_ip()

    # Componentes de velocidade ao longo do vetor normal
    p1 = bola1.velocidade.dot(normal_vetor)
    p2 = bola2.velocidade.dot(normal_vetor)
    
    # Velocidades após a colisão
    v1_final = p2 * normal_vetor
    v2_final = p1 * normal_vetor
    
    # Velocidades tangenciais (perpendiculares ao vetor normal)
    t1_vetor = bola1.velocidade - p1 * normal_vetor
    t2_vetor = bola2.velocidade - p2 * normal_vetor
    
    # Velocidades finais
    bola1.velocidade = v2_final + t1_vetor
    bola2.velocidade = v1_final + t2_vetor
    
    # Separar as bolas para evitar que grudem
    superposicao = (bola1.raio + bola2.raio) - distancia
    bola1.pos -= normal_vetor * (superposicao / 2)
    bola2.pos += normal_vetor * (superposicao / 2)
'''
def tratar_colisao(bola1, bola2):
    # Vetor de colisão (do centro da bola1 para o centro da bola2)
    normal_vetor = bola2.pos - bola1.pos
    distancia = normal_vetor.length()
    
    # Para evitar erros de divisão por zero se as bolas estiverem na mesma posição
    if distancia == 0:
        return

    normal_vetor.normalize_ip()

    # Componentes de velocidade ao longo do vetor normal
    p1 = bola1.velocidade.dot(normal_vetor)
    p2 = bola2.velocidade.dot(normal_vetor)
    
    # Velocidades após a colisão
    v1_final = p2 * normal_vetor
    v2_final = p1 * normal_vetor
    
    # Velocidades tangenciais (perpendiculares ao vetor normal)
    t1_vetor = bola1.velocidade - p1 * normal_vetor
    t2_vetor = bola2.velocidade - p2 * normal_vetor
    
    # Velocidades finais
    bola1.velocidade = v2_final + t1_vetor
    bola2.velocidade = v1_final + t2_vetor
    
    # --- NOVO TRECHO DE CÓDIGO ---
    # Separar as bolas para evitar que grudem. Isso resolve o problema de tremor.
    superposicao = (bola1.raio + bola2.raio) - distancia
    bola1.pos -= normal_vetor * (superposicao / 2)
    bola2.pos += normal_vetor * (superposicao / 2)


# --- Funções de Desenho ---
def desenhar_taco(tela, bola_branca, pos_clique, pos_arrasto):
    # Vetor de arrasto do mouse
    vetor_arrasto = pos_arrasto - pos_clique
    
    # Vetor do taco (inverso ao arrasto)
    vetor_taco = -vetor_arrasto
    
    if vetor_taco.length() > 0:
        vetor_taco.normalize_ip()
    
    # Posição da ponta do taco (perto da bola)
    ponta_taco = bola_branca.pos - vetor_taco * 20
    
    # Posição da base do taco (distancia-se da bola com o arrasto)
    base_taco = ponta_taco + vetor_taco * vetor_arrasto.length()

    # Desenha o taco
    pygame.draw.line(tela, MARROM, (int(ponta_taco.x), int(ponta_taco.y)), (int(base_taco.x), int(base_taco.y)), 8)


# --- Criando Objetos do Jogo ---

# Buracos
buracos = [
    Buraco("buraco1", (margem_da_mesa, margem_da_mesa), raio_do_buraco, PRETO),
    Buraco("buraco2", (largura/2, margem_da_mesa), raio_do_buraco, PRETO),
    Buraco("buraco3", (largura - margem_da_mesa, margem_da_mesa), raio_do_buraco, PRETO),
    Buraco("buraco4", (margem_da_mesa, altura - margem_da_mesa), raio_do_buraco, PRETO),
    Buraco("buraco5", (largura/2, altura - margem_da_mesa), raio_do_buraco, PRETO),
    Buraco("buraco6", (largura - margem_da_mesa, altura - margem_da_mesa), raio_do_buraco, PRETO)
]

# Bolas
bola_branca = Bola(largura / 4, altura / 2, BRANCO, 0)
bola_um = Bola(largura / 2, altura / 2, AMARELO, 1)
bola_dois = Bola(largura / 2 + 50, altura / 2 + 50, AZUL, 2)
bolas = [bola_branca, bola_um, bola_dois]

# Variáveis para a tacada
pos_inicial_clique = None
pos_final_arraste = None
mouse_pressionado = False

# Loop principal do jogo
rodando = True
clock = pygame.time.Clock()

while rodando:
    clock.tick(60)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                # Reiniciar o jogo
                bola_branca.pos = pygame.Vector2(largura / 4, altura / 2)
                bola_branca.velocidade = pygame.Vector2(0, 0)
                
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse_pressionado = True
            pos_inicial_clique = pygame.Vector2(evento.pos)
            pos_final_arraste = pygame.Vector2(evento.pos)
        
        elif evento.type == pygame.MOUSEMOTION and mouse_pressionado:
            pos_final_arraste = pygame.Vector2(evento.pos)
            
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            mouse_pressionado = False
            
            # Aplica a força na bola branca quando o taco é liberado
            vetor_arrasto = pos_final_arraste - pos_inicial_clique
            forca_tacada = vetor_arrasto.length() * 0.1  # Multiplicador para ajustar a força
            
            direcao_tacada = -vetor_arrasto
            if direcao_tacada.length() > 0:
                direcao_tacada.normalize_ip()
            
            bola_branca.velocidade = direcao_tacada * forca_tacada
            pos_inicial_clique = None
            
    # --- Atualizar o estado do jogo ---
    for bola in bolas:
        if bola.ativa:
            bola.mover()
            bola.colisao_com_bordas()  # Usando a nova lógica de colisão

    # Colisão entre as bolas
    for i in range(len(bolas)):
        for j in range(i + 1, len(bolas)):
            if bolas[i].ativa and bolas[j].ativa:
                if detectar_colisao(bolas[i], bolas[j]):
                    tratar_colisao(bolas[i], bolas[j])

    # Verificar se as bolas entraram nos buracos
    for bola in bolas:
        if bola.ativa:
            bola.entrou_buraco(buracos)

    # --- Desenhar na Tela ---
    tela.fill(VERDE)

    # Desenhar as bordas
    pygame.draw.rect(tela, cor_da_tabela, (0, 0, largura, margem_da_mesa))
    pygame.draw.rect(tela, cor_da_tabela, (0, altura - margem_da_mesa, largura, margem_da_mesa))
    pygame.draw.rect(tela, cor_da_tabela, (0, 0, margem_da_mesa, altura))
    pygame.draw.rect(tela, cor_da_tabela, (largura - margem_da_mesa, 0, margem_da_mesa, altura))

    # Desenhar os buracos
    for buraco in buracos:
        pygame.draw.circle(tela, buraco.cor, buraco.posicao, buraco.raio)

    # Desenhar as bolas
    for bola in bolas:
        bola.desenhar(tela)

    # Desenhar o taco
    if mouse_pressionado and pos_inicial_clique is not None:
        desenhar_taco(tela, bola_branca, pos_inicial_clique, pos_final_arraste)
        
    pygame.display.flip()

# Encerrar o Pygame
pygame.quit()