import pygame
import pymunk
import pymunk.pygame_util
import math

# Inicialização do Pygame
pygame.init()

# --- Configurações da Janela ---
largura, altura = 1100, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Simulacao com Pymunk")

# --- Cores ---
BRANCO = (255, 255, 255, 255)
PRETO = (0, 0, 0, 255)
VERDE = (34, 139, 34, 255)
MARROM = (139, 69, 19, 255)
AMARELO = (255, 236, 63, 255)
AZUL = (0, 74, 173, 255)
VERMELHO = (255, 0, 0, 255)
cor_da_tabela = (193, 255, 114, 255)
                   
# --- Variáveis de Jogo ---
margem_da_mesa = 50
raio_bola = 15
raio_do_buraco = 17

# --- Configuração do Pymunk ---
# O "espaço" é o nosso mundo de física, onde tudo acontece
espaco = pymunk.Space()
espaco.gravity = (0, 0)  # Não queremos gravidade

# Ferramenta para desenhar objetos Pymunk com o Pygame
draw_options = pymunk.pygame_util.DrawOptions(tela)

# --- Funções para Criar Objetos ---
def criar_bola(posicao, raio, massa, cor):
    # Corpo (Body) -> contém a física (posição, velocidade, etc.)
    corpo_bola = pymunk.Body(massa, pymunk.moment_for_circle(massa, 0, raio))
    corpo_bola.position = posicao
    
    # Forma (Shape) -> usada para detecção de colisão
    forma_bola = pymunk.Circle(corpo_bola, raio)
    forma_bola.elasticity = 0.9  # Quão "saltitante" a bola é (1.0 = sem perda de energia)
    forma_bola.friction = 0.5    # Atrito da bola
    
    # Armazenamos a cor na forma para poder desenhar depois
    forma_bola.color = cor
    
    espaco.add(corpo_bola, forma_bola)
    return corpo_bola, forma_bola

def criar_mesa():
    # Bordas da mesa (linhas estáticas)
    bordas = [
        pymunk.Segment(espaco.static_body, (margem_da_mesa, margem_da_mesa), (largura - margem_da_mesa, margem_da_mesa), 10),
        pymunk.Segment(espaco.static_body, (largura - margem_da_mesa, margem_da_mesa), (largura - margem_da_mesa, altura - margem_da_mesa), 10),
        pymunk.Segment(espaco.static_body, (largura - margem_da_mesa, altura - margem_da_mesa), (margem_da_mesa, altura - margem_da_mesa), 10),
        pymunk.Segment(espaco.static_body, (margem_da_mesa, altura - margem_da_mesa), (margem_da_mesa, altura - margem_da_mesa), 10),
    ]
    
    # Definindo a cor e elasticidade das bordas
    for borda in bordas:
        borda.elasticity = 0.9
        borda.color = cor_da_tabela
        
    espaco.add(*bordas)
    return bordas

# --- Criando Objetos do Jogo ---
bolas = []
bola_branca_corpo, bola_branca_forma = criar_bola((largura / 4, altura / 2), raio_bola, 1, BRANCO)
bolas.append(bola_branca_corpo)
bola_um_corpo, bola_um_forma = criar_bola((largura / 2, altura / 2), raio_bola, 1, AMARELO)
bolas.append(bola_um_corpo)
bola_dois_corpo, bola_dois_forma = criar_bola((largura / 2 + 50, altura / 2 + 50), raio_bola, 1, AZUL)
bolas.append(bola_dois_corpo)

# Cria as bordas da mesa
bordas_da_mesa = criar_mesa()

# --- Variáveis de Jogo ---
mouse_pressionado = False
pos_inicial_clique = None
pos_final_arraste = None

# Loop principal do jogo
rodando = True
clock = pygame.time.Clock()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse_pressionado = True
            pos_inicial_clique = pygame.Vector2(evento.pos)
            pos_final_arraste = pygame.Vector2(evento.pos)
        
        elif evento.type == pygame.MOUSEMOTION and mouse_pressionado:
            pos_final_arraste = pygame.Vector2(evento.pos)
            
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            mouse_pressionado = False
            
            vetor_arrasto = pos_final_arraste - pos_inicial_clique
            forca_tacada = vetor_arrasto.length() * 10  # Força do taco

            direcao_tacada = -vetor_arrasto
            if direcao_tacada.length() > 0:
                direcao_tacada.normalize_ip()

            # Converte o vetor do Pygame para uma tupla antes de usar no Pymunk
            impulso_para_aplicar = direcao_tacada * forca_tacada
            impulso_para_aplicar = (impulso_para_aplicar.x, impulso_para_aplicar.y)

            # Aplica um impulso ao corpo da bola
            bola_branca_corpo.apply_impulse_at_local_point(impulso_para_aplicar, (0, 0))

            pos_inicial_clique = None

    # --- Desenhar na Tela ---
    tela.fill(VERDE)

    # Usa o Pymunk para desenhar todos os corpos e formas no espaço
    espaco.debug_draw(draw_options)

    # Desenhar o taco
    if mouse_pressionado and pos_inicial_clique is not None:
        pygame.draw.line(tela, MARROM, pos_inicial_clique, pos_final_arraste, 5)

    # Atualiza a física do Pymunk a cada frame
    espaco.step(1 / 60.0) # O 1/60.0 garante 60 quadros por segundo

    pygame.display.flip()
    clock.tick(60)

pygame.quit()