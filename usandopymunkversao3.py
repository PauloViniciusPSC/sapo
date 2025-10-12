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

# Cores das bolas sólidas
AMARELO_SOLIDO = (255, 236, 63, 255)
AZUL_SOLIDO = (0, 74, 173, 255)
VERMELHO_SOLIDO = (255, 0, 0, 255)
ROXO_SOLIDO = (214, 52, 235, 255)
LARANJA_SOLIDO = (255, 162, 3, 255)
VERDE_SOLIDO = (0, 191, 99, 255)
VINHO_SOLIDO = (139, 0, 0, 255)

# Cores das bolas listradas
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
#variaveis relacionadas às massas das bolas 
#o peso médio das bolas é de 140g e o peso da bola branca é de 156g
#o pymunk trabalha com proporções então 156/140 = 1.11 essa será a massa da bola branca a ser utilizada
massa_bola_branca = 1.15
massa_bolas_coloridas = 1.0
#essa variavel existe devido ao uso da biblioteca pymunk. 
forca_maxima_tacada = 2000#evita que a bola a bola branca "saia" da mesa,
comprimento_taco = 200
larogura_taco = 4 

#variaveis de estado do jogo
ESTADO_JOGO = "ESPERANDO_JOGADA" 
taco_corpo = None
taco_forma = None
pos_inicial_clique_esquerdo = None
linha_mira = []



# --- Configuração do Pymunk ---
espaco = pymunk.Space()
espaco.gravity = (0, 0)
espaco.damping = 0.75 #constante de atrito
draw_options = pymunk.pygame_util.DrawOptions(tela)


# --- Funções para Criar Objetos ---
def criar_bola(posicao, raio, massa, cor):
    corpo_bola = pymunk.Body(massa, pymunk.moment_for_circle(massa, 0, raio))
    corpo_bola.position = posicao
    forma_bola = pymunk.Circle(corpo_bola, raio)
    forma_bola.elasticity = 0.85
    forma_bola.friction = 0.99
    forma_bola.color = cor
    
    espaco.add(corpo_bola, forma_bola)
    return corpo_bola, forma_bola

def criar_mesa():
    # Coordenadas dos buracos para criar as bordas corretamente
    buraco_raio_colisao = raio_do_buraco - 5
    
    # Bordas superior e inferior (segmentos com buracos)
    bordas_sup = [
        pymunk.Segment(espaco.static_body, (margem_da_mesa + buraco_raio_colisao, margem_da_mesa), 
                       (largura/2 - buraco_raio_colisao, margem_da_mesa), 10),
        pymunk.Segment(espaco.static_body, (largura/2 + buraco_raio_colisao, margem_da_mesa), 
                       (largura - margem_da_mesa - buraco_raio_colisao, margem_da_mesa), 10)
    ]
    bordas_inf = [
        pymunk.Segment(espaco.static_body, (margem_da_mesa + buraco_raio_colisao, altura - margem_da_mesa), 
                       (largura/2 - buraco_raio_colisao, altura - margem_da_mesa), 10),
        pymunk.Segment(espaco.static_body, (largura/2 + buraco_raio_colisao, altura - margem_da_mesa), 
                       (largura - margem_da_mesa - buraco_raio_colisao, altura - margem_da_mesa), 10)
    ]

    # Bordas laterais (segmentos com buracos)
    bordas_esq = [
        pymunk.Segment(espaco.static_body, (margem_da_mesa, margem_da_mesa + buraco_raio_colisao), 
                       (margem_da_mesa, altura/2 - buraco_raio_colisao), 10),
        pymunk.Segment(espaco.static_body, (margem_da_mesa, altura/2 + buraco_raio_colisao), 
                       (margem_da_mesa, altura - margem_da_mesa - buraco_raio_colisao), 10)
    ]
    bordas_dir = [
        pymunk.Segment(espaco.static_body, (largura - margem_da_mesa, margem_da_mesa + buraco_raio_colisao), 
                       (largura - margem_da_mesa, altura/2 - buraco_raio_colisao), 10),
        pymunk.Segment(espaco.static_body, (largura - margem_da_mesa, altura/2 + buraco_raio_colisao), 
                       (largura - margem_da_mesa, altura - margem_da_mesa - buraco_raio_colisao), 10)
    ]

    bordas = bordas_sup + bordas_inf + bordas_esq + bordas_dir
    
    for borda in bordas:
        borda.elasticity = 0.9
        borda.color = cor_da_tabela
    
    espaco.add(*bordas)
    return bordas

def criar_taco():
    '''
    Essa função serve para criar o taco no jogo
    '''
    #Primeiro instancia o objeto como um corpo(Body)
    corpo = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    #agora a gente cria a forma do dito cujo
    forma = pymunk.Poly.create_box(corpo,(comprimento_taco,larogura_taco))
    #agora definimos a cor dessa desgraça
    forma.color = COR_TACK
    espaco.add(corpo,forma)
    #por fim retorna o corpo do taco junto da sua forma, que nesse caso age como uma sprite
    return corpo,forma

def desenhar_linha_tracejada(superficie, cor, inicio, fim, largura=1, espaco_traco=5):
    """Essa funcao vai servir para desenhar a linha de mira..."""
    ponto_inicio = pygame.math.Vector2(inicio)
    ponto_fim = pygame.math.Vector2(fim)

    vetor = ponto_fim - ponto_inicio
    comprimento = vetor.length
    
    if comprimento < espaco_traco:
        return
        
    direcao = vetor.normalize()
    
    pos_atual = ponto_inicio
    distancia_percorrida = 0
    
    while distancia_percorrida < comprimento:
        fim_traco = pos_atual + direcao * espaco_traco
        
        if (fim_traco - ponto_inicio).length > comprimento:
            fim_traco = ponto_fim

        pygame.draw.line(superficie, cor, pos_atual, fim_traco, largura)
        
        pos_atual = fim_traco + direcao * espaco_traco
        distancia_percorrida = (pos_atual - ponto_inicio).length



# --- Criando Objetos do Jogo ---

# Lista de cores para as 15 bolas de sinuca, na ordem do triângulo
CORES_DO_TRIANGULO = [
    AMARELO_SOLIDO,
    AZUL_SOLIDO, VERMELHO_SOLIDO,
    VERDE_SOLIDO, PRETO, ROXO_SOLIDO,
    LARANJA_SOLIDO, VINHO_SOLIDO, AZUL_LISTRADO, AMARELO_LISTRADO,
    VERMELHO_LISTRADO, ROXO_LISTRADO, VERDE_LISTRADO, LARANJA_LISTRADO, VINHO_LISTRADO
]

# Configuração da posição inicial para a formação do triângulo
distancia_entre_bolas = raio_bola * 2 + 2
pos_inicial_triangulo = pygame.Vector2(largura * 0.7, altura / 2)

# Listas para armazenar os corpos e as formas das bolas
bolas_corpos = []
bolas_formas = []

# Criar a bola branca
bola_branca_corpo, bola_branca_forma = criar_bola((largura * 0.3, altura / 2), raio_bola, massa_bola_branca, BRANCO)
bolas_corpos.append(bola_branca_corpo)
bolas_formas.append(bola_branca_forma)

# Criar as 15 bolas do triângulo
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

# Cria as bordas da mesa
bordas_da_mesa = criar_mesa()

# --- Variáveis de Jogo ---
mouse_pressionado = False
pos_inicial_clique = None
pos_final_arraste = None

# Loop principal do jogo
rodando = True
clock = pygame.time.Clock()

# Loop principal do jogo
rodando = True
clock = pygame.time.Clock()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        # --- LÓGICA DO CLIQUE DIREITO ---
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 3: # Botão direito
            if ESTADO_JOGO == "ESPERANDO_JOGADA":
                # Cria o taco se ele não existir
                if taco_corpo is None:
                    taco_corpo, taco_forma = criar_taco()
                
                # Posiciona o taco e muda o estado
                ESTADO_JOGO = "POSICIONANDO_TACO"

        # --- LÓGICA DO CLIQUE ESQUERDO ---
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1: # Botão esquerdo
            if ESTADO_JOGO == "POSICIONANDO_TACO":
                # Inicia o processo de puxar o taco
                pos_inicial_clique_esquerdo = pygame.Vector2(evento.pos)
                ESTADO_JOGO = "PUXANDO_TACO"

        # --- LÓGICA DE SOLTAR O CLIQUE ESQUERDO (A TACADA) ---
        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            if ESTADO_JOGO == "PUXANDO_TACO":
                # Calcula a força baseada na distância que o taco foi puxado
                dist_puxada = (taco_corpo.position - bola_branca_corpo.position).length
                forca = dist_puxada * 30 # Fator de força para a tacada

                # Aplica um impulso FORTE na bola branca, na direção do taco
                
                #------------------------------
                # ...
                angulo = taco_corpo.angle
                # Cria o vetor de direção base
                vetor_impulso = pygame.math.Vector2(1, 0)
                # Rotaciona o vetor (a função retorna um novo vetor rotacionado)
                vetor_impulso = vetor_impulso.rotate(-math.degrees(angulo)) # rotate usa graus

                # Calcula o impulso final
                impulso = forca * vetor_impulso
                bola_branca_corpo.apply_impulse_at_local_point((impulso.x, impulso.y))
                # ...
                #------------------------------




                # Reseta o estado do jogo
                ESTADO_JOGO = "ESPERANDO_JOGADA"
                pos_inicial_clique_esquerdo = None
                # O taco pode ser removido ou apenas escondido. Por enquanto, vamos deixá-lo.
                # Se quiser remover:
                # espaco.remove(taco_corpo, taco_forma)
                # taco_corpo, taco_forma = None, None

    # --- ATUALIZAÇÕES FORA DO LOOP DE EVENTOS (ACONTECEM A TODO QUADRO) ---
    
    # Se estiver posicionando o taco, ele segue o mouse
    if ESTADO_JOGO == "POSICIONANDO_TACO":
        mouse_pos = pygame.mouse.get_pos()
        vetor_direcao = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(bola_branca_corpo.position)
        angulo_taco = vetor_direcao.angle_to(pygame.math.Vector2(1, 0)) * (math.pi / 180.0) # Converte para radianos
        
        taco_corpo.angle = -angulo_taco
        
        # Posiciona o taco um pouco atrás da bola branca
        offset_taco = vetor_direcao.normalize() * -(raio_bola + comprimento_taco / 2)
        taco_corpo.position = bola_branca_corpo.position + offset_taco

    # Se estiver puxando o taco para trás
    if ESTADO_JOGO == "PUXANDO_TACO":
        mouse_pos = pygame.mouse.get_pos()
        vetor_arrasto = pygame.Vector2(mouse_pos) - pos_inicial_clique_esquerdo
        
        # Projeta o arrasto na direção do taco para limitar o movimento
        angulo_taco_rad = -taco_corpo.angle
        direcao_taco = pygame.math.Vector2(1, 0).rotate_rad(angulo_taco_rad)
        distancia_puxada = vetor_arrasto.dot(direcao_taco)
        
        # Limita o quanto pode puxar para trás
        distancia_puxada = max(0, distancia_puxada)
        
        # Posição base do taco (tocando a bola)
        offset_base = direcao_taco * -(raio_bola + comprimento_taco / 2)
        pos_base = bola_branca_corpo.position + offset_base
        
        # Nova posição puxada
        taco_corpo.position = pos_base + direcao_taco * -distancia_puxada

        # Calcula a linha de mira
        ponto_final_mira = bola_branca_corpo.position + direcao_taco * 1000
        linha_mira = [bola_branca_corpo.position, ponto_final_mira]
    else:
        linha_mira = []


    # --- Desenhar na Tela ---
    tela.fill(VERDE)

    # ... (seu código que desenha as bordas)

    # Desenha as bolas sem as bordas pretas
    for forma in bolas_formas:
        pos = (int(forma.body.position.x), int(forma.body.position.y))
        raio = int(forma.radius)
        cor = forma.color
        pygame.draw.circle(tela, cor, pos, raio)

    # Desenha o taco se ele existir
    if taco_corpo:
        # Pega os vértices do polígono do taco
        vertices = [v.rotated(taco_corpo.angle) + taco_corpo.position for v in taco_forma.get_vertices()]
        pygame.draw.polygon(tela, taco_forma.color, vertices)

    # Desenha a linha de mira
    if linha_mira:
        desenhar_linha_tracejada(tela, BRANCO, linha_mira[0], linha_mira[1])


    # Atualiza a física do Pymunk
    espaco.step(1 / 60.0)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()