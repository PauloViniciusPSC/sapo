import pygame
import math

# ==============================================================================
# 1. A FUNÇÃO EM TESTE (VERSÃO CORRETA E VERIFICADA)
# ==============================================================================
def desenhar_linha_tracejada(superficie, cor, inicio, fim, largura=1, espaco_traco=5):
    """Desenha uma linha tracejada na superfície do Pygame."""
    ponto_inicio = pygame.math.Vector2(inicio)
    ponto_fim = pygame.math.Vector2(fim)

    vetor = ponto_fim - ponto_inicio
    
    # Esta é a linha que estamos investigando.
    # '.length' é um atributo que retorna um número (float).
    comprimento = vetor.length()
    
    if comprimento < espaco_traco:
        # Se a linha for menor que um traço, desenha uma linha simples
        pygame.draw.line(superficie, cor, ponto_inicio, ponto_fim, largura)
        return
        
    # '.normalize()' é um método que retorna um novo vetor e precisa de '()'.
    direcao = vetor.normalize()
    
    pos_atual = ponto_inicio
    distancia_percorrida = 0
    
    while distancia_percorrida < comprimento:
        fim_traco = pos_atual + direcao * espaco_traco
        
        # Garante que o último traço não passe do ponto final
        if (fim_traco - ponto_inicio).length() > comprimento:
            fim_traco = ponto_fim

        pygame.draw.line(superficie, cor, pos_atual, fim_traco, largura)
        
        # Move para o início do próximo traço, pulando o espaço
        pos_atual = fim_traco + direcao * espaco_traco
        distancia_percorrida = (pos_atual - ponto_inicio).length
        
# ==============================================================================
# 2. CÓDIGO DE TESTE SIMPLES
# ==============================================================================
pygame.init()
tela = pygame.display.set_mode((500, 300))
pygame.display.set_caption("Teste da Linha Tracejada")
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
    
    tela.fill((0, 0, 50)) # Fundo azul escuro
    
    # Chamamos a função com valores fixos e simples para o teste
    ponto_a = (50, 150)
    ponto_b = pygame.mouse.get_pos() # A linha segue o mouse
    desenhar_linha_tracejada(tela, (255, 255, 0), ponto_a, ponto_b)
    
    pygame.display.flip()

pygame.quit()