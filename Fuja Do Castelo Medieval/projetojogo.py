import time
import platform
import random
import subprocess
import sys
from itens import allitems

if platform.system() == 'Windows':
    if 'curses' not in sys.modules:
        subprocess.check_call(['pip', 'install', 'windows-curses'])
    import curses
else:
    import curses



salas_ja_visitadas = []
reliquias = []
inventario = {'cura': 20, 'espada': 1, 'túnica de peles': 1}
life = 100
damage = 10
moedas = 100
chance_critico = 0.2 #30% de chance de dano crítico
chance_errar = 0.3 #50% de chance de errar

def tamanhojanela(stdscr):
    """Define o tamanho da janela!"""
    a = 37 #meio tem valor igual a 19
    b = 139 #meio tem valor igual a 70
    return(a, b)

def menuinicial(stdscr):
    """Menu Inicial"""
    curses.curs_set(0) #serve para esconder o cursor
    stdscr.clear()
    stdscr.refresh()

    botoes = ['Inicio', 'Sair']
    pos_y = 0

    sh, sw = tamanhojanela(stdscr)

    titulo = [
        ' ___ _   _    _  _     ___   ___     ___   _   ___ _____ ___ _    ___ ',
        '| __| | | |_ | |/_\   |   \ / _ \   / __| /_\ / __|_   _| __| |  / _ \ ',
        '| _|| |_| | || / _ \  | |) | (_) | | (__ / _ \\__  \ | | | _|| |_| (_) |  ',
        '|_|  \___/ \__/_/ \_\ |___/ \___/   \___/_/ \_\___/ |_| |___|____\___/',
        '                                                                       ',
        '                __  __ ___ ___ ___ _____   ___   _',
        '               |  \/  | __|   \_ _| __\ \ / /_\ | |',
        '               | |\/| | _|| |) | || _| \ V / _ \| |__',
        '               |_|  |_|___|___/___|___| \_/_/ \_\____|',
    ]

    imagem = [
        "                         ._-_.",
        "                         |_-_(",
        "                         I",
        "                        /_\ ___",
        "            ._-_.   |,|/   \ ",
        "            |_-_(   | /_____\       ._-_.",
        "            I        \| u  -| _     |_-_(",
        "           / \    -_-_-_-_--|/ \    I",
        "          /___\   \._._._./-|___\  / \ ",
        "          |_u |    |_   _| -| u_| /___\ ",
        "          |_-_-_-_-_-  U_| -|  _| | u_|",
        "          |_\._._._./   _|-_-_-_-_-_-_|",
        "           \_|-   -|    _|    ..   -|_|",
        "            \|-   U|    _| U  ++  U-|/",
        "             |U   -|  U _|   ____  -|",
        "             |- _ -|    _|  /|-|-\ -|",
        "             |-/#\-|    _|  |-|-|| -|",
        "         ,___|_MEB_|-----'__I|-|-I__|__,",
        "      ._/ /                 \____/      \,",
        "     /  \ \                  \```\        \,",
        "    (__   _\                 |'''|         L_,",
        "    /   ./ /                  \```\       /  _\ ",
        "   |   /  /                   |'''|       \,   |",
        "   /  (                       \```\       /  _/ \ ",
        "  /_                           |'''|           _,|",
        " |                                                \ ",
    ]

    ytitul = (sh // 2) - 7
    xtitul = (sw - len(titulo[0]))//2

    try: 
        janela = curses.newwin(sh, sw, 0, 0)
        janela.border()
        janela.keypad(True)

        for linha in range(len(titulo)):
            janela.addstr(ytitul + linha, xtitul, titulo[linha])
            janela.refresh()
            time.sleep(0.1)

        for linha in range(len(imagem)):
            stdscr.addstr(sh//2 - 8 + linha, 1, imagem[linha])
            stdscr.refresh()
            time.sleep(0.1)

        while True:

            for i in range(len(botoes)):
                if pos_y == i:
                    janela.addstr(ytitul + 15 + i, (sw - len(botoes[i]))//2, botoes[i], curses.A_STANDOUT)
                else:
                    janela.addstr(ytitul + 15 + i, (sw - len(botoes[i]))//2, botoes[i])

            janela.refresh()
            tecla = janela.getch()  

            if tecla == curses.KEY_UP and pos_y > 0 or tecla == 450 and pos_y > 0:
                pos_y += -1
            
            if tecla == curses.KEY_DOWN and pos_y < len(botoes) - 1 or tecla == 456 and pos_y < len(botoes) - 1:
                pos_y += 1

            if tecla == 10 or tecla == curses.KEY_ENTER:
                aux = botoes[pos_y]
                if aux == botoes[0]:
                    main(stdscr)
                    break
                else:
                    break

    except curses.error:
        y, x = stdscr.getmaxyx()
        mensagem = 'Por favor, maximize a janela do terminal para o jogo rodar.'
        stdscr.clear()
        stdscr.addstr(y//2, (x - len(mensagem))//2, mensagem)
        stdscr.refresh()

        while y < 37 and  x < 139:
            stdscr.clear()
            stdscr.addstr(y//2, (x - len(mensagem))//2, mensagem)
            stdscr.refresh()
            y, x = stdscr.getmaxyx()

            key = stdscr.getch()
            if key == curses.KEY_RESIZE:
                menuinicial(stdscr)
                break


def main(stdscr):
    """Tela principal do jogo. Onde aparece o mapa, inventário e vida. Aqui também é definido o movimento"""
    global reliquias
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    matriz = [
        ['entrada','ponte', 'corredor', 'baú', 'biblioteca'],
        ['torre', 'armaria real', 'corredor2', 'salão comunal', 'torre2'],
        ['calabouço', 'quarto real', 'corredor3', 'trono real', 'biblioteca2'],
        ['celas','capela', 'corredor4', 'jardim real', 'muralha fortificada'],
        ['feudo', 'sala de armadilhas', 'poço dos desejos', 'chafariz monumental', 'saída'],
    ]

    sh, sw = tamanhojanela(stdscr)
    pos_x = 0
    pos_y = 0

    display = curses.newwin(sh // 2 + 6, sw // 2 - 1, sh * 3 // 10, sw // 2)
    janela = curses.newwin(sh, sw, 0, 0)
    janela_action = curses.newwin(sh // 3 - 3, sw // 2 - 1, (sh * 3 // 4) - 1, 1)
    janela_info = curses.newwin(sh // 2 - 5, sw // 2 - 1, sh // 2 - 7, 1)
    janela_info2 = curses.newwin(sh // 2 - 8, sw // 2 - 4, sh // 2 - 5, 2)  # Essa janela que vai receber os textos

    display.border()
    janela.border()
    janela_action.border()
    janela_info.border()

    janela.keypad(True)
    janela_action.keypad(True)
    janela_info.keypad(True)

    try:
        if len(reliquias) == 3:
            inventario['túnica rubro negra'] = 1
            popup('item', 'túnica rubro negra', 1)
            del inventario['relíquia da família real']
            del inventario['relíquia do clérigo']
            del inventario['relíquia dos ancestrais']
            del reliquias
    except:
        pass
        

    # Loop principal
    while True:
        janela.addstr(2, 2, 'Vida: {}'.format(life))
        janela.addstr(2, sw - 20, 'Moedas: {}'.format(moedas))
        janela_info.addstr(1, 1, 'Informações: ')

        # Serve para apagar a info/display assim que passo para a sala seguinte e mostra a info da sala nova
        janela_info2.clear()
        janela_action.clear()
        display.clear()
        
        janela_action.addstr(1, 1, 'Ação: ')
        janela_action.border()
        display.border()

        # Mostrar a matriz e o lugar selecionado
        for linha in range(len(matriz)):
            for coluna in range(len(matriz[linha])):
                if pos_y == linha and pos_x == coluna:
                    janela.addstr(linha + 5, sw // 18 + coluna * (sw // 5), matriz[linha][coluna], curses.A_STANDOUT)
                    janela_info2.addstr(1, 0, infosalas(matriz[linha][coluna]))
                    room = matriz[linha][coluna]
                else:
                    janela.addstr(linha + 5, sw // 18 + coluna * (sw // 5), matriz[linha][coluna])

        # Mostrar o preview de cada sala
        # TEM VÁRIOS ERROS AQUI
        with open('preview_salas.txt', 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()

        linhas = conteudo.strip().split('\n')

        contadordelinhas = 0
        # EXISTEM VÁRIOS ERROS NESSE LOOP.
        for linha in linhas:
            contadordelinhas += 1
            linha = linha.strip()
            if not linha:
                continue

            if linha.endswith(':'):
                if linha[:-1] == room:
                    aux = 0
                    for i in range(contadordelinhas, len(linhas)):
                        if linhas[i].endswith(':'):
                            break
                        else:
                            display.addstr(1 + aux, 1, linhas[i])
                        aux += 1
                else:
                    continue

        janela.refresh()
        janela_action.refresh()
        janela_info.refresh()
        janela_info2.refresh()
        display.refresh()

        # Chamar a função para capturar a ação do usuário
        action = menuacao(stdscr, "principal", janela_action)

        if action.lower() in ['l', 'leste'] and pos_x < len(matriz[0]) - 1:
            pos_x += 1

        if action.lower() in ['o', 'oeste'] and pos_x > 0:
            pos_x -= 1

        if action.lower() in ['n', 'norte'] and pos_y > 0:
            pos_y -= 1

        if action.lower() in ['s', 'sul'] and pos_y < len(matriz) - 1:
            pos_y += 1

        if action.lower() in ['esc', 'sair']:
            menuinicial(stdscr)
            break

        if action.lower() in ['gear', 'equipamento']:
            gear(stdscr, inventario, 10)
            break

        if action.lower() == 'entrar':
            aux = matriz[pos_y][pos_x]
            salas(stdscr, aux)
            break


def popup(tipo = None, valor = None, qtd = None, stdscr = None):
    janela_popup = curses.newwin(10, 40, 13, 45)
    janela_popup.border()
    
    match tipo:

        case 'ataque':
            janela_popup.addstr(1, 1, f'Você deu {valor} de dano ao inimigo!')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)

        case 'chave':
            janela_popup.addstr(1, 1, f'Você precisa da {valor}')
            janela_popup.addstr(2, 1, 'para entrar nessa sala!') 
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)

        case 'comprou':
            janela_popup.addstr(1, 1, f'Você comprou')
            janela_popup.addstr(2, 1, f'{valor} ({qtd})') 
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)

        case 'dano_recebido':
            janela_popup.addstr(1, 1, f'Você recebeu {valor} de dano do inimigo!')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)
        
        case 'item':
            janela_popup.addstr(1, 1, f'Você recebeu {valor}! ({qtd})')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4) 

        case 'errou':
            janela_popup.addstr(1, 1, f'Tente novamente!')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)
        
        case 'equipar':
            janela_popup.addstr(1, 1, f'Você equipou {valor}!')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)
        
        case 'moeda':
            janela_popup.addstr(1, 1, f'Você recebeu {valor} moedas!')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)

        case 'n_equipou':
            janela_popup.addstr(1, 1, f'{valor.title()} não está no seu inventário')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)

        case 'visited':
            janela_popup.addstr(1, 1, 'Sala já visitada!')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)
        
        case 'saída':
            janela_popup.addstr(1, 1, 'Você precisa visitar')
            janela_popup.addstr(2, 1, 'todas as salas para sair!')
            janela_popup.addstr(5, 1, f'Ainda faltam {17 - len(salas_ja_visitadas)} salas!')
            janela_popup.addstr(7, 1, 'Você precisa da chave mestra também!')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)
        
        case 'sala_vazia':
            janela_popup.addstr(1, 1, 'Sala Vazia!')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.6)

        case 'sem_moedas':
            janela_popup.addstr(1, 1, 'Sem moedas o suficiente!')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.6)

        case 'vitoria':
            janela_popup.addstr(1, 1, 'Você derrotou seu inimigo!')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)

        case'gameover':
            janela_popup.addstr(1, 1, 'GAME OVER')
            janela_popup.addstr(3, 1, 'Você foi derrotado!')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)
            quit()
            
        
        case 'inimigo_errou':
            janela_popup.addstr(1, 1, 'Seu inimigo errou o ataque!')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)
        
        case 'errou_ataque':
            janela_popup.addstr(1, 1, 'Você errou seu ataque!')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)

        case 'critical':
            janela_popup.addstr(1, 1, 'DANO CRÍTICO!')
            janela_popup.addstr(3, 1, f'Você deu {valor} de dano ao inimgo')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)
        
        case 'enemy_critical':
            janela_popup.addstr(1, 1, 'DANO CRÍTICO DO INIMIGO!')
            janela_popup.addstr(2, 1, f'Você recebeu {valor} de dano do inimigo')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)

        case 'curou':
            janela_popup.addstr(1, 1, f'Você curou {valor} de vida!')
            janela_popup.refresh()
            janela_popup.clear()
            time.sleep(1.4)

        case 'zerou':
            janela_popup = curses.newwin(37, 139, 0, 0)
            janela_popup.border()
            imagem_final = [
                "                            ==(W{==========-      /===-                        ",
                "                              ||  (.--.)         /===-_---~~~~~~~~~------____  ",
                "                              | \_,|**|,__      |===-~___                _,-' `",
                "                 -==\\        `\ ' `--'   ),    `//~\\   ~~~~`---.___.-~~  ",
                "             ______-==|        /`\_. .__/\ \    | |  \\           _-~` ",
                "       __--~~~  ,-/-==\\      (   | .  |~~~~|   | |   `\        ,'",
                "    _-~       /'    |  \\     )__/==0==-\<>/   / /      \      /",
                "  .'        /       |   \\      /~\___/~~\/  /' /        \   /'",
                " /  ____  /         |    \`\.__/-~~   \  |_/'  /          \/'",
                "/-'~    ~~~~~---__  |     ~-/~         ( )   /'        _--~`  ",
                "                  \_|      /        _) | ;  ),   __--~~  ",
                "                    '~~--_/      _-~/- |/ \   '-~ \     ",
                "                   {\__--_/}    / \\_>-|)<__\      \   ",
                "                   /'   (_/  _-~  | |__>--<__|      | ",
                "                  |   _/) )-~     | |__>--<__|      |",
                "                  / /~ ,_/       / /__>---<__/      |",
                "                 o-o _//        /-~_>---<__-~      / ",
                "                 (^(~          /~_>---<__-      _-~ ",
                "                ,/|           /__>--<__/     _-~  ",
                "             ,//('(          |__>--<__|     /                  .----_     ",
                "            ( ( '))          |__>--<__|    |                 /' _---_~\   ",
                "         `-)) )) (           |__>--<__|    |               /'  /     ~\`\  ",
                "        ,/,'//( (             \__>--<__\    \            /'  //        ||    ",
                "      ,( ( ((, ))              ~-__>--<_~-_  ~--____---~' _/'/        /'  ",
                "    `~/  )` ) ,/|                 ~-_~>--<_/-__       __-~ _/     ",
                "  ._-~//( )/ )) `                    ~~-'_/_/ /~~~~~~~__--~    ",
                "   ;'( ')/ ,)(                              ~~~~~~~~~~     ",
                "  ' ') '( (/ ",
                "    '   '  `",
            ]

            for linha in range(len(imagem_final)):
                janela_popup.addstr(1 + linha, 10, imagem_final[linha])
                janela_popup.refresh()
                time.sleep(0.1)
            time.sleep(1.4)
            quit()



def menuacao(stdscr, check, window, room=None):
    """Aqui vai ser recebido os comando de texto que serão executados.
    Comandos como usar itens, armaduras, atacar, defender, etc.
    """
    global life
    janela = window
    janela.border()
    janela.keypad(True)
    janela.addstr(1, 1, 'Ação: ')
    curses.curs_set(2)

    curses.echo()  # Essa função permite o input do usuário aparecer na janela
    texto = janela.getstr(2, 1)  # Essa função permite o input do usuário
    curses.noecho()  # Essa função desabilita a exibição do texto
    
    # Conversão para string
    texto = texto.decode().strip()
    partes = texto.split()
            
    #essa fução concatena em "string" tudo que vem depois de equipar
    if 'equipar' in partes:
        string = ' '.join(partes[1:])
        equipamento(string)

    if 'pólen' in partes:
        if 'frasco de pólen' in inventario:
            if life + 50 > 100:
                life += (100 - life)
                inventario['frasco de pólen'] -= 1
                if inventario['frasco de pólen'] == 0:
                    del inventario['frasco de pólen']
            else: 
                life += 50
                inventario['frasco de pólen'] -= 1
                if inventario['frasco de pólen'] == 0:
                    del inventario['frasco de pólen']
            popup('curou', 50)

    if check == "principal":
         if texto.lower() == 'curar' and life < 100:
            if life + 20 > 100:
                life += (100 - life)
                inventario['cura'] -= 1
            else: 
                life += 20
                inventario['cura'] -= 1
            popup('curou', 20)
            return texto
         else:
            return texto

    if check == "sala":
        if texto.lower() == 'curar' and life < 100:
            if life + 20 > 100:
                life += (life + 20) - 100
                inventario['cura'] -= 1
            else: 
                life += 20
                inventario['cura'] -= 1
            popup('curou', 20)
            return texto

        else:
            return texto
    

def combate(dano_do_inimigo, damage, chance_critico, chance_errar):
    numero_aleatorio = random.random() #gera um número entre 0 e 1
    numero_aleatorio2 = random.random()

    dano_feito = damage
    dano_levado = dano_do_inimigo

    if numero_aleatorio < chance_errar:
        dano_feito = 0

    if numero_aleatorio < chance_critico:
        dano_feito = damage * 2

    if numero_aleatorio2 < chance_errar:
        dano_levado = 0
    
    if numero_aleatorio2 < chance_critico:
        dano_levado = dano_do_inimigo * 2

    return dano_feito, dano_levado


        
def equipamento(item = None):
    """função para ver quais itens estão equipados"""
    global arma, defense, damage, life 
    if item in inventario:
        inventario[item] -= 1
        tipo = allitems[item]['type']
        descricao = allitems[item]['description']
        popup('equipar', item)

        if tipo == 'melee':
            dano = allitems[item]['value']
            damage += dano
            arma = (tipo, item, descricao, dano)
        elif tipo == 'armor':
            defesa = allitems[item]['value']
            if life < 100:
                life += defesa
            else:
                life = 100 + defesa
            defense = (tipo, item, descricao, defesa)
        if inventario[item] == 0:
            del inventario[item]

    else:
        popup('n_equipou', item)
        pass
        

def gear(stdscr, mochila = None, keypressed = None):
    """Mostra o inventário e equipamentos do personagem"""
    curses.curs_set(0)
    if keypressed:
        sh, sw = tamanhojanela(stdscr)

        yjanela = sh//2
        xjanela = sw//2
        janela = curses.newwin(yjanela, xjanela, yjanela//2, 10)
        janela_equipamento = curses.newwin(yjanela, xjanela//2, yjanela//2, xjanela + 10) 
        janela.keypad(True)

        status = [
        "   .-. ",
        " __|=|__ ",
        "(_/`-`\_)",
        "//\___/\\\ ", 
        "_________",
        f"vida: {life}",
        ]

        while True:
            janela.clear()
            janela_equipamento.clear()
            janela_equipamento.border()
            janela.border()
            janela.addstr(1, 1, 'Inventário: ')

            for i, (elemento, valor) in enumerate(mochila.items()):
                aux = f'{elemento}: {valor}'
                try:
                    janela.addstr(3 + i, 1, aux, curses.A_BOLD)
                except:
                    janela.addstr(3 + i, 15, aux, curses.A_BOLD)

            for i in range(len(status)):
                janela_equipamento.addstr(1 + i, 12, status[i])
            
            try:
                janela_equipamento.addstr(8, 1, f'ARMA: {arma[1]}')
                janela_equipamento.addstr(9, 1, f'dano: {arma[3]}')
                janela_equipamento.addstr(10, 1, f'descrição: {arma[2]}')
            except: 
                janela_equipamento.addstr(8, 1, f'ARMA: ')

            try:
                janela_equipamento.addstr(12, 1, f'ARMADURA: {defense[1]}')
                janela_equipamento.addstr(13, 1, f'defesa: {defense[3]}')
                janela_equipamento.addstr(14, 1, f'descrição: {defense[2]}')
            except:
                janela_equipamento.addstr(12, 1, f'ARMADURA: ')
                
            janela_equipamento.refresh()
            janela.refresh()
            key = janela.getch()
            if key == 27: #TECLA ESC
                main(stdscr)
                break
        
    return mochila   


def refresher(janelas):
    for i in range(len(janelas)):
        janelas[i].clear()
        janelas[i].border()
        janelas[i].refresh()



def infosalas(sala):
    """Informação de cada sala"""
    #NOMES IGUAIS ESTÃO DANDO CONFUSÃO NA HORA DE MOSTRAR A INFO DELES
    with open('descricao_salas.txt', 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()
    
    #serve para separar o conteúdo (string que contém as infos) em linhas quando tem espaço em branco (tipo enter)
    linhas = conteudo.strip().split('\n') 
    

    info_salas = {} #Esse dicionário está armazenando todas as informações do arquivo de texto
    chave = None #chave aqui se refere à sala e é auxiliar para colocar os itens no dicionário
    valor_acumulado = [] #valor aqui se refere às informações das salas
    
    #Esse loop funciona da seguinte forma:
    #O arquivo de texto está organizado como um dicionário. Daí, as chaves lá estão delimitadas com ':' 
    #seguidas de um ENTER (para pular linha (ver arquivo em caso de dúvida)).
    #A partir disso, o loop para cada linha nesse arquivo, vai verificar se essa termina em ':'
    #Caso termine, é uma chave então.
    #A partir daí o loop vai verificar se cada linha seguinte termina com ':'. Se não, essa linha é
    #appendada na lista de valor_acumulado pois se refere ao valor da chave encontrada.
    #Se encontrar outra linha que termine com ':', quer dizer que encontrou outra chave.
    #Daí o loop vai então direcionar todo aquele valor_acumulado para a chave anterior e resetar o processo com
    #a nova chave. Por conta disso, a última chave ficaria sem seu valor. Dái vem o if debaixo para appendar
    #esse valor.
    for linha in linhas:

        #Tem que tirar os espaços do inicio e do final da string se não appenda apenas uma chave e o restante do texto
        #se torna o valor da primeira chave
        linha = linha.strip() 
        if not linha:  #se a linha estiver vazia, vai continuar para a próxima linha
            continue

        if linha.endswith(':'):
            if chave:
                info_salas[chave] = ' '.join(valor_acumulado).strip()
            chave = linha[:-1].strip()
            valor_acumulado = []
        else:
            valor_acumulado.append(linha.strip())

    if chave:
        info_salas[chave] = ' '.join(valor_acumulado).strip()

   
    return info_salas.get(sala, 'Sem informações')
        

def salas(stdscr, room = None, save= None):
    """Janela que vai servir pra mostrar os conteúdos de uma sala"""
    global life, moedas
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()

    sh, sw = tamanhojanela(stdscr)
    
    janela = curses.newwin(sh, sw, 0, 0)

    janela.border()
    janela.keypad(True)

    with open('conteudos_salas.txt', 'r', encoding='utf-8') as arquivo:
        conteudo = arquivo.read()
        
    linhas = conteudo.strip().split('\n')

    contadordelinhas = 0
    maiorlinha = ''
    for linha in linhas:
        contadordelinhas += 1
        linha = linha.strip()
        if not linha:
            continue
        
        if linha.endswith(':'):
            if linha[:-1] == room:
                aux = 0
                for i in range(contadordelinhas, len(linhas)): 
                    if linhas[i].endswith(':'):
                        break
                    else:
                        janela.addstr(1 + aux, 1, linhas[i])
                        if len(linhas[i]) > len(maiorlinha):
                            maiorlinha = linhas[i]
                    aux += 1
            else:
                continue

    janela_action = curses.newwin(sh//3 - 4, sw - len(maiorlinha) - 2, 1, len(maiorlinha) + 1)
    janela_status = curses.newwin(sh//3 - 3, sw - len(maiorlinha) - 2, sh//3 - 2, len(maiorlinha) + 1)
    janela_inventario = curses.newwin(sh - (2*sh//3 - 4), sw - len(maiorlinha) - 2, sh//2 + 1, len(maiorlinha) + 1)
    
    janela_action.border()
    janela_status.border()
    janela_inventario.border()
    
    janela_action.addstr(1, 1, 'Ação:')
    janela_status.addstr(1, 1, 'Status:')
    janela_inventario.addstr(1, 1, 'Inventário:')

    status = [
        "   .-. ",
        " __|=|__ ",
        "(_/`-`\_)",
        "//\___/\\\ ", 
    ]

    for i in range(len(status)):
        janela_status.addstr(1 + i, 1, status[i])
    
    try:
        janela_status.addstr(1, 13, f'ARMA: {arma[1]}')
        janela_status.addstr(2, 13, f'dano:{arma[3]}')
        janela_status.addstr(3, 13, f'descrição: {arma[2]}')
    except: 
        janela_status.addstr(1, 13, f'ARMA: ')

    try:
        janela_status.addstr(5, 13, f'ARMADURA: {defense[1]}')
        janela_status.addstr(6, 13, f'defesa:{defense[3]}')
        janela_status.addstr(7, 13, f'descrição: {defense[2]}')
    except:
        janela_status.addstr(5, 13, f'ARMADURA: ')

    janela_status.addstr(len(status) + 2, 1, f'Moedas: {moedas}')
    janela_status.addstr(len(status) + 3, 1, f'Vida: {life}')

    for i, (elemento, valor) in enumerate(inventario.items()):
        aux = f'{elemento}: {valor}'
        janela_inventario.addstr(3 + i, 1, aux, curses.A_BOLD) 

    match room:
        case 'entrada':
            popup('sala_vazia')
            main(stdscr)

        case 'ponte':
            if 'ponte' not in salas_ja_visitadas:
                if save:
                    enemy_life = save
                else:
                    enemy_life = 50
                dano_do_inimigo = 15
                while True:
                    janela.addstr(sh - 2, 2, f"vida: {enemy_life}")
                    janela_status.addstr(len(status) + 3, 1, f'Vida: {life}')
                    for i in range(len(status)):
                        janela_status.addstr(1 + i, 1, status[i])

                    janela_inventario.addstr(1, 1, 'Inventário:')
                    for i, (elemento, valor) in enumerate(inventario.items()):
                        aux = f'{elemento}: {valor}'
                        janela_inventario.addstr(3 + i, 1, aux, curses.A_BOLD) 
                    
                    janela.refresh()
                    janela_action.refresh()
                    janela_inventario.refresh()
                    janela_status.refresh()

                    action = menuacao(stdscr, "sala", janela_action, room)
                    dano_feito, dano_levado = combate(dano_do_inimigo, damage, chance_critico, chance_errar)
                    
                    if action.lower() == 'atacar':
                        if dano_feito == 0:
                            popup('errou_ataque')
                        elif dano_feito == damage * 2.0:
                            popup('critical', dano_feito)
                            enemy_life -= dano_feito
                        else:
                            enemy_life -= dano_feito
                            popup('ataque', dano_feito)

                    if enemy_life <= 0:
                        popup('vitoria')
                        salas_ja_visitadas.append('ponte')
                        inventario['cura'] += 5
                        moedas += 50
                        popup('moeda', 50)
                        popup('item', 'cura', 5)
                        main(stdscr)
                        break
                    
                    if dano_levado == 0:
                        popup('inimigo_errou')
                    
                    if dano_levado == dano_do_inimigo * 2.0:
                        popup('enemy_critical', dano_levado)
                        life -= dano_levado
                    else:
                        life -= dano_levado
                        popup('dano_recebido', dano_levado)
                    
                    if life < 0:
                        popup('gameover', stdscr=stdscr)
                        break
                
                    salas(stdscr, room='ponte', save=enemy_life)
            
            else:
                popup('visited')
                main(stdscr)

        case 'baú':
            if 'baú' not in salas_ja_visitadas:
                while True:
                    janela.refresh()
                    janela_action.refresh()
                    janela_inventario.refresh()
                    janela_status.refresh()

                    janela_action.addstr(1, 1, 'Ação:')
                    janela_status.addstr(1, 1, 'Status:')
                    janela_inventario.addstr(1, 1, 'Inventário:')
                    
                    action = menuacao(stdscr, "sala", janela_action, room)

                    
                    if action.lower() == '2123ond':
                        moedas += 200
                        popup('moeda', 200)
                        inventario['cura'] += 5
                        popup('item', 'cura', 5)
                        janela_inventario.refresh()
                        salas_ja_visitadas.append('baú')
                        main(stdscr)
                        break
                    elif action.lower() == 'sair':
                        main(stdscr)
                        break
                    else:
                        popup('errou')
                        salas(stdscr, 'baú')
            else:
                popup('visited')
                main(stdscr)
        

        case 'corredor':
            if 'corredor' not in salas_ja_visitadas:
                if save:
                    enemy_life = save
                else:
                    enemy_life = 100
                dano_do_inimigo = 25
                while True:
                    janela.addstr(sh - 2, 2, f"vida: {enemy_life}")
                    janela_status.addstr(len(status) + 3, 1, f'Vida: {life}')
                    for i in range(len(status)):
                        janela_status.addstr(1 + i, 1, status[i])

                    janela_inventario.addstr(1, 1, 'Inventário:')
                    for i, (elemento, valor) in enumerate(inventario.items()):
                        aux = f'{elemento}: {valor}'
                        janela_inventario.addstr(3 + i, 1, aux, curses.A_BOLD) 
                    
                    janela.refresh()
                    janela_action.refresh()
                    janela_inventario.refresh()
                    janela_status.refresh()

                    action = menuacao(stdscr, "sala", janela_action, room)
                    dano_feito, dano_levado = combate(dano_do_inimigo, damage, chance_critico, chance_errar)
                    
                    if action.lower() == 'atacar':
                        if dano_feito == 0:
                            popup('errou_ataque')
                        elif dano_feito == damage * 2.0:
                            popup('critical', dano_feito)
                            enemy_life -= dano_feito
                        else:
                            enemy_life -= dano_feito
                            popup('ataque', dano_feito)

                    if enemy_life <= 0:
                        popup('vitoria')
                        salas_ja_visitadas.append('corredor')
                        inventario['capa do drácula'] = 1
                        inventario['cura'] += 5
                        moedas += 100
                        popup('moeda', 100)
                        popup('item', 'capa do drácula', 1)
                        popup('item', 'cura', 5)
                        main(stdscr)
                        break
                    
                    if dano_levado == 0:
                        popup('inimigo_errou')
                    
                    if dano_levado == dano_do_inimigo * 2.0:
                        popup('enemy_critical', dano_levado)
                        life -= dano_levado
                    else:
                        life -= dano_levado
                        popup('dano_recebido', dano_levado)
                    
                    if life < 0:
                        popup('gameover', stdscr=stdscr)
                        break
                
                    salas(stdscr, room='corredor', save=enemy_life)
            
            else:
                popup('visited')
                main(stdscr)
            
        case 'biblioteca':
            if 'biblioteca' not in salas_ja_visitadas:
                while True:
                    janela.refresh()
                    janela_action.refresh()
                    janela_inventario.refresh()
                    janela_status.refresh()

                    janela_action.addstr(1, 1, 'Ação:')
                    janela_status.addstr(1, 1, 'Status:')
                    janela_inventario.addstr(1, 1, 'Inventário:')

                    action = menuacao(stdscr, "sala", janela_action, room)

                    if action.lower() == 'rio':
                        inventario['chave riscada'] = 1
                        popup('item', 'chave riscada', 1)
                        salas_ja_visitadas.append('biblioteca')
                        main(stdscr)
                        break
                    elif action.lower() == 'sair':
                        main(stdscr)
                        break
                    else:
                        popup('errou')
                        salas(stdscr, 'biblioteca')
            else:
                popup('visited')
                main(stdscr)

        case 'torre':
            if 'torre' not in salas_ja_visitadas:
                if save:
                    enemy_life = save
                else:
                    enemy_life = 200

                dano_do_inimigo = 30
                while True:
                    janela.addstr(sh - 2, 2, f"vida: {enemy_life}")
                    janela_status.addstr(len(status) + 3, 1, f'Vida: {life}')
                    for i in range(len(status)):
                        janela_status.addstr(1 + i, 1, status[i])

                    janela_inventario.addstr(1, 1, 'Inventário:')
                    for i, (elemento, valor) in enumerate(inventario.items()):
                        aux = f'{elemento}: {valor}'
                        janela_inventario.addstr(3 + i, 1, aux, curses.A_BOLD) 
                    
                    janela.refresh()
                    janela_action.refresh()
                    janela_inventario.refresh()
                    janela_status.refresh()

                    action = menuacao(stdscr, "sala", janela_action, room)
                    dano_feito, dano_levado = combate(dano_do_inimigo, damage, chance_critico, chance_errar)
                    
                    if action.lower() == 'atacar':
                        if dano_feito == 0:
                            popup('errou_ataque')
                        elif dano_feito == damage * 2.0:
                            popup('critical', dano_feito)
                            enemy_life -= dano_feito
                        else:
                            enemy_life -= dano_feito
                            popup('ataque', dano_feito)

                    if enemy_life <= 0:
                        popup('vitoria')
                        salas_ja_visitadas.append('torre')
                        inventario['espada afiada'] = 1
                        moedas += 200
                        popup('item', 'espada afiada', 1)
                        popup('moeda', 200)
                        main(stdscr)
                        break
                    
                    if dano_levado == 0:
                        popup('inimigo_errou')
                    
                    if dano_levado == dano_do_inimigo * 2.0:
                        popup('enemy_critical', dano_levado)
                        life -= dano_levado
                    else:
                        life -= dano_levado
                        popup('dano_recebido', dano_levado)
                    
                    if life < 0:
                        popup('gameover', stdscr=stdscr)
                        break
                
                    salas(stdscr, room='torre', save=enemy_life)
            
            else:
                popup('visited')
                main(stdscr)

        case 'armaria real':
            if 'chave riscada' in inventario:
                while True:
                    janela.refresh()
                    janela_action.refresh()
                    janela_inventario.refresh()
                    janela_status.refresh()

                    janela_action.addstr(1, 1, 'Ação:')
                    janela_status.addstr(1, 1, 'Status:')
                    janela_inventario.addstr(1, 1, 'Inventário:')
                    
                    action = menuacao(stdscr, "sala", janela_action, room)
                    
                    match action:
                        case '1':
                            if moedas >= 1000:
                                moedas -= 1000
                                inventario['excalibur'] = 1
                                popup('comprou', 'excalibur', 1)
                                salas(stdscr, 'armaria real')
                            else:
                                popup('sem_moedas')
                                salas(stdscr, 'armaria real')

                        case '2':
                            if moedas >= 1000:
                                moedas -= 1000
                                inventario['armadura real'] = 1
                                popup('comprou', 'armadura real', 1)
                                salas(stdscr, 'armaria real')
                            else:
                                popup('sem_moedas')
                                salas(stdscr, 'armaria real')

                        case '3':
                            if moedas >= 500:
                                moedas -= 500
                                inventario['elmo e calça de cota de malha'] = 1
                                popup('comprou', 'elmo e calça de cota de malha', 1)
                                salas(stdscr, 'armaria real')
                            else:
                                popup('sem_moedas')
                                salas(stdscr, 'armaria real')

                        case '4':
                            if moedas >= 500:
                                moedas -= 500
                                inventario['arco e flecha'] = 1
                                popup('comprou', 'arco e flecha', 1)
                                salas(stdscr, 'armaria real')
                            else:
                                popup('sem_moedas')
                                salas(stdscr, 'armaria real')

                        case '5':
                            if moedas >= 50:
                                moedas -= 50
                                inventario['cura'] += 1
                                popup('comprou', 'cura', 1)
                                salas(stdscr, 'armaria real')
                            else:
                                popup('sem_moedas')
                                salas(stdscr, 'armaria real')

                        case 'sair': 
                            main(stdscr)

            else:
                popup('chave', 'chave riscada')
                main(stdscr)

        case 'corredor2':
            popup('sala_vazia')
            main(stdscr)

        case 'salão comunal':
            if 'salão comunal' not in salas_ja_visitadas:
                while True:
                    janela.refresh()
                    janela_action.refresh()
                    janela_inventario.refresh()
                    janela_status.refresh()

                    janela_action.addstr(1, 1, 'Ação:')
                    janela_status.addstr(1, 1, 'Status:')
                    janela_inventario.addstr(1, 1, 'Inventário:')

                    action = menuacao(stdscr, "sala", janela_action, room)

                    if action.lower() == '20':
                        inventario['chave enferrujada'] = 1
                        popup('item', 'chave enferrujada', 1)
                        salas_ja_visitadas.append('salão comunal')
                        main(stdscr)
                        break
                    elif action.lower() == 'sair':
                        main(stdscr)
                        break
                    else:
                        popup('errou')
                        salas(stdscr, 'salão comunal')
            else:
                popup('visited')
                main(stdscr)

        case 'torre2':
            if 'torre2' not in salas_ja_visitadas:
                if save:
                    enemy_life = save
                else:
                    enemy_life = 200

                dano_do_inimigo = 30
                while True:
                    janela.addstr(sh - 2, 2, f"vida: {enemy_life}")
                    janela_status.addstr(len(status) + 3, 1, f'Vida: {life}')
                    for i in range(len(status)):
                        janela_status.addstr(1 + i, 1, status[i])

                    janela_inventario.addstr(1, 1, 'Inventário:')
                    for i, (elemento, valor) in enumerate(inventario.items()):
                        aux = f'{elemento}: {valor}'
                        janela_inventario.addstr(3 + i, 1, aux, curses.A_BOLD) 
                    
                    janela.refresh()
                    janela_action.refresh()
                    janela_inventario.refresh()
                    janela_status.refresh()

                    action = menuacao(stdscr, "sala", janela_action, room)
                    dano_feito, dano_levado = combate(dano_do_inimigo, damage, chance_critico, chance_errar)
                    
                    if action.lower() == 'atacar':
                        if dano_feito == 0:
                            popup('errou_ataque')
                        elif dano_feito == damage * 2.0:
                            popup('critical', dano_feito)
                            enemy_life -= dano_feito
                        else:
                            enemy_life -= dano_feito
                            popup('ataque', dano_feito)

                    if enemy_life <= 0:
                        popup('vitoria')
                        salas_ja_visitadas.append('torre2')
                        moedas += 200
                        popup('moeda', 200)
                        main(stdscr)
                        break
                    
                    if dano_levado == 0:
                        popup('inimigo_errou')
                    
                    if dano_levado == dano_do_inimigo * 2.0:
                        popup('enemy_critical', dano_levado)
                        life -= dano_levado
                    else:
                        life -= dano_levado
                        popup('dano_recebido', dano_levado)
                    
                    if life < 0:
                        popup('gameover', stdscr=stdscr)
                        break
                
                    salas(stdscr, room='torre2', save=enemy_life)
            
            else:
                popup('visited')
                main(stdscr)

        case 'calabouço':
            if 'calabouço' not in salas_ja_visitadas:
                if save:
                    enemy_life = save
                else:
                    enemy_life = 250

                dano_do_inimigo = 35
                while True:
                    janela.addstr(sh - 2, 2, f"vida: {enemy_life}")
                    janela_status.addstr(len(status) + 3, 1, f'Vida: {life}')
                    for i in range(len(status)):
                        janela_status.addstr(1 + i, 1, status[i])

                    janela_inventario.addstr(1, 1, 'Inventário:')
                    for i, (elemento, valor) in enumerate(inventario.items()):
                        aux = f'{elemento}: {valor}'
                        janela_inventario.addstr(3 + i, 1, aux, curses.A_BOLD) 
                    
                    janela.refresh()
                    janela_action.refresh()
                    janela_inventario.refresh()
                    janela_status.refresh()

                    action = menuacao(stdscr, "sala", janela_action, room)
                    dano_feito, dano_levado = combate(dano_do_inimigo, damage, chance_critico, chance_errar)
                    
                    if action.lower() == 'atacar':
                        if dano_feito == 0:
                            popup('errou_ataque')
                        elif dano_feito == damage * 2.0:
                            popup('critical', dano_feito)
                            enemy_life -= dano_feito
                        else:
                            enemy_life -= dano_feito
                            popup('ataque', dano_feito)

                    if enemy_life <= 0:
                        popup('vitoria')
                        salas_ja_visitadas.append('calabouço')
                        inventario['armadura da harpia'] = 1
                        moedas += 200
                        popup('item', 'armadura da harpia', 1)
                        popup('moeda', 200)
                        main(stdscr)
                        break
                    
                    if dano_levado == 0:
                        popup('inimigo_errou')
                    
                    if dano_levado == dano_do_inimigo * 2.0:
                        popup('enemy_critical', dano_levado)
                        life -= dano_levado
                    else:
                        life -= dano_levado
                        popup('dano_recebido', dano_levado)
                    
                    if life < 0:
                        popup('gameover', stdscr=stdscr)
                        break
                
                    salas(stdscr, room='calabouço', save=enemy_life)
            
            else:
                popup('visited')
                main(stdscr)

        case 'quarto real':
            if 'quarto real' not in salas_ja_visitadas:
                if 'chave enferrujada' in inventario:
                    while True:
                        janela.refresh()
                        janela_action.refresh()
                        janela_inventario.refresh()
                        janela_status.refresh()

                        janela_action.addstr(1, 1, 'Ação:')
                        janela_status.addstr(1, 1, 'Status:')
                        janela_inventario.addstr(1, 1, 'Inventário:')

                        action = menuacao(stdscr, "sala", janela_action, room)

                        if action.lower() == 'explorar':
                            moedas += 250
                            popup('moeda', 250)
                            salas_ja_visitadas.append('quarto real')
                            main(stdscr)
                            break
                        if action.lower() == 'sair':
                            salas_ja_visitadas.append('quarto real')
                            main(stdscr)
                            break
                else:
                    popup('chave', 'chave enferrujada')
                    main(stdscr)
            else:
                popup('visited')
                main(stdscr)

        case 'corredor3':
            popup('sala_vazia')
            main(stdscr)

        case 'trono real':
            if 'trono real' not in salas_ja_visitadas:
                inventario['relíquia da família real'] = 1
                reliquias.append('relíquia da família real')
                moedas += 200
                popup('moeda', 200)
                popup('item', 'relíquia da família real', 1)
                salas_ja_visitadas.append('trono real')
                main(stdscr)
            else:
                popup('visited')
                main(stdscr)

        case 'biblioteca2':
            popup('sala_vazia')
            main(stdscr)

        case 'celas':
            if 'celas' not in salas_ja_visitadas:
                if save:
                    enemy_life = save
                else:
                    enemy_life = 100

                dano_do_inimigo = 25
                while True:
                    janela.addstr(sh - 2, 2, f"vida: {enemy_life}")
                    janela_status.addstr(len(status) + 3, 1, f'Vida: {life}')
                    for i in range(len(status)):
                        janela_status.addstr(1 + i, 1, status[i])

                    janela_inventario.addstr(1, 1, 'Inventário:')
                    for i, (elemento, valor) in enumerate(inventario.items()):
                        aux = f'{elemento}: {valor}'
                        janela_inventario.addstr(3 + i, 1, aux, curses.A_BOLD) 
                    
                    janela.refresh()
                    janela_action.refresh()
                    janela_inventario.refresh()
                    janela_status.refresh()

                    action = menuacao(stdscr, "sala", janela_action, room)
                    dano_feito, dano_levado = combate(dano_do_inimigo, damage, chance_critico, chance_errar)
                    
                    if action.lower() == 'atacar':
                        if dano_feito == 0:
                            popup('errou_ataque')
                        elif dano_feito == damage * 2.0:
                            popup('critical', dano_feito)
                            enemy_life -= dano_feito
                        else:
                            enemy_life -= dano_feito
                            popup('ataque', dano_feito)

                    if enemy_life <= 0:
                        popup('vitoria')
                        salas_ja_visitadas.append('celas')
                        inventario['armadura de ossos'] = 1
                        moedas += 100
                        popup('item', 'armadura de ossos', 1)
                        popup('moeda', 100)
                        main(stdscr)
                        break
                    
                    if dano_levado == 0:
                        popup('inimigo_errou')
                    
                    if dano_levado == dano_do_inimigo * 2.0:
                        popup('enemy_critical', dano_levado)
                        life -= dano_levado
                    else:
                        life -= dano_levado
                        popup('dano_recebido', dano_levado)
                    
                    if life < 0:
                        popup('gameover', stdscr=stdscr)
                        break
                
                    salas(stdscr, room='celas', save=enemy_life)
            
            else:
                popup('visited')
                main(stdscr)
        
        case 'capela':
            if 'capela' not in salas_ja_visitadas:
                inventario['relíquia do clérigo'] = 1
                reliquias.append('relíquia do clérigo')
                popup('item', 'relíquia do clérigo', 1)
                salas_ja_visitadas.append('capela')
                main(stdscr)
            else:
                popup('visited')
                main(stdscr)
        
        case 'corredor4':
            if 'corredor4' not in salas_ja_visitadas:
                if save:
                    enemy_life = save
                else:
                    enemy_life = 250
                dano_do_inimigo = 35
                while True:
                    janela.addstr(sh - 2, 2, f"vida: {enemy_life}")
                    janela_status.addstr(len(status) + 3, 1, f'Vida: {life}')
                    for i in range(len(status)):
                        janela_status.addstr(1 + i, 1, status[i])

                    janela_inventario.addstr(1, 1, 'Inventário:')
                    for i, (elemento, valor) in enumerate(inventario.items()):
                        aux = f'{elemento}: {valor}'
                        janela_inventario.addstr(3 + i, 1, aux, curses.A_BOLD) 
                    
                    janela.refresh()
                    janela_action.refresh()
                    janela_inventario.refresh()
                    janela_status.refresh()

                    action = menuacao(stdscr, "sala", janela_action, room)
                    dano_feito, dano_levado = combate(dano_do_inimigo, damage, chance_critico, chance_errar)
                    
                    if action.lower() == 'atacar':
                        if dano_feito == 0:
                            popup('errou_ataque')
                        elif dano_feito == damage * 2.0:
                            popup('critical', dano_feito)
                            enemy_life -= dano_feito
                        else:
                            enemy_life -= dano_feito
                            popup('ataque', dano_feito)

                    if enemy_life <= 0:
                        popup('vitoria')
                        salas_ja_visitadas.append('corredor4')
                        inventario['chave mestra'] = 1
                        moedas += 200
                        popup('moeda', 200)
                        popup('item', 'chave mestra', 1)
                        main(stdscr)
                        break
                    
                    if dano_levado == 0:
                        popup('inimigo_errou')
                    
                    if dano_levado == dano_do_inimigo * 2.0:
                        popup('enemy_critical', dano_levado)
                        life -= dano_levado
                    else:
                        life -= dano_levado
                        popup('dano_recebido', dano_levado)
                    
                    if life < 0:
                        popup('gameover', stdscr=stdscr)
                        break
                
                    salas(stdscr, room='corredor4', save=enemy_life)
            
            else:
                popup('visited')
                main(stdscr)

        case 'jardim real':
            if 'jardim real' not in salas_ja_visitadas:
                while True:
                    janela.refresh()
                    janela_action.refresh()
                    janela_inventario.refresh()
                    janela_status.refresh()

                    janela_action.addstr(1, 1, 'Ação:')
                    janela_status.addstr(1, 1, 'Status:')
                    janela_inventario.addstr(1, 1, 'Inventário:')

                    action = menuacao(stdscr, "sala", janela_action, room)

                    if action.lower() == '51':
                        inventario['frasco de pólen'] = 5
                        popup('item', 'frasco de pólen', 5)
                        salas_ja_visitadas.append('jardim real')
                        main(stdscr)
                        break
                    elif action.lower() == 'sair':
                        main(stdscr)
                        break
                    else:
                        popup('errou')
                        salas(stdscr, 'jardim real')
            else:
                popup('visited')
                main(stdscr)

        case 'muralha fortificada':
            popup('sala_vazia')
            main(stdscr)

        case 'feudo':
            if 'feudo' not in salas_ja_visitadas:
                inventario['relíquia dos ancestrais'] = 1
                reliquias.append('relíquia dos ancestrais')
                popup('item', 'relíquia dos ancestrais', 1)
                salas_ja_visitadas.append('feudo')
                main(stdscr)
            else:
                popup('visited')
                main(stdscr)

        case 'sala de armadilhas':
            if 'sala de armadilhas' not in salas_ja_visitadas:
                while True:
                    janela.refresh()
                    janela_action.refresh()
                    janela_inventario.refresh()
                    janela_status.refresh()

                    janela_action.addstr(1, 1, 'Ação:')
                    janela_status.addstr(1, 1, 'Status:')
                    janela_inventario.addstr(1, 1, 'Inventário:')

                    action = menuacao(stdscr, "sala", janela_action, room)

                    if action.lower() == 'xeque-mate pastor' or 'xeque-mate do pastor':
                        moedas += 500
                        popup('moeda', 500)
                        salas_ja_visitadas.append('sala de armadilhas')
                        main(stdscr)
                        break

                    else:
                        popup('errou')
                        salas(stdscr, 'sala de armadilhas')
            else:
                popup('visited')
                main(stdscr)

        case 'poço dos desejos':
            if 'poço dos desejos' not in salas_ja_visitadas:
                moedas += 50
                popup('moeda', 50)
                salas_ja_visitadas.append('poço dos desejos')
                main(stdscr)
            else:
                popup('visited')
                main(stdscr)

        case 'chafariz monumental':
            popup('sala_vazia')
            main(stdscr)

        case 'saída':
            if len(salas_ja_visitadas) == 17 and 'chave mestra' in inventario:
                if save:
                    enemy_life = save
                else:
                    enemy_life = 400
                dano_do_inimigo = 60
                while True:
                    janela.addstr(sh - 2, 2, f"vida: {enemy_life}")
                    janela_status.addstr(len(status) + 3, 1, f'Vida: {life}')
                    for i in range(len(status)):
                        janela_status.addstr(1 + i, 1, status[i])

                    janela_inventario.addstr(1, 1, 'Inventário:')
                    for i, (elemento, valor) in enumerate(inventario.items()):
                        aux = f'{elemento}: {valor}'
                        janela_inventario.addstr(3 + i, 1, aux, curses.A_BOLD) 
                    
                    janela.refresh()
                    janela_action.refresh()
                    janela_inventario.refresh()
                    janela_status.refresh()

                    action = menuacao(stdscr, "sala", janela_action, room)
                    dano_feito, dano_levado = combate(dano_do_inimigo, damage, chance_critico, chance_errar)
                    
                    if action.lower() == 'atacar':
                        if dano_feito == 0:
                            popup('errou_ataque')
                        elif dano_feito == damage * 2.0:
                            popup('critical', dano_feito)
                            enemy_life -= dano_feito
                        else:
                            enemy_life -= dano_feito
                            popup('ataque', dano_feito)

                    if enemy_life <= 0:
                        popup('vitoria')
                        popup('zerou')
                        main(stdscr)
                        break
                    
                    if dano_levado == 0:
                        popup('inimigo_errou')
                    
                    if dano_levado == dano_do_inimigo * 2.0:
                        popup('enemy_critical', dano_levado)
                        life -= dano_levado
                    else:
                        life -= dano_levado
                        popup('dano_recebido', dano_levado)
                    
                    if life < 0:
                        popup('gameover', stdscr=stdscr)
                        break
                
                    salas(stdscr, room='saída', save=enemy_life)
            else:
                popup('saída')
                main(stdscr)  
        

curses.wrapper(menuinicial)