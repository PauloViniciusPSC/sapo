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
COR_TACK = (139, 69, 19, 255)
AMARELO_SOLIDO = (255, 236, 63, 255)
AZUL_SOLIDO = (0, 74, 173, 255)
VERMELHO_SOLIDO = (255, 0, 0, 255)
ROXO_SOLIDO = (214, 52, 235, 255)
LARANJA_SOLIDO = (255, 162, 3, 255)
VERDE_SOLIDO = (0, 191, 99, 255)
VINHO_SOLIDO = (139, 0, 0, 255)
AMARELO_LISTRADO = (255, 236, 63, 255)
AZUL_LISTRADO = (0, 74, 173, 255)
VERMELHO_LISTRADO = (255, 0, 0, 255)
ROXO_LISTRADO = (214, 52, 235, 255)
LARANJA_LISTRADO = (255, 162, 3, 255)
VERDE_LISTRADO = (0, 191, 99, 255)
VINHO_LISTRADO = (139, 0, 0, 255)
cor_da_tabela = (193, 255, 114, 255)

# --- Variáveis de Jogo ---
margem_da_mesa = 50
raio_bola = 15
raio_do_buraco = 17
massa_bola_branca = 1.15
massa_bolas_coloridas = 1.0
forca_maxima_tacada = 2000

# --- Constantes do Taco ---
comprimento_taco = 200
largura_taco = 5 # CORREÇÃO de typo: larogura -> largura

# --- Variáveis de Estado do Jogo ---
ESTADO_JOGO = "ESPERANDO_JOGADA"
taco_corpo = None
taco_forma = None
pos_inicial_clique_esquerdo = None
linha_mira = [] # CORREÇÃO de typo: linha_minha -> linha_mira

# --- Configuração do Pymunk ---
espaco = pymunk.Space()
espaco.gravity = (0, 0)
espaco.damping = 0.95 # Valor de exemplo, ajuste conforme o 'feeling' desejado
draw_options = pymunk.pygame_util.DrawOptions(tela)

# --- Funções para Criar Objetos ---
def criar_bola(posicao, raio, massa, cor):
    corpo_bola = pymunk.Body(massa, pymunk.moment_for_circle(massa, 0, raio))
    corpo_bola.position = posicao
    forma_bola = pymunk.Circle(corpo_bola, raio)
    forma_bola.elasticity = 0.85
    forma_bola.friction = 0.8
    forma_bola.color = cor
    espaco.add(corpo_bola, forma_bola)
    return corpo_bola, forma_bola

def criar_mesa():
    buraco_raio_colisao = raio_do_buraco - 5
    bordas_sup = [
        pymunk.Segment(espaco.static_body, (margem_da_mesa + buraco_raio_colisao, margem_da_mesa), (largura/2 - buraco_raio_colisao, margem_da_mesa), 10),
        pymunk.Segment(espaco.static_body, (largura/2 + buraco_raio_colisao, margem_da_mesa), (largura - margem_da_mesa - buraco_raio_colisao, margem_da_mesa), 10)
    ]
    bordas_inf = [
        pymunk.Segment(espaco.static_body, (margem_da_mesa + buraco_raio_colisao, altura - margem_da_mesa), (largura/2 - buraco_raio_colisao, altura - margem_da_mesa), 10),
        pymunk.Segment(espaco.static_body, (largura/2 + buraco_raio_colisao, altura - margem_da_mesa), (largura - margem_da_mesa - buraco_raio_colisao, altura - margem_da_mesa), 10)
    ]
    bordas_esq = [
        pymunk.Segment(espaco.static_body, (margem_da_mesa, margem_da_mesa + buraco_raio_colisao), (margem_da_mesa, altura - margem_da_mesa - buraco_raio_colisao), 10)
    ]
    bordas_dir = [
        pymunk.Segment(espaco.static_body, (largura - margem_da_mesa, margem_da_mesa + buraco_raio_colisao), (largura - margem_da_mesa, altura - margem_da_mesa - buraco_raio_colisao), 10)
    ]
    bordas = bordas_sup + bordas_inf + bordas_esq + bordas_dir
    for borda in bordas:
        borda.elasticity = 0.9
        borda.color = cor_da_tabela
    espaco.add(*bordas)
    return bordas

def criar_taco():
    corpo = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    forma = pymunk.Poly.create_box(corpo, (comprimento_taco, largura_taco))
    forma.color = COR_TACK
    espaco.add(corpo, forma)
    return corpo, forma

def desenhar_linha_tracejada(superficie, cor, inicio, fim, largura=1, espaco_traco=5):
    ponto_inicio = pygame.math.Vector2(inicio)
    ponto_fim = pygame.math.Vector2(fim)
    vetor = ponto_fim - ponto_inicio
    
    # CORREÇÃO DEFINITIVA: .length() é um método e PRECISA de parênteses.
    comprimento = vetor.length()
    
    if comprimento < espaco_traco:
        return
        
    # CORREÇÃO DEFINITIVA: .normalize() também é um método.
    direcao = vetor.normalize()
    
    pos_atual = ponto_inicio
    distancia_percorrida = 0
    while distancia_percorrida < comprimento:
        fim_traco = pos_atual + direcao * espaco_traco
        if (fim_traco - ponto_inicio).length() > comprimento:
            fim_traco = ponto_fim
        pygame.draw.line(superficie, cor, pos_atual, fim_traco, largura)
        pos_atual = fim_traco + direcao * espaco_traco
        distancia_percorrida = (pos_atual - ponto_inicio).length()

# --- Criando Objetos do Jogo ---
CORES_DO_TRIANGULO = [AMARELO_SOLIDO, AZUL_SOLIDO, VERMELHO_SOLIDO, VERDE_SOLIDO, PRETO, ROXO_SOLIDO, LARANJA_SOLIDO, VINHO_SOLIDO, AZUL_LISTRADO, AMARELO_LISTRADO, VERMELHO_LISTRADO, ROXO_LISTRADO, VERDE_LISTRADO, LARANJA_LISTRADO, VINHO_LISTRADO]
distancia_entre_bolas = raio_bola * 2 + 2
pos_inicial_triangulo = pygame.Vector2(largura * 0.7, altura / 2)
bolas_corpos = []
bolas_formas = []

bola_branca_corpo, bola_branca_forma = criar_bola((largura * 0.3, altura / 2), raio_bola, massa_bola_branca, BRANCO)
bolas_corpos.append(bola_branca_corpo)
bolas_formas.append(bola_branca_forma)

indice_cor = 0
for i in range(5):
    num_bolas_na_linha = i + 1
    y_offset = (num_bolas_na_linha - 1) * distancia_entre_bolas / 2
    for j in range(num_bolas_na_linha):
        x_pos = pos_inicial_triangulo.x + i * (distancia_entre_bolas * math.sqrt(3) / 2)
        y_pos = pos_inicial_triangulo.y - y_offset + j * distancia_entre_bolas
        corpo, forma = criar_bola((x_pos, y_pos), raio_bola, massa_bolas_coloridas, CORES_DO_TRIANGULO[indice_cor])
        bolas_corpos.append(corpo)
        bolas_formas.append(forma)
        indice_cor += 1

bordas_da_mesa = criar_mesa()
rodando = True
clock = pygame.time.Clock()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 3:
            if ESTADO_JOGO == "ESPERANDO_JOGADA":
                if taco_corpo is None:
                    taco_corpo, taco_forma = criar_taco()
                ESTADO_JOGO = "POSICIONANDO_TACO"

        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            if ESTADO_JOGO == "POSICIONANDO_TACO":
                pos_inicial_clique_esquerdo = pygame.Vector2(evento.pos)
                ESTADO_JOGO = "PUXANDO_TACO"

        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if ESTADO_JOGO == "PUXANDO_TACO":
                dist_puxada = (pygame.Vector2(taco_corpo.position) - pygame.Vector2(bola_branca_corpo.position)).length()
                forca = dist_puxada * 30
                if forca > forca_maxima_tacada:
                    forca = forca_maxima_tacada




                angulo_rad = taco_corpo.angle
                # CORREÇÃO AQUI: Criar o vetor e rotacioná-lo corretamente.
                vetor_impulso = pygame.math.Vector2(1, 0)
                vetor_impulso = vetor_impulso.rotate(-math.degrees(angulo_rad))
                
                impulso_final = forca * vetor_impulso
                bola_branca_corpo.apply_impulse_at_local_point((impulso_final.x, impulso_final.y))

                ESTADO_JOGO = "ESPERANDO_JOGADA"
                pos_inicial_clique_esquerdo = None

    if ESTADO_JOGO == "POSICIONANDO_TACO":
        mouse_pos = pygame.mouse.get_pos()
        vetor_direcao = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(bola_branca_corpo.position)
        angulo_taco_rad = math.atan2(-vetor_direcao.y, vetor_direcao.x)
        taco_corpo.angle = angulo_taco_rad
        
        # CORREÇÃO AQUI: .normalize() precisa de parênteses.
        offset_taco = vetor_direcao.normalize() * -(raio_bola + comprimento_taco / 2)
        taco_corpo.position = bola_branca_corpo.position + offset_taco

    if ESTADO_JOGO == "PUXANDO_TACO":
        mouse_pos = pygame.mouse.get_pos()
        vetor_arrasto = pygame.Vector2(mouse_pos) - pos_inicial_clique_esquerdo
        
        angulo_taco_rad = taco_corpo.angle
        direcao_taco = pygame.math.Vector2(1, 0).rotate(-math.degrees(angulo_taco_rad))
        distancia_puxada = vetor_arrasto.dot(direcao_taco)
        distancia_puxada = max(0, distancia_puxada)
        
        offset_base = direcao_taco * -(raio_bola + comprimento_taco / 2)
        pos_base = bola_branca_corpo.position + offset_base
        
        taco_corpo.position = pos_base + direcao_taco * -distancia_puxada

        ponto_final_mira = bola_branca_corpo.position + direcao_taco * 1000
        linha_mira = [bola_branca_corpo.position, ponto_final_mira]
    else:
        linha_mira = []

    tela.fill(VERDE)
    for borda in bordas_da_mesa:
        p1 = borda.a
        p2 = borda.b
        pygame.draw.line(tela, borda.color, p1, p2, 20)
        
    for forma in bolas_formas:
        pos = (int(forma.body.position.x), int(forma.body.position.y))
        pygame.draw.circle(tela, forma.color, pos, raio_bola)

    if taco_corpo and ESTADO_JOGO != "ESPERANDO_JOGADA":
        vertices = [v.rotated(taco_corpo.angle) + taco_corpo.position for v in taco_forma.get_vertices()]
        pygame.draw.polygon(tela, taco_forma.color, vertices)

    if linha_mira:
        desenhar_linha_tracejada(tela, BRANCO, linha_mira[0], linha_mira[1])

    espaco.step(1 / 60.0)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()