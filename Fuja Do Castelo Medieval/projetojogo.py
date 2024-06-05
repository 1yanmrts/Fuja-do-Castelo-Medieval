import platform
import sys
import subprocess
import time

if platform.system() == 'Windows':
    if 'curses' not in sys.modules:
        subprocess.check_call(['pip', 'install', 'windows-curses'])
    import curses
else:
    import curses


invent = {'cura': 20, 'espada': 10, 'chapeu': 10, 'elmo': 1}

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

    botoes = ['Inicio', 'Opções', 'Sair']
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
                elif aux == botoes[1]:
                    opcaocontroles(stdscr)
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


def opcaocontroles(stdscr):
    """Menu de controles"""
    sh, sw = tamanhojanela(stdscr)
    xjanela = sw//2
    yjanela = sh//2
    janela = curses.newwin(yjanela, xjanela, yjanela//2, xjanela//2)
    janela.border()
    janela.keypad(True)
    
    texto = [
        'CONTROLES:',
        '          ',
        'Seta para cima (↑) para ir para cima ',
        'Seta para a baixo (↓) para ir para baixo',
        'Seta para a esquerda (←) para ir para a esquerda',
        'Seta para a direita (→) para ir para a direita',
        'Aperte TAB para abrir o menu de ações e escrever',
        'Aperte I para abrir o inventário',
        'Aperte ENTER ( ↵) para interagir e entrar em salas'
        '',
        '',
        '',
        'Aperte ESC para voltar',
    ]

    while True:

        for linha in range(len(texto)):
            janela.addstr(1 + linha, 1, texto[linha], curses.A_LOW)
        
        key = janela.getch()
        if key == 27: #TECLA ESC
            menuinicial(stdscr)

        janela.refresh()



def main(stdscr):
    """Tela principal do jogo. Onde aparece o mapa, inventário e vida. Aqui também é definido o movimento"""
    curses.curs_set(0) 
    stdscr.clear()
    stdscr.refresh()
    matriz = [
        ['entrada', 'corredor', 'bau', 'biblioteca', 'ruínas'],
        ['torre', 'armadura de cavalheiro', 'corredor', 'salão comunal', 'torre'],
        ['calabouço', 'quarto real', 'corredor', 'trono em ruínas', 'biblioteca'],
        ['celas', 'ponte', 'jardim', 'chafariz monumental', 'muralha'],
        ['feudo', 'sala de armadilhas', 'ruínas', 'corredor', 'saída'],
    ] 

    sh, sw = tamanhojanela(stdscr)
    pos_x = 0
    pos_y = 0
    vida = 100

    display = curses.newwin(sh//2 + 6, sw//2 - 1, sh*3//10, sw//2)
    janela = curses.newwin(sh, sw, 0, 0)
    janela_action = curses.newwin(sh//3 - 3, sw//2 - 1, (sh*3//4) - 1, 1) 
    janela_info = curses.newwin(sh//2 - 5, sw//2 - 1, sh//2 - 7, 1)
    janela_info2 = curses.newwin(sh//2 - 8, sw//2 - 4, sh//2 - 5, 2) #Essa janela que vai receber os textos
    
    display.border()
    janela.border()
    janela_action.border()
    janela_info.border()

    janela.keypad(True)
    janela_action.keypad(True)
    janela_info.keypad(True)

    #Loop principal
    while True:
        janela.addstr(2, 2, 'Vida: {}'.format(vida))
        janela_action.addstr(1, 1, 'Ação: ')
        janela_info.addstr(1, 1, 'Informações: ')

        #Serve para apagar a info/display assim que passo para a sala seguinte e mostra a info da sala nova
        janela_info2.clear()
        display.clear()
        
        display.border()

        #Mostrar a matriz e o lugar selecionado
        for linha in range(len(matriz)):
            for coluna in range(len(matriz[linha])):
                if pos_y == linha and pos_x == coluna:
                    janela.addstr(linha + 5, sw//18 + coluna * (sw//5), matriz[linha][coluna], curses.A_STANDOUT)
                    janela_info2.addstr(1, 0, infosalas(matriz[linha][coluna]))
                    room = matriz[linha][coluna]
                else:
                    janela.addstr(linha + 5, sw//18 + coluna * (sw//5), matriz[linha][coluna])
        

        #Mostrar o preview de cada sala
        #TEM VÁRIOS ERROS AQUI
        with open('preview_salas.txt', 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
        
        linhas = conteudo.strip().split('\n')

        contadordelinhas = 0
        #EXISTEM VÁRIOS ERROS NESSE LOOP. 
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

        key = janela.getch()
    
        #Essa sequência de if's serve para se movimentar no mapa
        if key == curses.KEY_RIGHT and pos_x < len(matriz[0]) - 1  or key == 454 and pos_x < len(matriz[0]) - 1:
            pos_x += 1

        if key == curses.KEY_LEFT and pos_x > 0 or key == 452 and pos_x > 0 :
            pos_x += -1

        if key == curses.KEY_UP and pos_y > 0 or key == 450 and pos_y > 0:
            pos_y += -1
        
        if key == curses.KEY_DOWN and pos_y < len(matriz) - 1 or key == 456 and pos_y < len(matriz) - 1:
            pos_y += 1

        if key == 27: #TECLA ESC
            menuinicial(stdscr)
            break

        if key == 9: #TECLA TAB
            menuacao(stdscr, "principal", janela_action)
        
        if key == ord('I') or key == ord('i'): 
            inventario(stdscr, invent, 10)
            break
        
        if key == curses.KEY_ENTER or key == 10:
            aux = matriz[pos_y][pos_x]
            salas(stdscr, aux)
            break


def menuacao(stdscr, check, window, room = None):
    """Aqui vai ser recebido os comando de texto que serão executados.
    Comandos como usar itens, armaduras, atacar, defender, etc.
    """
    janela = window
    janela.border()
    janela.keypad(True)
    janela.addstr(1, 1, 'Ação: ', curses.A_BLINK)

    curses.echo() #Essa função permite o input do usuário aparecer na janela
    texto = janela.getstr(2, 1) #Essa função permite o input do usuário
    curses.noecho()#Essa função desabilita a exibição do texto
    
    bag = inventario(stdscr, invent)
    palavras = texto.decode().split() #TEM QUE USAR O DECODE PQ "TEXTO" RECEBE STRINGS EM BYTES
    print(palavras)


    if 'usar' in palavras:
        if palavras[1] in bag:
            bag[palavras[1]] -= 1

    if check == "principal":
        main(stdscr)
        return texto

    if check == "sala":
        salas(stdscr, room)
        return texto
        
# def remover():
#     """Remover itens do inventário"""
#     pass

# def mover():
#     "Mover itens do inventário"
#     pass

def inventario(stdscr, mochila = None, keypressed = None):
    """Inventário representado por um dicionário com itens sendo chaves e valores sendo suas utilidades"""
    
    if keypressed:
        sh, sw = tamanhojanela(stdscr)

        yjanela = sh//2
        xjanela = sw//2
        janela = curses.newwin( yjanela, xjanela, yjanela//2, xjanela//2) 
        janela.keypad(True)


        while True:
            janela.clear()
            janela.border()
            janela.addstr(1, 1, 'Inventário: ')

            for i, (elemento, valor) in enumerate(mochila.items()):
                aux = f'{elemento}: {valor}'
                janela.addstr(3 + i, 1, aux, curses.A_BOLD) 

            key = janela.getch()
            if key == 27: #TECLA ESC
                main(stdscr)
                break
        
    return mochila   


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
        

def salas(stdscr, room = None):
    """Janela que vai servir pra mostrar os conteúdos de uma sala"""
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
    #EXISTEM VÁRIOS ERROS NESSE LOOP. 
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

    janela_action = curses.newwin(sh//3 - 4, sw - len(maiorlinha), 1, len(maiorlinha) - 1)
    janela_status = curses.newwin(sh//3 - 3, sw - len(maiorlinha), sh//3 - 2, len(maiorlinha) - 1)
    janela_inventario = curses.newwin(sh - (2*sh//3 - 4), sw - len(maiorlinha), sh//2 + 1, len(maiorlinha) - 1)
    
    janela_action.border()
    janela_status.border()
    janela_inventario.border()

    match room:
        
        case 'bau':
            while True:
                janela_action.addstr(1, 1, 'Ação:')
                janela_status.addstr(1, 1, 'Status:')
                janela_inventario.addstr(1, 1, 'Inventário:')

                janela.refresh()
                janela_action.refresh()
                janela_inventario.refresh()
                janela_status.refresh()

                key = janela.getch()
                if key == 27: #TECLA ESC
                    main(stdscr)
                    break
                if key == 9: #TECLA TAB
                    answer = menuacao(stdscr, "sala", janela_action, room)
                
                # if answer.decode() == '2123ond':
                # else:
                #     salas(stdscr, room)
        
        case 'entrada':
            while True:
                janela_action.addstr(1, 1, 'Ação:')
                janela_status.addstr(1, 1, 'Status:')
                janela_inventario.addstr(1, 1, 'Inventário:')

                janela.refresh()
                janela_action.refresh()
                janela_inventario.refresh()
                janela_status.refresh()

                key = janela.getch()
                if key == 27: #TECLA ESC
                    main(stdscr)
                    break

curses.wrapper(menuinicial)