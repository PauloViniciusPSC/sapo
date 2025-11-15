import pymunk

#aqui a gente vai fazer toda a logica do jogo né 
# Em: logica_jogo.py
import pymunk

def handler_primeiro_contato(arbitro, espaco, data):
    """
    Essa função vai ser chamada sempre que uma colisão ocorrer no jogo. 
    O objetivo dela aqui, é o de detectar quando um jogador comete uma falta. 
    Essas faltas em especifico são os seguintes casos:
    1 - O jogador que está na tacada, se nenhuma bola caiu ainda e o jogador atingir a bola 1, de forma direta o jogador que não está na jogada ganha.
    2 - Se o jogador na tacada não acertar nenhuma bola e estiver no estouro, ou então se nenhum matou nenhuma bola ainda no jogo, nenhuma falta é cometida nesse caso e o jogador simplesmente passa a tacada 
    3 - Se no jogo as bolas de cada jogador já estão definidas, e um dos jogadores após realizar a sua tacada comete falta com penalidade nas seguintes condições:
        3.a: Se ele acertar uma das bolas do oponente de forma direta, uma falta é cometida, e então as duas bolas de menor número do jogador que  nao está na tacada e o jogador tem que passar a vez.
        3.b: Se ele acertar uma das bolas do oponente de forma indireta: Só ocorre se e somente se a bola branca primeiro acerte uma tabela e então acerte uma das bolas do outro jogador. Nesse caso cai a bola de menor número do outro jogador e o jogador que estava na tacada tem que passar a vez. 

    data: é um dicionario que contem as informaçoes que vao ser utilizadas para tratar as colisões no jogo
    arbitro: é basicamente um arbitro que vai fazer o julgamento da tacada, de forma imparcial é claro.
    espaco: é o "espaco fisico" sobre o qual o jogo vai atuar.

    """
    
    # Pega as variáveis do dicionário 'data'
    estado_jogo = data["ESTADO_JOGO"]
    primeiro_contato = data["primeiro_contato"]
    primeira_tacada_feita = data["primeira_tacada_feita"]
    turno_jogador = data["turno_jogador"]

    # Só faz algo se for a PRIMEIRA colisão desta jogada
    # (Ou seja, se ainda não registramos nenhum contato)
    if primeiro_contato is None:
        forma_branca, forma_colorida = arbiter.shapes

        # Garante que pegamos a forma colorida corretamente
        # (Assumiremos que 1 é o tipo da branca, 2 da colorida)
        if forma_branca.collision_type != 1: 
            forma_branca, forma_colorida = forma_colorida, forma_branca

        # Pega o número da bola tocada
        num_bola_tocada = forma_colorida.numero
        
        # ATUALIZA o dicionário 'data' com o primeiro contato
        data["primeiro_contato"] = num_bola_tocada 
        print(f"Primeiro contato com a bola: {num_bola_tocada}")

        # --- VERIFICA A REGRA DO ESTOURO ---
        # Se for a primeira tacada E o primeiro contato foi com a bola 1
        if not primeira_tacada_feita and num_bola_tocada == 1:
            print(f"FALTA GRAVE NO ESTOURO! Jogador {turno_jogador} atingiu a bola 1 primeiro.")
            
            # ATUALIZA o dicionário 'data' com o fim do jogo
            data["ESTADO_JOGO"] = "FIM_DE_JOGO" 
            data["vencedor"] = 2 if turno_jogador == 1 else 1 
            print(f"Jogador {data['vencedor']} venceu!")
            
            # Retorna False para que a física ignore esta colisão (opcional, mas evita bugs)
            return False 
        # a partir daqui a gente faz o tratamento para os outros casos 2 e 3a e 3b. 
        #Se não for a primeira tacada e o primeiro contato da bola branca foi com uma bola do adversário:
            #apontamos a penalidade e 0



        #Se não foi a primeira tacada e o primeiro contato da bola branca foi com uma das tabelas e depois com uma das bolas do adversário 

    # Retorna True para que a física processe a colisão normalmente
    return True