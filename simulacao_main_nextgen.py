#bibliotecas
import pygame
import pymunk
import pymunk.pygame_util
import math
import logica_jogo


# Inicialização do Pygame
pygame.init()

#criando um objeto de fonte, vai servir para criar os números nas bolas
try:
    numero_font = pygame.font.SysFont('Arial',14, bold = True)
except: 
    numero_font = pygame.font.Font(None,18)



#Configurações da Janela, dimensões externas da mesa
largura, altura = 1100, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Sinuca")



#lista de variáveis para o jogo
turno_jogador = 1             # Começa com o Jogador 1
bolas_atribuidas = False      # Os tipos de bola que cada jogador mata ainda não foram definidos, então é inicializado como false
jogador1_grupo = None         # Pode ser "impares", "pares" ou None
jogador2_grupo = None         # Pode ser "impares", "pares" ou None
falta_na_jogada = False       # Indica se ocorreu uma falta na jogada atual
primeiro_contato = None       # Guarda o tipo da primeira bola tocada pela branca se foi uma bola par ou ímpar.
primeiro_contato_tipo = None  # Armazena qual foi o tipo da primeira colisão: se foi em uma bola ou tabela(impacta na regra)
bolas_encacapadas_na_jogada = [] # Lista de números das bolas encaçapadas na jogada atual
primeira_tacada_feita = False    # Indica que o estouro ainda não foi feito
bolas_impares_em_jogo = [3, 5, 7, 9, 11, 13, 15]# lista das bolas impares, exclui a 1, pois ela é o castigo
bolas_pares_em_jogo = [2, 4, 6,8, 10, 12, 14] #lista das bolas pares 
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
# esse dicionario serve para pegar a cor da bola de acordo com o seu numero.

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

# Variaveis da parte física do jogo
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

# Posições dos buracos: essa lista tem todos os pontos onde os buracos da mesa estarão localizados
posicoes_buracos = [
    (margem_da_mesa + raio_do_buraco, margem_da_mesa + raio_do_buraco), # Canto Superior Esquerdo
    (largura/2, margem_da_mesa + raio_do_buraco), # Meio Superior
    (largura - margem_da_mesa - raio_do_buraco, margem_da_mesa + raio_do_buraco), # Canto Superior Direito
    (margem_da_mesa + raio_do_buraco, altura - raio_do_buraco - margem_da_mesa), # Canto Inferior Esquerdo
    (largura/2, altura - margem_da_mesa - raio_do_buraco), # Meio Inferior
    (largura - raio_do_buraco - margem_da_mesa, altura - raio_do_buraco - margem_da_mesa) # Canto Inferior Direito
]

#Posicoes das tabelas:
tabela_superior_esquerda = [(margem_da_mesa+26,margem_da_mesa),
                            (largura/2 - raio_do_buraco,margem_da_mesa),
                            (largura/2-raio_do_buraco-4,margem_da_mesa+margem_das_tabelas),
                            (margem_da_mesa+margem_das_tabelas+30, margem_da_mesa+margem_das_tabelas)]
tabela_superior_direita = [(largura/2+raio_do_buraco,margem_da_mesa),
                           (largura - margem_da_mesa - 26, margem_da_mesa), 
                           (largura - margem_da_mesa-margem_das_tabelas-30,margem_da_mesa+margem_das_tabelas), 
                           (largura/2+raio_do_buraco+4,margem_da_mesa+margem_das_tabelas)]
tabela_lateral_esquerda = [(margem_da_mesa,margem_da_mesa+26),#P1
                            (margem_da_mesa+margem_das_tabelas,margem_da_mesa+margem_das_tabelas+30),#P2
                            (margem_da_mesa+margem_das_tabelas,altura-margem_da_mesa-margem_das_tabelas-30),#P3
                            (margem_da_mesa,altura - margem_da_mesa-26)]
    
tabela_lateral_direita = [(largura - margem_da_mesa,margem_da_mesa+26),#P1
                          (largura - margem_da_mesa,altura - margem_da_mesa - 26),#P2
                          (largura - margem_da_mesa-margem_das_tabelas,altura -margem_da_mesa - margem_das_tabelas -30),#P3
                          (largura-margem_da_mesa-margem_das_tabelas,margem_da_mesa+margem_das_tabelas+30) ]
    
tabela_inferior_esquerda =  [(margem_da_mesa+26,altura - margem_da_mesa),#P1
                             (largura/2 - raio_do_buraco,altura-margem_da_mesa),#P2
                             (largura/2 - raio_do_buraco-4,altura - margem_da_mesa-margem_das_tabelas),#P3
                             (margem_da_mesa+margem_das_tabelas+30,altura - margem_da_mesa-margem_das_tabelas)]
    
tabela_inferior_direita = [(largura/2 +raio_do_buraco,altura-margem_da_mesa),#P1
                           (largura/2 + raio_do_buraco + 4, altura - margem_da_mesa -margem_das_tabelas), #P2
                           (largura-margem_da_mesa-margem_das_tabelas-30,altura-margem_da_mesa-margem_das_tabelas), #P3
                           (largura-margem_da_mesa-26,altura-margem_da_mesa)]
    
lista_tabelas = [ tabela_superior_esquerda, tabela_lateral_esquerda, tabela_superior_direita, tabela_lateral_direita, tabela_inferior_esquerda, tabela_inferior_direita]

#Detalhe das caçapas
cacapa_superior_esquerda = [(0,0),
                        (margem_da_mesa+8,0),
                        (margem_da_mesa+margem_das_tabelas-5,margem_da_mesa),
                        (margem_da_mesa,margem_da_mesa+margem_das_tabelas-5),
                        (0,margem_da_mesa+8)]
cacapa_meio_superior = [(largura/2 - raio_do_buraco - 14,0),
                        (largura/2 + raio_do_buraco + 14,0),
                        (largura/2 + raio_do_buraco, margem_da_mesa + raio_do_buraco),
                        (largura/2 - raio_do_buraco, margem_da_mesa + raio_do_buraco)]
cacapa_superior_direita = [(largura - margem_da_mesa - 8, 0),
                           (largura,0),
                           (largura,margem_da_mesa +8),
                           (largura - margem_da_mesa,margem_da_mesa+margem_das_tabelas -5),
                           (largura - margem_da_mesa -margem_das_tabelas+5,margem_da_mesa)]  
cacapa_inferior_direita = [(largura,altura - margem_da_mesa-8),
                           (largura,altura),
                           (largura - margem_da_mesa -8, altura),
                           (largura-margem_da_mesa-margem_das_tabelas+5,altura -margem_da_mesa),
                           (largura -margem_da_mesa, altura - margem_da_mesa -margem_das_tabelas +5)]  
cacapa_meio_inferior = [(largura/2 - raio_do_buraco - 14, altura),
                        (largura/2 + raio_do_buraco + 14, altura),
                        (largura/2 + raio_do_buraco, altura - margem_da_mesa-raio_do_buraco),
                        (largura/2 - raio_do_buraco, altura - margem_da_mesa-raio_do_buraco)]
    
cacapa_inferior_esquerda = [(0,altura),
                            (0,altura-margem_da_mesa-8),
                            (margem_da_mesa,altura -margem_da_mesa-margem_das_tabelas+5),
                            (margem_da_mesa+margem_das_tabelas-5,altura-margem_da_mesa),
                            (margem_da_mesa+8,altura)]
#Essa lista armazena um conjunto de listas pontos(6 variaveis anteriores) que é utilizado para desenhar os detalhes cinzas das caçapas, 
lista_cacapas = [ cacapa_superior_esquerda,cacapa_meio_superior, cacapa_superior_direita,cacapa_inferior_direita,cacapa_meio_inferior,cacapa_inferior_esquerda]

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
#basicamente estamos só definindo uma marcacao para diferenciar as bolas coloridas da bola branca. cada objeto no jogo bolas e tabelas tem um tipo de colisao proprio 
''' as 4 variaveis a seguir contem o tipo de colisao que cada objeto vai experienciar. Elas são importantes na hora de fazer a identificação de ocorrência de faltas. É através de uma função, colisao_bola_branca_callback que o pymunk identifica o que deve acontecer quando uma colisão entre uma bola e uma tabela ocorre, e se essa colisão deve ser processada por exemplo. Esses marcadores são definidos como numeros inteiros por padrão na biblioteca pymunk.
'''
col_tipo_bola_branca = 1 
col_tipo_bola_par = 2
col_tipo_bola_impar = 3
col_tipo_tabela = 4
# Configurações do Pymunk
espaco = pymunk.Space()#espaco é a variavel encima da qual toda a fisica do jogo vai acontecer 
espaco.gravity = (0, 0)#o jogo é bidimensional é estamos olhando ele de cima, não é necessário implementar gravidade
espaco.damping = 0.60 # é a perda por atrito do espaço, 0.60 é o valor que mais se adequa à realidade
draw_options = pymunk.pygame_util.DrawOptions(tela)

# Seção de Funções: A seguir temos um conjunto de funções que são utilizadas no jogo, cada uma tem uma utilidade e sua funcionalidade pode ser lida nas docstrings presentes.
def criar_bola(posicao, raio, massa, cor, numero = None):
    '''
    Essa função é responsável por criar as bolas no jogo, criando uma forma e um corpo, a forma é o desenho, ou seja, o que você vê visualmente. O corpo é o objeto que vai passsar pelas colisoes.
    numero é passado com valor padrao None para facilitar a parte da criação da bola branca. 
    posicao: coordenadas (x,y) de onde a bola deve ser criada
    raio: raio da circunferencia da bola
    massa: nesse caso é o numero proporcional, se for bola numerada é 1, branca é 1,15.
    cor: cor que a bola vai ter
    numero: numero da bola, por padrão é None por conta da bola branca.
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

    #agora a gente usa o numero da bola para definir o tipo de colisao que essa bola vai experienciar
    if numero is None:
        #Se for a bola branca, atribui o tipo de colisao como bola branca
        forma_bola.collision_type = col_tipo_bola_branca
    elif numero % 2 == 0: 
        #Se o numero da bola é par, atribui o tipo de colisao que ela vai experienciar
        forma_bola.collision_type = col_tipo_bola_par
    else:
        #Mesma coisa 
        forma_bola.collision_type = col_tipo_bola_impar
    #por fim, retorna dois objetos, a forma da bola que é desenhada na tela, e o corpo dela, que é processado pelo pymunk.
    return corpo_bola, forma_bola
def criar_tabelas(tabelas_tabelas_tabelas):
    """
    Cria as 6 tabelas como poligonos estáticos que correspondem
    aos poligonos que são desenhados na tela.
    tabelas_tabelas_tabelas: é uma lista de listas de pontos, cada item dessa lista contém uma lista de pontos de uma das tabelas
    """
    for tabela in tabelas_tabelas_tabelas:
        forma_tabela = pymunk.Poly(espaco.static_body,tabela)
        forma_tabela.elasticity = 0.9
        forma_tabela.friction = 0.8
        forma_tabela.color = cor_da_tabela
        espaco.add(forma_tabela)
        forma_tabela.collision_type = col_tipo_tabela
def criar_taco():
    """
    Esta função é usada para criar o taco no jogo, o principio de funcionamento é o mesmo das outras funções de desenho.
    A unica diferença esta no corpo em si, é um corpo do tipo KINEMATIC, objetos desse tipo não interagem com o ambiente.
    """
    corpo = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    forma = pymunk.Poly.create_box(corpo, (comprimento_taco, largura_taco))
    forma.sensor = True # transforma o taco em um "sensor"
    espaco.add(corpo, forma)
    return corpo, forma
def desenhar_linha_tracejada(superficie, cor, inicio, fim, largura=1, espaco_traco=5):
    '''
    Essa função serve para desenhar uma linha tracejada para auxiliar o jogador a mirar. 
    superficie: superficie na qual a linha é desenhada
    cor: cor da linha 
    inicio: ponto (x,y) que marca qual é o ponto de inicio da linha de mira, geralmente é a propria coodenada da bola branca
    fim : ponto (x,y) que marca o fim da linha tracejada
    largura = 1: variavel que marca a largura da linha em pixels
    espaco_traco = 5: a linha é tracejada, essa variavel marca o espaço entre cada um dos tracinhos
    '''
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
    O pymunk tem uma falha: as bolas demoram para parar, dessa forma, utilizamos essa função para verificar se a velocidade da bola ao quadrado(evitar valores negativos) é menor que a do limiar.
    limiar_velocidade_sq = 10: O pymunk tem uma falha
    Retorna False se as bolas ainda estão em movimento, True se estão todas paradas
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
def aplicar_remocao_penalidade(jogador_alvo, num_bolas_remover):
    """
    Remove fisicamente as 'num_bolas_remover' de menor número do grupo do jogador alvo.
    Esta função precisa ser chamada APENAS na lógica de penalidade (fora do loop de encaçapamento).
    quando uma falta grave é cometida, como acertar diretamente uma bola do oponente por exemplo, ela faz a remoção das bolas de menor numero do outro jogador.
    jogador_alvo: jogador que não está na tacada
    num_bolas_remover: numero de bolas a serem removidas
    """
    global bolas_impares_em_jogo, bolas_pares_em_jogo, bolas_formas, bolas_corpos, espaco, bolas_por_numero

    # 1. Determina a lista de bolas restantes em jogo do alvo
    if jogador_alvo == 1:
        grupo_alvo = jogador1_grupo
    else:
        grupo_alvo = jogador2_grupo
        
    if grupo_alvo == "impares":
        lista_numeros = bolas_impares_em_jogo
    elif grupo_alvo == "pares":
        lista_numeros = bolas_pares_em_jogo
    else:
        # Grupos não definidos, não há penalidade a ser aplicada
        return 

    # 2. Ordena e seleciona as bolas de menor número (já estão ordenadas, mas garante)
    bolas_selecionadas = sorted(lista_numeros)[:num_bolas_remover]

    if not bolas_selecionadas:
        print("PENALIDADE: Nenhuma bola para remover do adversário.")
        return

    print(f"PENALIDADE: Removendo bolas {bolas_selecionadas} do jogador alvo.")

    # 3. Remove a bola fisicamente do jogo e das listas
    for num in bolas_selecionadas:
        if num in bolas_por_numero:
            corpo = bolas_por_numero[num]['corpo']
            forma = bolas_por_numero[num]['forma']

            # 3a. Remove do espaço físico
            espaco.remove(corpo, forma)
            
            # 3b. Remove das listas de rastreamento principais
            bolas_corpos.remove(corpo)
            bolas_formas.remove(forma)
            del bolas_por_numero[num]

            # 3c. Remove da lista de rastreamento de regras (impares/pares)
            if num % 2 != 0:
                bolas_impares_em_jogo.remove(num)
            else:
                bolas_pares_em_jogo.remove(num)
def aplicar_penalidade_suave(jogador_alvo):
    """
    Remove uma bola de menor número do grupo do jogador alvo (penalidade suave).
    jogador_alvo: jogador que não está na tacada. 
    """
    global bolas_impares_em_jogo, bolas_pares_em_jogo, bolas_formas, bolas_corpos, espaco, bolas_por_numero

    if jogador_alvo == 1:
        grupo_alvo = jogador1_grupo
    else:
        grupo_alvo = jogador2_grupo
        
    if grupo_alvo == "impares":
        lista_numeros = bolas_impares_em_jogo
    elif grupo_alvo == "pares":
        lista_numeros = bolas_pares_em_jogo
    else:
        print("Penalidade Suave: Grupos não atribuídos.")
        return 

    # Seleciona a bola de menor número para remoção
    if lista_numeros:
        bola_a_remover_num = lista_numeros[0] # A lista já está ordenada (menor número é o índice 0)
        
        print(f"PENALIDADE SUAVE: Bola {bola_a_remover_num} removida do jogo.")

        # 1. Remoção da lista de regras (impares/pares)
        lista_numeros.remove(bola_a_remover_num)
        
        # 2. Remoção física do espaço
        if bola_a_remover_num in bolas_por_numero:
            corpo = bolas_por_numero[bola_a_remover_num]['corpo']
            forma = bolas_por_numero[bola_a_remover_num]['forma']

            espaco.remove(corpo, forma)
            bolas_corpos.remove(corpo)
            bolas_formas.remove(forma)
            del bolas_por_numero[bola_a_remover_num]
def colisao_bola_branca_tabela_callback(arbiter, espaco, data):
    """
    Essa função é usada como callback sempre que ocorre uma colisao entre uma bola e uma tabela. 
    arbiter: é um objeto da própria biblioteca pymunk, serve para processar a colisão entre os objetos
    espaco: objeto da classe Space no qual a colisao ocorre, neste caso o espaco definido no inicio do codigo
    data: são os dados que queremos que o arbiter (Arbitro) analise, quando essa função é chamada passamos para ela um dicionario dados_para_handler como padrão.
    No fim retorna True para que a colisao possa ser processada normalmente.
    """
    #a linha de codigo a seguir foi pode ser comentada, pois serve para verificar se ela esta sendo chamada. 
    print("funcao colisao bola branca tabela callback disparada")
    # Lê do dicionário 'data'
    primeiro_contato = data["primeiro_contato"]
    primeiro_contato_tipo = data["primeiro_contato_tipo"]
    
    # Apenas se NADA foi registrado antes
    if primeiro_contato_tipo is None and primeiro_contato is None:
        #Atualiza o dicionário
        data["primeiro_contato_tipo"] = "tabela"
        print("Primeiro Contato: Tabela (Sequência Checada).")
    
    return True
def colisao_bola_branca_callback(arbiter, espaco, data):
    """
    Essa função é usada como callback sempre que ocorre uma colisao entre a bola branca e uma bola colorida. Essencialmente o que ela faz é checar se a bola branca colidiu com uma das bolas do jogador na tacada ou uma das bolas do outro jogador.
    arbiter: é um objeto da própria biblioteca pymunk, serve para processar a colisão entre os objetos
    espaco: objeto da classe Space no qual a colisao ocorre, neste caso o espaco definido no inicio do codigo
    data: são os dados que queremos que o arbiter (Arbitro) analise, quando essa função é chamada passamos para ela um dicionario dados_para_handler como padrão.
    No fim retorna True para que a colisao possa ser processada normalmente.
    """
    print("funcao bola branca call back invocada")
    global primeiro_contato, primeiro_contato_tipo, falta_na_jogada
    global bolas_atribuidas, turno_jogador, jogador1_grupo, jogador2_grupo
    global dados_para_handler # Para sinalizar a penalidade


    # Só processa a lógica se for o PRIMEIRO contato com uma bola
    if primeiro_contato is None:
        a, b = arbiter.shapes
        # Identifica a bola branca e a outra bola
        forma_branca = a if a.collision_type == col_tipo_bola_branca else b
        forma_tocada = b if a.collision_type == col_tipo_bola_branca else a
        
        num_bola_tocada = forma_tocada.numero if hasattr(forma_tocada, 'numero') else None

        if num_bola_tocada is None or num_bola_tocada == 0: 
            return True

        grupo_bola_tocada = "pares" if num_bola_tocada % 2 == 0 else "impares"
        
        #Registra nos dados qual o numero da bola tocada
        data["primeiro_contato"] = num_bola_tocada
        # Define qual foi o grupo da bola tocada, se foi par ou impar
        if primeiro_contato_tipo is None:
             primeiro_contato_tipo = grupo_bola_tocada

        # Lógica de faltas
        if bolas_atribuidas:#se já existe um grupo de bolas definido
            grupo_jogador_atual = jogador1_grupo if turno_jogador ==1 else jogador2_grupo

            #Casos em que a falta é grave:
            #primeiro caso: acertou diretamente a bola uma bola do adversário
            if primeiro_contato_tipo != "tabela" and grupo_jogador_atual != grupo_bola_tocada and num_bola_tocada != 1:
                falta_na_jogada = True
                #sinaliza a penalidade grave 
                dados_para_handler["penalidade_aplicar"] ={"tipo":"grave", "jogador":2 if turno_jogador == 1 else 1}
                print(f"Falta grave, jogador {turno_jogador} acertou diretamente uma bola do outro jogador.")
                return True
            elif primeiro_contato_tipo != "tabela" and num_bola_tocada == 1:
                #checa se o jogador atual ainda tem bolas para matar
                if grupo_jogador_atual == "pares" and len(bolas_pares_em_jogo)>0:#jogador atual mata par
                    #se o jogador atual ainda tem bolas para matar antes da 1 e a atingiu diretamente, falta grave
                    falta_na_jogada = True 
                    dados_para_handler["penalidade_aplicar"] = {"tipo":"grave", "jogador": 2 if turno_jogador == 1 else 1}
                    print(f"jogador {turno_jogador} cometeu uma falta, acertou a bola 1 diretamente sem ter terminado de matar as bolas dele")
                    return True
                if grupo_jogador_atual == "impares" and len(bolas_impares_em_jogo) > 0:#jogador atual mata par
                    #se o jogador atual ainda tem bolas para matar antes da 1 e a atingiu diretamente, mata impar, falta grave
                    falta_na_jogada = True 
                    dados_para_handler["penalidade_aplicar"] = {"tipo":"grave", "jogador": 2 if turno_jogador == 1 else 1}
                    print(f"jogador {turno_jogador} cometeu uma falta, acertou a bola 1 diretamente sem ter terminado de matar as bolas dele")
                    return True       
            #caso em que a falta é suave
            #jogador jogou, pegou na tabela e acertou uma bola do adversário"
            if primeiro_contato_tipo == "tabela":#nesse caso a função de callback para colisao da bola branca com a tabela já foi chamada
                if grupo_jogador_atual != grupo_bola_tocada and num_bola_tocada !=1:
                    falta_na_jogada = True 
                    dados_para_handler["penalidade_aplicar"] = {"tipo":"suave", "jogador": 2 if turno_jogador == 1 else 1}
                    print(f"O jogador {turno_jogador} cometeu uma falta, acertou uma bola do adversário tocando na tabela primeiro")
                    return True
            if primeiro_contato_tipo == "tabela" and num_bola_tocada == 1 and grupo_jogador_atual == "pares" and len(bolas_pares_em_jogo)>0:
                falta_na_jogada = True 
                dados_para_handler["penalidade_aplicar"] = {"tipo":"suave", "jogador": 2 if turno_jogador == 1 else 1}
                print(f"O jogador {turno_jogador} cometeu uma falta, acertou a bola 1 sem ter terminado de encaçapar as bolas pares dele primeiro")
                return True 
            if primeiro_contato_tipo == "tabela" and num_bola_tocada == 1 and grupo_jogador_atual == "impares" and len(bolas_impares_em_jogo)>0:
                falta_na_jogada = True 
                dados_para_handler["penalidade_aplicar"] = {"tipo":"suave", "jogador": 2 if turno_jogador == 1 else 1}
                print(f"O jogador {turno_jogador} cometeu uma falta, acertou a bola 1 sem ter terminado de encaçapar as bolas impares dele primeiro")
                return True 
    return True


# Cria os objetos do jogo
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
        

        # Incrementa o número INDEPENDENTEMENTE de ter criado a bola ou não
        numero_bola_atual += 1
#Dicionario com os dados que serão necessários para o handler de colisões
dados_para_handler = {
                    #variaveis de controle de fluxo 
                    "ESTADO_JOGO": ESTADO_JOGO,
                    "turno_jogador":primeiro_contato,
                    "primeira_tacada_feita": primeira_tacada_feita,
                    "vencedor": vencedor, 
                    #variaveis de lógica de colisão e faltas 
                    "primeiro_contato": primeiro_contato,
                    "primeiro_contato_tipo": primeiro_contato_tipo,
                    "falta_na_jogada": falta_na_jogada, 
                    #variaveis de regra de jogo 
                    "bolas_atribuidas": bolas_atribuidas,
                    "jogador1_grupo":jogador1_grupo,
                    "jogador2_grupo":jogador2_grupo
                      }

#Callbacks quando ocorrem colisões: aqui são utilizadas as funcoes de callback para tratar as colisoes e identificar quando uma falta é cometida
# Esse callback vai chamar a função colisao_bola_branca_tabela_calback sempre que a bola branca colidir com a tabela
espaco.on_collision(col_tipo_bola_branca, col_tipo_tabela, colisao_bola_branca_tabela_callback, data=dados_para_handler)
# Esse callback vai chamar a função colisao_bola_branca_callback semrpe que a bola branca colidir com uma das bolas pares uai
espaco.on_collision(col_tipo_bola_branca, col_tipo_bola_par, colisao_bola_branca_callback,data=dados_para_handler)
# Esse callback vai chamar a função colisao_bola_branca_callback semrpe que a bola branca colidir com uma das bolas impares uai
espaco.on_collision(col_tipo_bola_branca, col_tipo_bola_impar, colisao_bola_branca_callback,data=dados_para_handler)


#Chama a função da criação das tabelas
criar_tabelas(lista_tabelas)

# Loop principal do jogo
rodando = True #flag
clock = pygame.time.Clock()
while rodando:

    #O laço for a seguir serve para fazer o gerenciamento dos eventos no jogo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        
        #Inicio da tacada, quando o usuário pressiona o botão direito do mouse
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 3 and ESTADO_JOGO == "ESPERANDO_JOGADA":
            if taco_corpo is None:
                taco_corpo, taco_forma = criar_taco()
                vetor_mira_travado = None # Garante que a mira antiga seja limpa
            ESTADO_JOGO = "MIRANDO"
           
        #Se o usuário soltar o botão direito antes de pressionar o esquerdo ou quando está pressionando o botão esquerdo a tacada é cancelada
        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 3:
            if ESTADO_JOGO in ["MIRANDO", "PUXANDO_TACO"]:
                ESTADO_JOGO = "ESPERANDO_JOGADA"
                pos_inicial_clique_esquerdo = None
                linha_mira = []
                vetor_mira_travado = None

        #Se com o botao direito pressionado, o usuario clica no botao esquerdo, ele tem então que puxar o taco, dessa forma quando ele arrastar o mouse e soltar o botão esquerdo do mouse novamente a tacada sera feita. Nesse momento a mira final é definida!
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and ESTADO_JOGO == "MIRANDO":
            #a gente pega a posicao do mouse aonde o usuario clicou com o botao esquerdo
            pos_inicial_clique_esquerdo = pygame.Vector2(pygame.mouse.get_pos())
            print(pos_inicial_clique_esquerdo)
            mouse_pos = pygame.mouse.get_pos()
            vetor_direcao = pygame.math.Vector2(pos_inicial_clique_esquerdo)-pygame.math.Vector2(bola_branca_corpo.position)
            vetor_mira_travado = vetor_direcao.normalize()
            print(vetor_mira_travado)
            ESTADO_JOGO = "PUXANDO_TACO"

        #Execução da tacada, ou seja quando o usuario solta o botão esquerdo do mouse
        if evento.type == pygame.MOUSEBUTTONUP and evento.button == 1 and ESTADO_JOGO == "PUXANDO_TACO":
            # calcula a posicao final do taco para calcular a distancia de deslocamento para que a força possa ser calculada           
            pos_final_arraste = pygame.Vector2(pygame.mouse.get_pos())
            vetor_arrasto = pos_final_arraste - pos_inicial_clique_esquerdo
            forca = abs(vetor_arrasto.length())* 9 # Fator de força

            if 'FORCA_MAXIMA_TACADA' in locals() and forca > forca_maxima_tacada:
                forca = forca_maxima_tacada
            

            #define o vetor de impulso e depois aplica o impulso na tacada:
            vetor_impulso = vetor_mira_travado if vetor_mira_travado is not None else pygame.math.Vector2(1,0)
            impulso_final = pymunk.Vec2d(vetor_impulso.x * forca, vetor_impulso.y * forca)

            #Debug
            #Imprime para verificar com consistência a direção e magnitude 
            print("impulso:", impulso_final, "vetor_mira_travado:", vetor_mira_travado, "forca:", forca)
            # a funcao apply_impulse_at_world_point é utilizada para aplicar o impulso, que vem de fora(do taco) para a bola branca 
            bola_branca_corpo.apply_impulse_at_world_point(impulso_final, bola_branca_corpo.position)

            #agora temos que fazer o reposicionamento da bola 1 caso seja o estouro 
            if not primeira_tacada_feita:
                #Debug
                #mostra na tela se o jogo conseguiu identificar que a primeira tacada foi feita
                print("Primeira tacada realizada. Criando Bola 1.")
                # Define a posição de criação da bola 1(colada no meio da tabela lateral esquerda)
                posicao_criacao_bola1 = (margem_da_mesa+margem_das_tabelas+raio_bola+1, altura / 2)
                # Pega a cor correta para a bola 1
                cor_bola_1 = cor_por_numero.get(1, AMARELO_LISTRADO) # Usa Amarelo como padrão

                # Cria a bola 1
                corpo_b1, forma_b1 = criar_bola(posicao_criacao_bola1, raio_bola, massa_bolas_coloridas, cor_bola_1, 1)

                # Adiciona a bola 1 às listas principais
                bolas_corpos.append(corpo_b1)
                bolas_formas.append(forma_b1)
                # Marca que a primeira tacada foi feita
                primeira_tacada_feita = True
                # Marca a bola 1 como "em jogo"
                bola_um_em_jogo = True 


            #Agora nós temos que mudar o estado do jogo, pq depois que a tacada é dada as bolas entram em movimento
            ESTADO_JOGO = "BOLAS_EM_MOVIMENTO"#atualiza o estado do jogo
            #reseta as variaveis utilizadas para fazer a tacada
            pos_inicial_clique_esquerdo = None
            vetor_mira_travado = None
            bolas_encacapadas_na_jogada.clear()
            falta_na_jogada = False 
            primeiro_contato = None

    #Atualizações contínuas
    if ESTADO_JOGO == "MIRANDO":
        mouse_pos = pygame.mouse.get_pos()
        vetor_direcao = pygame.math.Vector2(mouse_pos) - pygame.math.Vector2(bola_branca_corpo.position)
        
        if vetor_direcao.length() > 0:
            angulo_taco_rad = math.atan2(vetor_direcao.y, vetor_direcao.x)
            taco_corpo.angle = angulo_taco_rad
            offset_taco = vetor_direcao.normalize() * -(raio_bola + comprimento_taco / 2)
            taco_corpo.position = bola_branca_corpo.position + offset_taco
            ponto_final_mira = bola_branca_corpo.position + vetor_direcao.normalize() * 1000
            linha_mira = [bola_branca_corpo.position, ponto_final_mira]
    
    elif ESTADO_JOGO == "PUXANDO_TACO":
        #serve para atualizar na tela o efeito de arrasto do taco 
        mouse_pos = pygame.mouse.get_pos()
        vetor_arrasto = pygame.Vector2(mouse_pos) - pos_inicial_clique_esquerdo
        distancia_puxada = abs(vetor_arrasto.length())
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
            print(f'bolas atribuidas? {bolas_atribuidas}')
            if 'penalidade_aplicar' in dados_para_handler:
                penalidade = dados_para_handler['penalidade_aplicar']
                jogador_alvo = penalidade['jogador']
                if penalidade['tipo'] == 'suave':
                    # Aplica a penalidade suave (remove 1 bola)
                    aplicar_penalidade_suave(jogador_alvo) 
                    falta_na_jogada = True
                elif penalidade['tipo'] == 'grave':
                    # Aplica a penalidade grave (remove 2 bolas)
                    # Reutilizamos aplicar_penalidade_suave duas vezes ou criamos uma nova
                    # Vamos usar a função aplicar_remocao_penalidade que você já tem:
                    aplicar_remocao_penalidade(jogador_alvo, 2)
                    falta_na_jogada = True
                # Limpa a flag de penalidade
                del dados_para_handler['penalidade_aplicar']#atualiza o dicionario de dados para o handler
            
            #Lógica de avaliação 
            trocar_turno = True #estamos assumindo que o turno será trocado por padrão 
            
            #Verifica se houve falta JÁ marcada (Ex: Bola Branca caiu ou Falta Grave do handler)
            if falta_na_jogada:
                print(f"Falta cometida pelo jogador {turno_jogador} (Branca caiu ou Falta Grave).")
                # Se a falta foi a branca caindo, aplicamos a penalidade suave aqui se ainda não foi aplicada
                # (Nota: Se foi falta grave do handler, a penalidade já foi aplicada acima)
                trocar_turno = True

            #Verifica se o jogador não acertou nenhuma bola (Famoso cegou de bola)
            elif primeiro_contato is None:
                #verifica se após a tacada a bola branca não encostou em nenhuma outra bola
                print(f"FALTA: Jogador {turno_jogador} não acertou nenhuma bola!")
                falta_na_jogada = True
                
                # Aplica a penalidade suave (remove 1 bola do adversário)
                jogador_adversario = 2 if turno_jogador == 1 else 1
                aplicar_penalidade_suave(jogador_adversario)
                trocar_turno = True

            #Verifica as bolas encacapadas na jogada, caso não tenha ocorrido nenhuma penalidade antes
            elif bolas_encacapadas_na_jogada:
                jogador_atual_grupo = jogador1_grupo if turno_jogador == 1 else jogador2_grupo
                #Verifica se alguma bola encaçapada pertence ao grupo do jogador
                bola_valida_encacapada = True 
                for num_bola in bolas_encacapadas_na_jogada:
                    #define o grupo da bola (par ou impar)
                    grupo_da_bola = "pares" if num_bola % 2 == 0 else "impares"
                    #Aqui verifica se as bolas ainda não foram definidas
                    if not bolas_atribuidas:
                        #Debug
                        #Imprime na tela o numero da bola encaçapada
                        print(f"Primeira bola encaçapada de forma válida: {num_bola}. Grupos definidos")
                        if turno_jogador == 1:
                            jogador1_grupo = grupo_da_bola
                            jogador2_grupo = "pares" if grupo_da_bola == "impares" else "impares"
                        else:
                            jogador2_grupo = grupo_da_bola
                            jogador1_grupo = "pares" if grupo_da_bola == "impares" else "impares"

                        #Caso alguma bola foi encaçapada atualiza a variavel que marca isso
                        bolas_atribuidas = True 
                        
                        # Atualiza o dicionário para evitar sobrescrita
                        dados_para_handler["bolas_atribuidas"] = True
                        dados_para_handler["jogador1_grupo"] = jogador1_grupo
                        dados_para_handler["jogador2_grupo"] = jogador2_grupo
                        jogador_atual_grupo = grupo_da_bola 
                        bola_valida_encacapada = True
                    #Caso o jogador tenha encacapado uma bola válida    
                    elif bolas_atribuidas and jogador_atual_grupo == grupo_da_bola:
                        bola_valida_encacapada = True 
                        #se encaçapou a bola valida não precisa checar as outras dessa jogada
                        break   

                #Se o jogador encaçapou uma bola valida, seja ela a primeira bola do jogo ou uma bola do grupo dele, ele continua na jogada 
                if bola_valida_encacapada:
                    print(f"Jogador {turno_jogador} encaçapou uma bola válida. Continua jogando.")
                    trocar_turno = False 
                else: 
                    print(f"Jogador {turno_jogador} encaçapou uma bola inválida. Passa a vez.") 
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
            #depois que todas as bolas pararam a gente limpa a lista
            #Limpa as variaveis que são utilizadas nas callbacks
            primeiro_contato_tipo = None 
            primeiro_contato = None
            ESTADO_JOGO = "ESPERANDO_JOGADA"#Atualiza o estado do jogo

    else:
        linha_mira = []

    #Lógica do jogo: Física e regras
    #atualização do dicionario do handler antes da fisica
    #Sincroniza da física (Passa o estado atual para os handlers)
    dados_para_handler["ESTADO_JOGO"] = ESTADO_JOGO
    dados_para_handler["primeiro_contato"] = primeiro_contato
    dados_para_handler["primeiro_contato_tipo"] = primeiro_contato_tipo
    dados_para_handler["falta_na_jogada"] = falta_na_jogada
    dados_para_handler["bolas_atribuidas"] = bolas_atribuidas
    dados_para_handler["turno_jogador"] = turno_jogador
    dados_para_handler["jogador1_grupo"] = jogador1_grupo
    dados_para_handler["jogador2_grupo"] = jogador2_grupo
    # Atualiza a física do Pymunk
    espaco.step(1 / 60.0)

    #agora a gente recupera as informações para ver se alguma coisa mudou 
    primeiro_contato = dados_para_handler["primeiro_contato"]
    primeiro_contato_tipo = dados_para_handler["primeiro_contato_tipo"]
    falta_na_jogada = dados_para_handler["falta_na_jogada"]
    
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
            grupo_atual = jogador1_grupo if turno_jogador == 1 else jogador2_grupo

            # verifica quantas bolas do jogador atual ainda restam na mesa
            bolas_restantes = -1 
            if grupo_atual  == "pares":
                bolas_restantes = len(bolas_pares_em_jogo)
            elif grupo_atual == "impares":
                bolas_restantes = len(bolas_impares_em_jogo)
            
            #avalia o resultado 
            if grupo_atual is None:
                #se os grupos nem foram definidos ainda e ele matou a 1: Perdeu 
                print(f"jogador {turno_jogador} perdeu a partida! (matou a 1 sem definir os grupos)")
                vencedor = 2 if turno_jogador == 1 else 1
                ESTADO_JOGO = "FIM_DE_JOGO"
            elif bolas_restantes == 0:
                #Se o jogador já terminou de matar as bolas dele, vitoria!
                print(f'Jogador {turno_jogador} ganhou a partida!!! ')
                vencedor = turno_jogador
                ESTADO_JOGO = "FIM_DE_JOGO"
            else: 
                #se ainda sobrar bolas no grupo dele: derrota
                print(f'O jogador {turno_jogador} perdeu! ainda tinha bolas na mesa e mesmo assim matou a 1.')
                vencedor = 2 if turno_jogador == 1 else 1
                ESTADO_JOGO = "FIM_DE_JOGO"





        elif numero % 2 != 0: # a bola é impar 
            if numero in bolas_impares_em_jogo:
                bolas_impares_em_jogo.remove(numero)
        else: #a bola é par 
            if numero in bolas_pares_em_jogo:
                bolas_pares_em_jogo.remove(numero)
        #Fim da mecânica de encaçapamento das bolas. 
        
    #Seção de desenho( os desenhos são atualizados no fim para evitar conflitos)
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
        #primeiro pega a posicao da bola para poder desenha-la no jogo
        pos = (int(forma.body.position.x), int(forma.body.position.y))
        #Depois a gente desenha o circulo mais externo
        pygame.draw.circle(tela, forma.color, pos, raio_bola)
        #Agora a gente tem que desenhar o numero da bola, vamos usar um condicional pra isso caralho
        if forma.numero is not None:
            #primeiro temos que sedenhar o circulo branco na forma da bola, pra isso precisamos definir o raio desse circulo branco, quero que o diametro desse circulo branco seja do tamanho da bola branca, por que? por que sim uai.  
            pygame.draw.circle(tela, BRANCO, pos, 9)
            #agora a gente tem que renderizar o texto na bola ou seja o numero da bola (eu vou conseguir passar nessa materia). 
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
    #se as bolas foram definidas desenha na tela um texto simples falando qual é a bola de cada um 
    if bolas_atribuidas:
        font_marcacao = pygame.font.SysFont("Arial", 30, bold = True)
        texto_jogador1 = font_marcacao.render(f"Jogador 1:{'Pares' if jogador1_grupo == 'pares' else 'impares'}", True, PRETO, cor_da_tabela)
        tela.blit(texto_jogador1, (100, altura -65))
        texto_jogador2 = font_marcacao.render(f"Jogador 2: {'Impares' if jogador2_grupo == 'impares' else 'pares'}", True, PRETO, cor_da_tabela)
        tela.blit(texto_jogador2,(largura/2 + 70, altura -65))
    #desenha uma mensagem simples na tela quem ganhou o jogo 
    if ESTADO_JOGO == "FIM_DE_JOGO":
        font_vitoria = pygame.font.SysFont("Arial", 50, bold = True)
        texto = font_vitoria.render(f"JOGADOR {vencedor} VENCEU!", True, PRETO, VERDE)
        tela.blit(texto, (largura/2 -200, altura/2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()