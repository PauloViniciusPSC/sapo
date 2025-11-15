#bibliotecas
import pygame
import pymunk
import pymunk.pygame_util
import math
import logica_jogo
# import numpy # Removido - não estava sendo usado

# Inicialização do Pygame
pygame.init()

#criando um objeto de fonte 
try:
    numero_font = pygame.font.SysFont('Arial',14, bold = True)
except: 
    numero_font = pygame.font.Font(None,18)



#Configurações da Janela
largura, altura = 1100, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Simulacao com Pymunk")



# --- NOVO: Variáveis para Regras do Jogo (Pares/Ímpares) ---
turno_jogador = 1             # Começa com o Jogador 1
bolas_atribuidas = False      # Os grupos (pares/ímpares) ainda não foram definidos
jogador1_grupo = None         # Pode ser "impares", "pares" ou None
jogador2_grupo = None         # Pode ser "impares", "pares" ou None
falta_na_jogada = False       # Indica se ocorreu uma falta na jogada atual
primeiro_contato = None       # Guarda o número da primeira bola tocada pela branca
bolas_encacapadas_na_jogada = [] # Lista de números das bolas encaçapadas na jogada atual
primeira_tacada_feita = False # Indica que o estouro ainda não foi dado 
# Listas para rastrear quais bolas estão EM JOGO (excluindo a bola 8)
bolas_impares_em_jogo = [3, 5, 7, 9, 11, 13, 15]# Exclui a 1
bolas_pares_em_jogo = [2, 4, 6,8, 10, 12, 14] 
bola_um_em_jogo = False
vencedor = None #marca o vencedor da partida. Se foi o jogador 1 ou o jogador 2. 
# ---------------------------------------------------------

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
cor_da_cacapa = (192,192,192,255)
# --- ADICIONE ESTAS DUAS LINHAS ---
COR_TACO_JOGADOR1 = (255, 0, 0, 255) # Vermelho
COR_TACO_JOGADOR2 = (0, 0, 255, 255) # Azul
# ------------------------------------
# Colocando ordem nas cores 
cor_por_numero = {
    1: AMARELO_LISTRADO,
    2: AZUL_LISTRADO,
    3: VERMELHO_LISTRADO,
    4: ROXO_LISTRADO,
    5: LARANJA_LISTRADO,
    6: VERDE_LISTRADO,
    7: VINHO_LISTRADO,
    8: PRETO,
    9: AMARELO_LISTRADO,
    10: AZUL_LISTRADO,
    11: VERMELHO_LISTRADO,
    12: ROXO_LISTRADO,
    13: LARANJA_LISTRADO,
    14: VERDE_LISTRADO,
    15: VINHO_LISTRADO
    }
# --- Variáveis de Jogo ---
margem_da_mesa = 25
raio_bola = 15
raio_do_buraco = 18
massa_bola_branca = 1.15
massa_bolas_coloridas = 1.0
forca_maxima_tacada = 1000
margem_dos_buracos = 33
margem_das_tabelas = 40
inicio_tabela_lateral = 26
limiar_abertura_bocas_fundo = 30
limiar_abertura_boca_meio = 4

# Posições dos buracos (LINHA CORRIGIDA E FORMATADA):
posicoes_buracos = [
    (margem_da_mesa + raio_do_buraco, margem_da_mesa + raio_do_buraco), # Canto Superior Esquerdo
    (largura/2, margem_da_mesa + raio_do_buraco), # Meio Superior
    (largura - margem_da_mesa - raio_do_buraco, margem_da_mesa + raio_do_buraco), # Canto Superior Direito
    (margem_da_mesa + raio_do_buraco, altura - raio_do_buraco - margem_da_mesa), # Canto Inferior Esquerdo
    (largura/2, altura - margem_da_mesa - raio_do_buraco), # Meio Inferior
    (largura - raio_do_buraco - margem_da_mesa, altura - raio_do_buraco - margem_da_mesa) # Canto Inferior Direito
]

#Posicoes das tabelas:
tabela_superior_esquerda =  [
    (margem_da_mesa+26,margem_da_mesa),#P1
    (largura/2 - raio_do_buraco,margem_da_mesa), #P2
    (largura/2-raio_do_buraco-4,margem_da_mesa+margem_das_tabelas), #P3
    (margem_da_mesa+margem_das_tabelas+30, margem_da_mesa+margem_das_tabelas)#P4
]
tabela_superior_direita =   [
    (largura/2+raio_do_buraco,margem_da_mesa),#P1
    (largura - margem_da_mesa - 26, margem_da_mesa),#P2
    (largura - margem_da_mesa-margem_das_tabelas-30,margem_da_mesa+margem_das_tabelas),#P3
    (largura/2+raio_do_buraco+4,margem_da_mesa+margem_das_tabelas)#P4
]
tabela_lateral_esquerda =   [
    (margem_da_mesa,margem_da_mesa+26),#P1
    (margem_da_mesa+margem_das_tabelas,margem_da_mesa+margem_das_tabelas+30),#P2
    (margem_da_mesa+margem_das_tabelas,altura-margem_da_mesa-margem_das_tabelas-30),#P3
    (margem_da_mesa,altura - margem_da_mesa-26)#P4
]
tabela_lateral_direita =    [
    (largura - margem_da_mesa,margem_da_mesa+26),#P1
    (largura - margem_da_mesa,altura - margem_da_mesa - 26),#P2
    (largura - margem_da_mesa-margem_das_tabelas,altura -margem_da_mesa - margem_das_tabelas -30),#P3
    (largura-margem_da_mesa-margem_das_tabelas,margem_da_mesa+margem_das_tabelas+30)#P4
]
tabela_inferior_esquerda =  [
    (margem_da_mesa+26,altura - margem_da_mesa),#P1
    (largura/2 - raio_do_buraco,altura-margem_da_mesa),#P2
    (largura/2 - raio_do_buraco-4,altura - margem_da_mesa-margem_das_tabelas),#P3
    (margem_da_mesa+margem_das_tabelas+30,altura - margem_da_mesa-margem_das_tabelas)#P4
]
tabela_inferior_direita = [
    (largura/2 +raio_do_buraco,altura-margem_da_mesa),#P1
    (largura/2 + raio_do_buraco + 4, altura - margem_da_mesa -margem_das_tabelas), #P2
    (largura-margem_da_mesa-margem_das_tabelas-30,altura-margem_da_mesa-margem_das_tabelas), #P3
    (largura-margem_da_mesa-26,altura-margem_da_mesa)#P4
]

lista_tabelas = [
    tabela_superior_esquerda,
    tabela_lateral_esquerda,
    tabela_superior_direita,
    tabela_lateral_direita,
    tabela_inferior_esquerda,
    tabela_inferior_direita
]

#Detalhe das caçapas
cacapa_superior_esquerda = [(0,0),
    (margem_da_mesa+8,0),
    (margem_da_mesa+margem_das_tabelas-5,margem_da_mesa),
    (margem_da_mesa,margem_da_mesa+margem_das_tabelas-5),
    (0,margem_da_mesa+8)
]
cacapa_meio_superior = [
    (largura/2 - raio_do_buraco - 14,0),
    (largura/2 + raio_do_buraco + 14,0),
    (largura/2 + raio_do_buraco, margem_da_mesa + raio_do_buraco),
    (largura/2 - raio_do_buraco, margem_da_mesa + raio_do_buraco)
]
cacapa_superior_direita = [
    (largura - margem_da_mesa - 8, 0),
    (largura,0),
    (largura,margem_da_mesa +8),
    (largura - margem_da_mesa,margem_da_mesa+margem_das_tabelas -5),
    (largura - margem_da_mesa -margem_das_tabelas+5,margem_da_mesa)
]
cacapa_inferior_direita = [
    (largura,altura - margem_da_mesa-8),
    (largura,altura),
    (largura - margem_da_mesa -8, altura),
    (largura-margem_da_mesa-margem_das_tabelas+5,altura -margem_da_mesa),
    (largura -margem_da_mesa, altura - margem_da_mesa -margem_das_tabelas +5)
]
cacapa_meio_inferior = [
    (largura/2 - raio_do_buraco - 14, altura),
    (largura/2 + raio_do_buraco + 14, altura),
    (largura/2 + raio_do_buraco, altura - margem_da_mesa-raio_do_buraco),
    (largura/2 - raio_do_buraco, altura - margem_da_mesa-raio_do_buraco)
]
cacapa_inferior_esquerda = [
    (0,altura),
    (0,altura-margem_da_mesa-8),
    (margem_da_mesa,altura -margem_da_mesa-margem_das_tabelas+5),
    (margem_da_mesa+margem_das_tabelas-5,altura-margem_da_mesa),
    (margem_da_mesa+8,altura)
]
lista_cacapas = [
    cacapa_superior_esquerda,
    cacapa_meio_superior,
    cacapa_superior_direita,
    cacapa_inferior_direita,
    cacapa_meio_inferior,
    cacapa_inferior_esquerda
]

# Variáveis do Taco
comprimento_taco = 250
largura_taco = 5

# Variáveis de Estado de Jogo
ESTADO_JOGO = "ESPERANDO_JOGADA" # Os outros estados são: MIRANDO, PUXANDO O TACO, BOLAS_EM_MOVIMENTO. 
taco_corpo = None
taco_forma = None
pos_inicial_clique_esquerdo = None
pos_bola_branca_pre_tacada = None
linha_mira = []
vetor_mira_travado = None # Vetor de direção salvo para a tacada

#variaveis para marcaçao de colisoes:
#basicamente estamos só definindo uma marcacao para diferenciar as bolas coloridas da bola branca.
col_tipo_bola_branca = 1 
col_tipo_bola_colorida = 2

# Configurações do Pymunk
espaco = pymunk.Space()
espaco.gravity = (0, 0)
espaco.damping = 0.60
draw_options = pymunk.pygame_util.DrawOptions(tela)

# Seção de Funções
def criar_bola(posicao, raio, massa, cor, numero = None):
    '''
    Essa função é responsável por criar as bolas no jogo, o que ela faz realmente é criar uma forma e um corpo, a forma é o desenho, ou seja, o que você vê visualmente. 
    numero é passado com valor padrao None para facilitar a parte da criação da bola branca. 
    '''
    corpo_bola = pymunk.Body(massa, pymunk.moment_for_circle(massa, 0, raio))
    corpo_bola.position = posicao
    forma_bola = pymunk.Circle(corpo_bola, raio)
    forma_bola.elasticity = 0.85
    forma_bola.friction = 0.8
    forma_bola.color = cor
    espaco.add(corpo_bola, forma_bola)
    forma_bola.numero = numero
    if numero is not None:
        #o que estamos fazendo é colocar um dicionario dentro de outro dicionario
        bolas_por_numero[numero]= {'corpo':corpo_bola, 'forma': forma_bola}

    return corpo_bola, forma_bola

def criar_tabelas(tabelas_tabelas_tabelas):
    """
    Cria as 6 tabelas como poligonos estáticos que correspondem
    aos poligonos que são desenhados na tela.
    """
    for tabela in tabelas_tabelas_tabelas:
        forma_tabela = pymunk.Poly(espaco.static_body,tabela)
        forma_tabela.elasticity = 0.9
        forma_tabela.friction = 0.8
        forma_tabela.color = cor_da_tabela
        espaco.add(forma_tabela)

def criar_taco():
    """
    Esta função é usada para criar o taco no jogo
    """
    corpo = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    forma = pymunk.Poly.create_box(corpo, (comprimento_taco, largura_taco))
    forma.sensor = True # transforma o taco em um "sensor"
    espaco.add(corpo, forma)
    return corpo, forma

def desenhar_linha_tracejada(superficie, cor, inicio, fim, largura=1, espaco_traco=5):
    ponto_inicio = pygame.math.Vector2(inicio)
    ponto_fim = pygame.math.Vector2(fim)
    vetor = ponto_fim - ponto_inicio
    
    comprimento = vetor.length()
    
    if comprimento < espaco_traco:
        return
        
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

def todas_bolas_paradas(limiar_velocidade_sq = 10):
    """
    Essa função serve para verificar se todas as bolas no jogo estão paradas. 
    """
    for corpo in bolas_corpos:
        #pega a velocidade linear da bola ao quadrado:
        vel_sq = corpo.velocity.length_squared
        #pega a velocidade angular (rotação) eu não achei que fosse ter que ter isso no meu codigo mas aparentemente é padrão da biblioteca que estamos usando nesse codigo
        ang_vel = abs(corpo.angular_velocity)

        #esse condicional vai verificar se existe alguma bola que ainda esteja girando ou se movendo, e vai retornar false caso haja alguma 
        if vel_sq > limiar_velocidade_sq or ang_vel > 0.5:
            return False 
    # se o laço for terminar e nenhuma estiver se movendo a função retornara True cachorro 
    return True 



# --- Criando Objetos do Jogo ---
CORES_DO_TRIANGULO = [AMARELO_SOLIDO, AZUL_SOLIDO, VERMELHO_SOLIDO, VERDE_SOLIDO, PRETO, ROXO_SOLIDO, LARANJA_SOLIDO, VINHO_SOLIDO, AZUL_LISTRADO, AMARELO_LISTRADO, VERMELHO_LISTRADO, ROXO_LISTRADO, VERDE_LISTRADO, LARANJA_LISTRADO, VINHO_LISTRADO]
distancia_entre_bolas = raio_bola * 2 + 2
pos_inicial_triangulo = pygame.Vector2(largura * 0.7, altura / 2)
bolas_por_numero = {}#é um dicionario que vai armazenar a bolas por numero 'numero': {'corpo': corpo, 'forma': forma}
bolas_corpos = []
bolas_formas = []

bola_branca_corpo, bola_branca_forma = criar_bola((largura * 0.3, altura / 2), raio_bola, massa_bola_branca, BRANCO)
bolas_corpos.append(bola_branca_corpo)
bolas_formas.append(bola_branca_forma)

# Criar as 15 bolas do triângulo
indice_cor = 0
# Criar as 14 bolas do triângulo (pulando a bola 1)
numero_bola_atual = 1 # Começa a contagem em 1
for i in range(5):
    num_bolas_na_linha = i + 1
    y_offset = (num_bolas_na_linha - 1) * distancia_entre_bolas / 2
    for j in range(num_bolas_na_linha):
        # --- SÓ CRIA SE NÃO FOR A BOLA 1 ---
        if numero_bola_atual != 1:
            x_pos = pos_inicial_triangulo.x + i * (distancia_entre_bolas * math.sqrt(3) / 2)
            y_pos = pos_inicial_triangulo.y - y_offset + j * distancia_entre_bolas

            # Pega a cor correta do dicionário usando o número da bola
            # Precisamos garantir que o número existe no dicionário (caso pulemos o 1)
            if numero_bola_atual in cor_por_numero:
                 cor_correta = cor_por_numero[numero_bola_atual]
            else:
                 cor_correta = PRETO # Cor padrão se o número não for encontrado

            # Cria a bola com a cor correta e o número
            corpo, forma = criar_bola((x_pos, y_pos), raio_bola, massa_bolas_coloridas, cor_correta, numero_bola_atual)

            bolas_corpos.append(corpo)
            bolas_formas.append(forma)
        # ------------------------------------

        # Incrementa o número INDEPENDENTEMENTE de ter criado a bola ou não
        numero_bola_atual += 1








#chama a função da criação das tabelas
criar_tabelas(lista_tabelas)

# Loop principal do jogo
rodando = True
clock = pygame.time.Clock()
while rodando:

    #O laço for a seguir serve para fazer o gerenciamento dos eventos no jogo

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        # 1. INICIAR A TACADA (Pressionar Botão Direito)
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 3 and ESTADO_JOGO == "ESPERANDO_JOGADA":
            if taco_corpo is None:
                taco_corpo, taco_forma = criar_taco()
                vetor_mira_travado = None # Garante que a mira antiga seja limpa

            ESTADO_JOGO = "MIRANDO"
           
        # 2. CANCELAR A TACADA (Soltar Botão Direito)
        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 3:
            if ESTADO_JOGO in ["MIRANDO", "PUXANDO_TACO"]:
                ESTADO_JOGO = "ESPERANDO_JOGADA"
                pos_inicial_clique_esquerdo = None
                linha_mira = []
                vetor_mira_travado = None

        #Se com o botao direito o usuario clica no botao esquerdo, ele tem então que puxar o taco, dessa forma quando ele arrastar o mouse e soltar o botão esquerdo do mouse novamente a tacada sera feita. Nesse momento a mira final é definida!
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and ESTADO_JOGO == "MIRANDO":
            #a gente pega a posicao do mouse aonde o usuario clicou com o botao esquerdo
            pos_inicial_clique_esquerdo = pygame.Vector2(pygame.mouse.get_pos())
            print(pos_inicial_clique_esquerdo)
            mouse_pos = pygame.mouse.get_pos()

            vetor_direcao = pygame.math.Vector2(pos_inicial_clique_esquerdo)-pygame.math.Vector2(bola_branca_corpo.position)

            '''
            if vetor_direcao.length() > 0:
                vetor_mira_travado = vetor_direcao.normalize()
            else:
                vetor_mira_travado = pygame.math.Vector2(0,1) # Padrão (para baixo)
            '''
            vetor_mira_travado = vetor_direcao.normalize()
            print(vetor_mira_travado)
            ESTADO_JOGO = "PUXANDO_TACO"

        # 4. Execução da tacada, ou seja quando o usuario solta o botão esquerdo do mouse
        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1 and ESTADO_JOGO == "PUXANDO_TACO":
            # calcula a posicao final do taco para calcular a distancia de deslocamento para que a força possa ser calculada           
            pos_final_arraste = pygame.Vector2(pygame.mouse.get_pos())
            vetor_arrasto = pos_final_arraste - pos_inicial_clique_esquerdo
            forca = abs(vetor_arrasto.length())* 9 # Fator de força

            if 'FORCA_MAXIMA_TACADA' in locals() and forca > forca_maxima_tacada:
                forca = forca_maxima_tacada
            '''
            # Usa o vetor da mira que foi salvo (lógica unificada)
            vetor_impulso = vetor_mira_travado
            impulso_final = forca * vetor_impulso

            bola_branca_corpo.apply_impulse_at_local_point((impulso_final.x, impulso_final.y))
            
            '''

            #daqui pra baixo é novo:
            vetor_impulso = vetor_mira_travado if vetor_mira_travado is not None else pygame.math.Vector2(1,0)
            impulso_final = pymunk.Vec2d(vetor_impulso.x * forca, vetor_impulso.y * forca)

            #adicionar um debug 
            # DEBUG: imprima para verificar consistência da direção e magnitude (opcional)
            print("impulso:", impulso_final, "vetor_mira_travado:", vetor_mira_travado, "forca:", forca)
            # a funcao apply_impulse_at_world_point funciona pq de fato o impulso vem de fora para a bola e não nasce na bola como estava sendo feito anteriormente
            bola_branca_corpo.apply_impulse_at_world_point(impulso_final, bola_branca_corpo.position)

            #agora temos que fazer o reposicionamento da bola 1 caso seja o estouro 

            if not primeira_tacada_feita:
                print("Primeira tacada realizada. Criando Bola 1.")
                # Define a posição de criação (head spot)
                posicao_criacao_bola1 = (margem_da_mesa+margem_das_tabelas+raio_bola+1, altura / 2)
                # Pega a cor correta para a bola 1
                cor_bola_1 = cor_por_numero.get(1, AMARELO_LISTRADO) # Usa Amarelo como padrão

                # Cria a bola 1
                corpo_b1, forma_b1 = criar_bola(posicao_criacao_bola1, raio_bola, massa_bolas_coloridas, cor_bola_1, 1)

                # Adiciona às listas principais (importante!)
                bolas_corpos.append(corpo_b1)
                bolas_formas.append(forma_b1)

                # Marca que a primeira tacada foi feita
                primeira_tacada_feita = True
                # Marca a bola 1 como "em jogo"
                bola_um_em_jogo = True
            # --------------------------------------------- 


            #Agora nós temos que mudar o estado do jogo, pq depois que a tacada é dada as bolas entram em movimento
            ESTADO_JOGO = "BOLAS_EM_MOVIMENTO"
            pos_inicial_clique_esquerdo = None
            vetor_mira_travado = None
            bolas_encacapadas_na_jogada.clear()
            falta_na_jogada = False 
            primeiro_contato = None










    # --- ATUALIZAÇÕES CONTÍNUAS (FORA DO LOOP DE EVENTOS) ---
    if ESTADO_JOGO == "MIRANDO":
        mouse_pos = pygame.mouse.get_pos()
        vetor_direcao = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(bola_branca_corpo.position)
        
        if vetor_direcao.length() > 0:
            angulo_taco_rad = math.atan2(vetor_direcao.y, vetor_direcao.x)
            taco_corpo.angle = angulo_taco_rad
            ######
            offset_taco = vetor_direcao.normalize() * -(raio_bola + comprimento_taco / 2)
            taco_corpo.position = bola_branca_corpo.position + offset_taco
            
            ponto_final_mira = bola_branca_corpo.position + vetor_direcao.normalize() * 1000
            linha_mira = [bola_branca_corpo.position, ponto_final_mira]
    
    elif ESTADO_JOGO == "PUXANDO_TACO":
        mouse_pos = pygame.mouse.get_pos()
        vetor_arrasto = pygame.Vector2(mouse_pos) - pos_inicial_clique_esquerdo
        
        distancia_puxada = abs(vetor_arrasto.length())
        
        # Usa o vetor de mira travado para consistência
        direcao_taco = vetor_mira_travado
        
        offset_base = direcao_taco * -(raio_bola + comprimento_taco / 2)
        pos_base = bola_branca_corpo.position + offset_base
        
        taco_corpo.position = pos_base + direcao_taco * -distancia_puxada
    

    elif ESTADO_JOGO == "BOLAS_EM_MOVIMENTO":
        #esconde o taco enquanto as bolas estão em movimento 
        linha_mira = [] #aqui estamos garantindo que a linha de mira não vai ser impressa na tela caso as bolas ainda estejam em movimento.

        #agora a gente verifica se todas as bolas estão paradas ou não 
        if todas_bolas_paradas():
            print("bolas pararam...")

            #aqui entra a lógica de avaliação 
            trocar_turno = True #estamos assumindo que o turno será trocado por padrão 

            #primeiro a gente verifica se houve alguma falta 
            if falta_na_jogada:
                print(f"Falta cometida pelo jogador {turno_jogador}.")
                trocar_turno = True 
            #agora a gente verifica se houve alguma bola encaçapada caso não tenha havido falta. 
            elif bolas_encacapadas_na_jogada:
                jogador_atual_grupo = jogador1_grupo if turno_jogador == 1 else jogador2_grupo
                #Verifica se alguma bola encaçapada pertence ao grupo do jogador
                bola_valida_encacapada = True 
                for num_bola in bolas_encacapadas_na_jogada:
                    #define o grupo da bola (par ou impar)
                    grupo_da_bola = "pares" if num_bola % 2 == 0 else "impares"

                    #Se os grupos ainda não foram definidos e a bola não é a 8 
                    if not bolas_atribuidas and num_bola != 8:
                        print(f"Primeira bola encaçapada de forma válida: {num_bola}. Grupos definidos")
                        if turno_jogador == 1:
                            #aqui a gente esta atribuindo o grupo da bola para o jogador 1 
                            jogador1_grupo = grupo_da_bola
                            #define o grupo das bolas do jogador 2 com base no grupo de bolas do jogador 1 
                            jogador2_grupo = "pares" if grupo_da_bola == "impares" else "impares"
                        else:
                            jogador2_grupo = grupo_da_bola
                            jogador1_grupo = "pares" if grupo_da_bola == "impares" else "impares"

                        #passando disso as bolas foram atribuidas agora 
                        bolas_atribuidas = True 
                        jogador_atual_grupo = grupo_da_bola #define a primeira 
                        bola_valida_encacapada = True #primeira bola encacapada define o grupo e vale o turno 
                    elif bolas_atribuidas and jogador_atual_grupo == grupo_da_bola:
                        bola_valida_encacapada = True 
                        #se encaçapou a bola valida não precisa checar as outras dessa jogada
                        break 
                    
                #agora é o seguinte, se o jogador encaçapou uma bola valida, seja ela a primeira bola do jogo ou uma bola do grupo dele, ele continua na jogada né ? 
                if bola_valida_encacapada:
                    print(f"Jogador {turno_jogador} encaçapou uma bola válida. Continua jogando.")
                    trocar_turno = False 
                else: 
                    print(f"Jogador {turno_jogador} encaçapou uma bola inválida. Passa a vez.")
                    #acho aqui entraria o caso de avaliar qual foi a bola errada que o jogador na tacada encaçapou errado e já fazer a remoção da bola aqui. 
                    trocar_turno = True
            #mas também pode ter acontecido dele ter feito a tacada, não ter encaçapado nenhuma bola e não ter cometido nenhuma falta.
            else:
                print(f"O jogador{turno_jogador} não encaçapou nenhuma bola e não cometeu nenhuma falta")
                trocar_turno = True 
            
            #agora a gente tem que fazer a troca de turno 
            if trocar_turno:
                turno_jogador = 2 if turno_jogador == 1 else 1
                print(f"Turno passa para o jogador {turno_jogador}")
            #Agora que tudo foi tratado temos que atualizar o estado do jogo. 
            ESTADO_JOGO = "ESPERANDO_JOGADA"

    else:
        linha_mira = []

    # --- LÓGICA DO JOGO (FÍSICA E REGRAS) ---
    
    # Atualiza a física do Pymunk
    espaco.step(1 / 60.0)

    #Mecânica de encaçapamento das bolas:
    #como o proprio titulo diz essa seção do código trata do encaçapamento das bolas no jogo.
    bolas_para_remover = []
    quadrado_raio_do_buraco = raio_do_buraco * raio_do_buraco
    #para saber qual bola foi encaçapada é preciso fazer toda uma checagem das bolas né, por isso nós usamos esse laço for
    for forma_bola in bolas_formas:
        #pegamos a posicao da bola
        pos_bola = forma_bola.body.position
        #agora fazemos mais um for para iterar pelos 6 buracos
        for pos_buraco in posicoes_buracos:
            
            pos_buraco_vec = pymunk.Vec2d(pos_buraco[0],pos_buraco[1])
            distancia_sq = pos_bola.get_distance_squared(pos_buraco_vec)
            #se a distancia entre o centro da bola e o centro do burado for menor que o raio do buraco, isso significa que a bola foi encacapada apos a jogada 
            if distancia_sq < quadrado_raio_do_buraco:
                #agora a gente pega o numero da bola 
                numero_bola = forma_bola.numero
                #se a bola encapada for a bola branca
                if forma_bola == bola_branca_forma:
                    print("Você encaçapou a bola branca")
                    falta_na_jogada = True #aqui marcamos a falta 
                    bola_branca_corpo.position = (largura*0.3, altura/2)
                    bola_branca_corpo.velocity = (0,0)
                    bola_branca_corpo.angular_velocity = 0
                else:#caso não tenha sido a bola branca 
                    #adicionamos a bola encaçapada na lista
                    if numero_bola not in bolas_encacapadas_na_jogada:
                        bolas_encacapadas_na_jogada.append(numero_bola)
                    #inserimos a bola na lista de bolas para remover no proximo quadro
                    if forma_bola not in bolas_para_remover:
                        bolas_para_remover.append(forma_bola)
                break
    
    #agora a gente remove e atualiza as listas de bolas em jogo

    for forma in bolas_para_remover:
        numero = forma.numero 
        print(f"Bola {numero} encaçapada pelo jogador {turno_jogador}.")
        #agora a gente faz a remoção da bola encaçapada efetivamente
        espaco.remove(forma.body,forma)
        bolas_corpos.remove(forma.body)
        bolas_formas.remove(forma)

        #agora a gente atualiza as listas de rastreio 
        if numero == 1:
            bola_um_em_jogo = False 
            #aqui vai entrar a logica de vitória da partida 

        elif numero % 2 != 0: # a bola é impar 
            if numero in bolas_impares_em_jogo:
                bolas_impares_em_jogo.remove(numero)
        else:
            if numero in bolas_pares_em_jogo:
                bolas_pares_em_jogo.remove(numero)
        #Fim da mecânica de encaçapamento das bolas. 
        
                












    #for forma in bolas_para_remover:
    #    print("Bola colorida encacapada!")
    #    espaco.remove(forma.body,forma)
    #    bolas_corpos.remove(forma.body)
    #    bolas_formas.remove(forma)

    # --- SEÇÃO DE DESENHO (Tudo acontece no final) ---
    
    #Desenho da mesa
    tela.fill(VERDE)
    pygame.draw.rect(tela, MARROM, (0,0,largura,altura), margem_da_mesa)
    
    #Desenha os buracos na mesa:
    for posicao_buraco in posicoes_buracos:
        posicao_buraco_convertida = (int(posicao_buraco[0]), int(posicao_buraco[1]))
        pygame.draw.circle(tela, PRETO,posicao_buraco_convertida,raio_do_buraco)

    #Desenha as Tabelas na mesa:
    for tabela in lista_tabelas:
        pygame.draw.polygon(tela, cor_da_tabela,tabela)

    #Desenha as Cacapas na mesa:
    for cacapa in lista_cacapas:
        pygame.draw.polygon(tela, cor_da_cacapa, cacapa)
    
    #Desenha as bolas na mesa:
    for forma in bolas_formas:
        #PRIMEIRO A GENTE PEGA A POSICAO DA BOLA PARA DESENHAR-LA NÉ CARAIO
        pos = (int(forma.body.position.x), int(forma.body.position.y))
        #Depois a gente desenha o circulo mais externo
        pygame.draw.circle(tela, forma.color, pos, raio_bola)
        #Agora a gente tem que desenhar o numero da bola, vamos usar um condicional pra isso caralho
        if forma.numero is not None:
            #primeiro temos que sedenhar o circulo branco na forma da bola, pra isso precisamos definir o raio desse circulo branco, quero que o diametro desse circulo branco seja do tamanho da bola branca, por que? por que sim uai.  
            #raio_circulo_branco = raio_bola * 0,6
            # --- ADICIONE ESTA LINHA PARA DEBUG ---
            #print(f"DEBUG: Tipo={type(raio_circulo_branco)}, Valor={raio_circulo_branco}")
            # ------------------------------------/
            pygame.draw.circle(tela, BRANCO, pos, 9)
            #agora a gente tem que renderizar o texto na bola ou seja o numero da bola, eu vou conseguir passar nessa materia. 
            texto_surface = numero_font.render(str(forma.numero),True,PRETO)
            texto_rect = texto_surface.get_rect()
            texto_rect.center = pos 
            tela.blit(texto_surface, texto_rect)
            
    # Desenha o taco apenas se estivermos em um estado de tacada
    if taco_corpo and ESTADO_JOGO in ["MIRANDO", "PUXANDO_TACO"]:
        vertices = [v.rotated(taco_corpo.angle) + taco_corpo.position for v in taco_forma.get_vertices()]
        #esse condicional aqui serve para verificar quem está na tacada, se é o jogador 1 ou o jogador 2. 
        if turno_jogador == 1:
            cor_atual_taco = COR_TACO_JOGADOR1
        else:
            cor_atual_taco = COR_TACO_JOGADOR2
        pygame.draw.polygon(tela, cor_atual_taco, vertices)
    # Desenha a linha de mira se ela existir
    if linha_mira:
        desenhar_linha_tracejada(tela, BRANCO, linha_mira[0], linha_mira[1])

    pygame.display.flip()
    clock.tick(60)

pygame.quit()