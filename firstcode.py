import pygame
import math

# --- Configurações Iniciais ---
pygame.init()

# Definindo as cores
VERDE_LIMA = (50, 205, 50)
VERDE_ESCURO = (0, 100, 0)
MARROM = (139, 69, 19)
BRANCO = (255, 255, 255)

# Tamanho da janela
LARGURA_JANELA = 500
ALTURA_JANELA = 500

# Borda da mesa
LARGURA_BORDA = 40

# --- Configuração da Janela ---
tela = pygame.display.set_mode((LARGURA_JANELA, ALTURA_JANELA))
pygame.display.set_caption("Sinuca 2D")

# --- Variáveis do Jogo ---
# Posição e velocidade da bola branca
bola_branca_pos = pygame.Vector2(LARGURA_JANELA // 2, ALTURA_JANELA // 2)
bola_branca_velocidade = pygame.Vector2(0, 0)
bola_branca_diametro = 20  # Aumentado para 20 pixels
bola_branca_raio = bola_branca_diametro // 2

# Variáveis para a tacada
pos_inicial_clique = None
pos_final_arraste = None
mouse_pressionado = False

# Variáveis para o taco
taco_comprimento = 100  # Comprimento do taco em pixels
taco_largura = 5

# --- Loop Principal do Jogo ---
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        # Lógica para o clique e arrasto do mouse
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse_pressionado = True
            pos_inicial_clique = pygame.Vector2(evento.pos)
            pos_final_arraste = pygame.Vector2(evento.pos)
        
        elif evento.type == pygame.MOUSEMOTION and mouse_pressionado:
            pos_final_arraste = pygame.Vector2(evento.pos)
            
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            mouse_pressionado = False
            
            # --- Lógica da Tacada ---
            # 1. Calcular o vetor de arrasto
            vetor_arrasto = pos_final_arraste - pos_inicial_clique
            
            # 2. Calcular a força da tacada (baseada na distância do arrasto)
            forca_tacada = vetor_arrasto.length() * 0.1 # Multiplicador para controlar a velocidade
            
            # 3. Inverter o vetor de arrasto para obter a direção da tacada
            direcao_tacada = -vetor_arrasto
            if direcao_tacada.length() > 0:
                direcao_tacada = direcao_tacada.normalize() # Normaliza para ter um vetor de direção

            # 4. Aplicar a velocidade à bola branca
            bola_branca_velocidade = direcao_tacada * forca_tacada
            
    # --- Atualizar o estado do jogo ---
    # Movimentar a bola
    bola_branca_pos += bola_branca_velocidade
    
    # Aplicar atrito para desacelerar a bola gradualmente
    bola_branca_velocidade *= 0.98

    # Parar a bola quando a velocidade for muito baixa
    if bola_branca_velocidade.length() < 0.1:
        bola_branca_velocidade = pygame.Vector2(0, 0)

    # --- Desenhar na Tela ---
    
    # 1. Desenhar a mesa (fundo verde-lima)
    tela.fill(VERDE_LIMA)
    
    # 2. Desenhar as bordas
    pygame.draw.rect(tela, VERDE_ESCURO, (0, 0, LARGURA_JANELA, LARGURA_BORDA))
    pygame.draw.rect(tela, VERDE_ESCURO, (0, ALTURA_JANELA - LARGURA_BORDA, LARGURA_JANELA, LARGURA_BORDA))
    pygame.draw.rect(tela, VERDE_ESCURO, (0, 0, LARGURA_BORDA, ALTURA_JANELA))
    pygame.draw.rect(tela, VERDE_ESCURO, (LARGURA_JANELA - LARGURA_BORDA, 0, LARGURA_BORDA, ALTURA_JANELA))
    
    # 3. Desenhar a bola branca
    pygame.draw.circle(tela, BRANCO, (int(bola_branca_pos.x), int(bola_branca_pos.y)), bola_branca_raio)

    # 4. Desenhar o taco
    if mouse_pressionado:
        # Posição do taco
        vetor_direcao = (pos_inicial_clique - pos_final_arraste)
        if vetor_direcao.length() > 0:
            vetor_direcao = vetor_direcao.normalize()
            
        taco_ponta = bola_branca_pos - vetor_direcao * 30 # A ponta do taco fica perto da bola
        taco_base = taco_ponta + vetor_direcao * taco_comprimento
        
        # Desenhar uma linha que representa o taco
        pygame.draw.line(tela, MARROM, taco_ponta, taco_base, taco_largura)

    # Atualizar a tela
    pygame.display.flip()

# Finaliza o Pygame
pygame.quit()