"""Jogo da Batalha Naval
"""

import re
import random
import itertools
import operator

### MAIN FUNCTION ###
def main():
    """Função onde inicia o programa"""
    global jogador

    melhores = {}
    melhores = abrir()

    # Apresenta o banner de entrada
    banner('\__|BATALHA NAVAL|__/', 34)

    # Apresenta melhores jogadores
    banner('OS MELHORES OFICIAIS', 34)
    print_melhores(melhores)

    # Armazenar o nome do jogador
    jogador = input('\nJogador #1: ')

    vitorias = 0

    continuar = 's'

    while continuar.lower() == 's':

        iniciar_tabuleiros()

        distribuir_equipamento_cpu()
        distribuir_equipamento_jogador()

        jogar()

        if ganhou_jogador():
            vitorias += 1

        print('\nTem ' + str(vitorias) + ' batalha(s) conquistadas!\n')

        continuar = input('Jogar outra vez? (s/n): ')

    melhores[jogador] = int(vitorias)

    melhores = dict(sorted(melhores.items(), key=operator.itemgetter(1),reverse=True))
    dict(itertools.islice(melhores.items(), 2))

    guardar(melhores)

    # Apresenta melhores jogadores
    banner('OS MELHORES OFICIAIS', 34)
    print_melhores(melhores)


def print_melhores(m):

    lugar = 1


    for jogador, vitorias in m.items():
        print("{} - {}, {}\n".format(lugar, jogador, vitorias))
        lugar += 1

def abrir():
    dic = {}

    file = open('melhores', 'r')

    for l in file.readlines():
        jogador, vitorias = l[:-1].split(',')
        dic[jogador] = int(vitorias)

    return dic

def guardar(dic):

    file = open('melhores', "w")

    for jogador, vitorias in dic.items():
        file.write("{},{}\n".format(jogador, vitorias))

    file.close()

def jogar():

    banner('Começa a BATALHA! ', 36)

    jogada = 1

    while not ganhou_cpu() and not ganhou_jogador():

        desenhar_computador(tabuleiro_cpu, "CPU")
        desenhar(tabuleiro_jogador, 'Jogada n.º ' + str(jogada))

        l, c = obter_coordenadas()

        tiro = ' X '

        if tabuleiro_cpu[l][c] != ' X ' and tabuleiro_cpu[l][c] != '~~~':
            tabuleiro_cpu[l][c] = f"{bcolors.OKGREEN}{tiro}{bcolors.ENDC}".format(tiro)
        else:
            tabuleiro_cpu[l][c] = f"{bcolors.FAIL}{tiro}{bcolors.ENDC}".format(tiro)

        l = random.randint(0, num_linhas - 1)
        c = random.randint(0, num_colunas - 1)

        if tabuleiro_jogador[l][c] != ' X ' and tabuleiro_jogador[l][c] != '~~~':
            tabuleiro_jogador[l][c] = f"{bcolors.FAIL}{tiro}{bcolors.ENDC}".format(tiro)
        else:
            tabuleiro_jogador[l][c] = f"{bcolors.OKGREEN}{tiro}{bcolors.ENDC}".format(tiro)


        jogada += 1


def ganhou_cpu():

    for l in tabuleiro_jogador:
        for c in l:
            if c in ['\x1b[94mSBM\x1b[0m', '\x1b[94mFRG\x1b[0m', '\x1b[94mNAV\x1b[0m', '\x1b[94mCRZ\x1b[0m', '\x1b[94mPAV\x1b[0m']:
                return False



    return True

def ganhou_jogador():

    for l in tabuleiro_cpu:
        for c in l:
            if c in ['\x1b[94mSBM\x1b[0m', '\x1b[94mFRG\x1b[0m', '\x1b[94mNAV\x1b[0m', '\x1b[94mCRZ\x1b[0m', '\x1b[94mPAV\x1b[0m']:
                return False

    return True

def distribuir_equipamento_jogador():
    # Lista de equipamento para distribuir no tabuleiro do jogador

    distribuir = [('SBM', 1), ('FRG', 2), ('NAV', 3), ('CRZ', 4), ('PAV', 5) ]

    banner('Distribuir equipamentos... ', 28)

    while len(distribuir) > 0:

        equipamento = distribuir[0][0]
        dimensao = distribuir[0][1]

        desenhar(tabuleiro_jogador, '\nOnde queres colocar o equipamento {} com dimensão {}?'.format(equipamento, dimensao))

        l, c, o = obter_coordenadas_e_orientacao()

        while not verificar_posicao(tabuleiro_jogador, equipamento, dimensao, l, c, o):
            print(f"{bcolors.WARNING}Erro: Posição já ocupada ou sem espaço disponível para colocar equipamento{bcolors.ENDC}")
            l, c, o = obter_coordenadas_e_orientacao()




        posicionar_equipamento(tabuleiro_jogador, equipamento, dimensao, l, c, o)

        del distribuir[0]


def distribuir_equipamento_cpu():
    # Lista de equipamento para distribuir no tabuleiro do jogador

    distribuir = [('SBM', 1), ('FRG', 2), ('NAV', 3), ('CRZ', 4), ('PAV', 5) ]

    while len(distribuir) > 0:

        equipamento = distribuir[0][0]
        dimensao = distribuir[0][1]

        l = random.randint(0, num_linhas - 1)
        c = random.randint(0, num_colunas - 1)
        o = 'hv'[random.randint(0,1)]


        while not verificar_posicao(tabuleiro_cpu, equipamento, dimensao, l, c, o):
            l = random.randint(0, num_linhas - 1)
            c = random.randint(0, num_colunas - 1)
            o = 'hv'[random.randint(0,1)]

        posicionar_equipamento(tabuleiro_cpu, equipamento, dimensao, l, c, o)

        del distribuir[0]




def posicionar_equipamento(tabuleiro, equipamento, dimensao, linha, coluna, orientacao):
    """Função que posiciona um equipamente, com uma dimensão num tabuleiro, numa
    coordenada (linha e coluna) específica e com uma orientação (horizontal ou vertical)."""

    if orientacao == 'h':
        if coluna + dimensao < num_colunas:
            for i in range(dimensao):
                tabuleiro[linha][coluna+i] = f"{bcolors.OKBLUE}{equipamento}{bcolors.ENDC}".format(equipamento)
    else:
        if linha + dimensao < num_linhas:
            for i in range(dimensao):
                tabuleiro[linha + i][coluna] = f"{bcolors.OKBLUE}{equipamento}{bcolors.ENDC}".format(equipamento)

def verificar_posicao(tabuleiro, equipamento, dimensao, linha, coluna, orientacao):
    """Função que verifica (True ou False) se um equipamente, com uma dimensão pode
    ser colocado num tabuleiro, numa coordenada (linha e coluna) específica e com
    uma orientação (horizontal ou vertical)."""

    if orientacao == 'h':
        if coluna + dimensao >= num_colunas:
            return False
        for i in range(dimensao):
            if (tabuleiro[linha][coluna + i] != '~~~'):
                return False
    else:
        if linha + dimensao >= num_linhas:
            return False
        for i in range(dimensao):
            if (tabuleiro[linha + i][coluna ] != '~~~'):
                return False

    return True

def obter_coordenadas_e_orientacao():
    """A função recolhe as coordenada (linha e coluna) e a orientação de um equipamento."""

    pos = input('Posição [ex. A2h]> ')

    while re.findall("^[a-zA-Z]\d+[h|v]$", pos)==[]:
        print(f"{bcolors.WARNING}Erro: Posição inválida{bcolors.ENDC}")
        pos = input('Posição [ex. A2h]> ')

    l = int(ord(pos[0].upper()) - ord('A'))
    c = int(pos[1:-1])
    o = pos[-1]

    while l < 0 or l >= num_linhas or c < 0 or c >= num_colunas:
        print(f"{bcolors.WARNING}Erro: Posição inválida{bcolors.ENDC}")
        l, c, o = obter_coordenadas_e_orientacao()

    return l, c, o

def obter_coordenadas():
    """A função recolhe as coordenada (linha e coluna) de um equipamento."""

    pos = input('Posição [ex. A2h]> ')

    while re.findall("^[a-zA-Z]\d+", pos)==[]:
        print(f"{bcolors.WARNING}Erro: Posição inválida{bcolors.ENDC}")
        pos = input('Posição [ex. A2h]> ')

    l = int(ord(pos[0].upper()) - ord('A'))
    c = int(pos[1:])

    while l < 0 or l >= num_linhas or c < 0 or c >= num_colunas:
        print(f"{bcolors.WARNING}Erro: Posição inválida{bcolors.ENDC}")
        l, c = obter_coordenadas()

    return l, c


def split_coord(coord):
    return ord(coord[0]) - ord('A'), coord[1:]


def desenhar(tabuleiro, msg):

    print('\n', msg.center(num_colunas*5, ' '), '\n')
    print('   ', '  '.join([ str(i).center(3, ' ') for i in range(num_colunas)]))
    print('  +', '-'*(num_colunas*5), '+', sep='')

    i = 0
    for linha in  tabuleiro:
        print(chr(ord('A')+i), '|', '  '.join(linha), '|')
        i += 1

    print('  +', '-'*(num_colunas*5), '+', sep='')

def desenhar_computador(tabuleiro, msg):

    print('\n', msg.center(num_colunas*5, ' '), '\n')
    print('   ', '  '.join([ str(i).center(3, ' ') for i in range(num_colunas)]))
    print('  +', '-'*(num_colunas*5), '+', sep='')

    i = 0
    for linha in  tabuleiro:

        a  = list()

        for c in linha:
            if c in ['\x1b[94mSBM\x1b[0m', '\x1b[94mFRG\x1b[0m', '\x1b[94mNAV\x1b[0m', '\x1b[94mCRZ\x1b[0m', '\x1b[94mPAV\x1b[0m']:
                a.append('~~~')
            else:
                a.append(c)

        print(chr(ord('A')+i), '|', '  '.join(a), '|')
        i += 1

    print('  +', '-'*(num_colunas*5), '+', sep='')



def banner(frase, padding=20):
    """Procedimento que imprime um banner no ecã."""

    l = len(frase)

    print("*"*(l+padding), sep="")
    print("*", " "*(l+padding-2), "*", sep="")
    print("*"," "*int((padding-1)/2), f"{bcolors.BOLD}{bcolors.OKGREEN}{frase}{bcolors.ENDC}".format(frase), " "*int((padding-1)/2), "*", sep="")
    print("*", " "*(l+padding-2), "*", sep="")
    print("*"*(l+padding), sep="")


def iniciar_tabuleiros():
    global tabuleiro_cpu
    global tabuleiro_jogador

    tabuleiro_jogador = [['~~~' for x in range(num_colunas)] for y in range(num_linhas)]
    tabuleiro_cpu = [['~~~' for x in range(num_colunas)] for y in range(num_linhas)]

### PROGRAM ENTRY POINT ###

### DATA STRUCTURE ###

# Cores para formatação do texto
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

jogador = 'Jogado #1'

num_linhas = 10
num_colunas = 10

tabuleiro_jogador = [['~~~' for x in range(num_colunas)] for y in range(num_linhas)]
tabuleiro_cpu = [['~~~' for x in range(num_colunas)] for y in range(num_linhas)]

# Iniciar a execução do programa pela função main()
if __name__ == "__main__":
    main()

### END CODE ###