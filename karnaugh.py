import matplotlib.pyplot as plt
import numpy as np
import os
import shutil

indexImagem = 0

def indexImagemFunc():
    global indexImagem
    indexImagem += 1

def obter_valores_tabela():
    tabela = [[0 for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            tabela[i][j] = int(input(f'Entre com o valor para a célula (linha {i+1}, coluna {j+1}): '))
    return tabela

def gerar_mapa_karnaugh(tabela):
    mapa_karnaugh = [[' ' for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            if tabela[i][j] == 1:
                mapa_karnaugh[i][j] = '1'

    return mapa_karnaugh

def imprimir_mapa_karnaugh(mapa_karnaugh):
    print("Mapa de Karnaugh:")
    print("  00 01 11 10")
    for i, linha in enumerate(mapa_karnaugh):
        print(f" {i} ", end="")
        print(' '.join(linha))

def gerar_mapa_agrupamento_8(valor_1, valor_2, tabela, eh_linha):
    tabela_local = tabela
    if(eh_linha):
        for index, linha in enumerate(tabela):
            if(index == valor_1 or index == valor_2):
                tabela_local[index] = [2, 2, 2, 2]
    else:
        for index, coluna in enumerate(tabela):
            if(index == valor_1 or index == valor_2):
                tabela_local[index] = [2, 2, 2, 2]
        tabela_local = [list(coluna) for coluna in zip(*tabela_local)]

    gerar_imagem(tabela_local)
            
def iterando_linhas_e_colunas(tabela):
    linha_1 = linha_2 = linha_3 = linha_4 = False
    coluna_1 = coluna_2 = coluna_3 = coluna_4 = False

    coluna_1_e_4 = coluna_1_e_2 = coluna_2_e_3 = coluna_3_e_4 = False

    pontas_1 = pontas_2 = False
    pontas_final = False

    tabela_transposta = list(zip(*tabela))

    #Iterando sobre as linhas
    for index, linha in enumerate(tabela):
        primeiro_valor = linha[0]
        segundo_valor  = linha[1]
        terceiro_valor = linha[2]
        quarto_valor   = linha[3]

        if(primeiro_valor == 1 and segundo_valor == 1 and terceiro_valor == 1 and quarto_valor == 1):
            if(index == 0):
                linha_1 = True
            elif(index == 1):
                linha_2 = True
            elif(index == 2):
                linha_3 = True
            else:
                linha_4 = True
        
        if(index == 0):
            if(linha[0] == 1 and linha[3] == 1):
                pontas_1 = True

        if(index == 3):
            if(linha[0] == 1 and linha[3] == 1):
                pontas_2 = True
    
    #verificando agrupamento de 8 das linhas
    linha_1_e_4 = True if linha_1 and linha_4 else False
    linha_1_e_2 = True if linha_1 and linha_2 else False
    linha_2_e_3 = True if linha_2 and linha_3 else False
    linha_3_e_4 = True if linha_3 and linha_4 else False
    
    #Iterando sobre as colunas
    for index, coluna in enumerate(tabela_transposta):
        primeiro_valor = coluna[0]
        segundo_valor  = coluna[1]
        terceiro_valor = coluna[2]
        quarto_valor   = coluna[3]

        if(primeiro_valor == 1 and segundo_valor == 1 and terceiro_valor == 1 and quarto_valor == 1):
            if(index == 0):
                coluna_1 = True
            elif(index == 1):
                coluna_2 = True
            elif(index == 2):
                coluna_3 = True
            else:
                coluna_4 = True
        
    #verificando agrupamento de 8 das colunas
    coluna_1_e_4 = True if coluna_1 and coluna_4 else False
    coluna_1_e_2 = True if coluna_1 and coluna_2 else False
    coluna_2_e_3 = True if coluna_2 and coluna_3 else False
    coluna_3_e_4 = True if coluna_3 and coluna_4 else False

    #gerando agrupamentos de 8 variaveis
    #linhas
    if(linha_1_e_4):
        gerar_mapa_agrupamento_8(0, 3, tabela, True)
    if(linha_1_e_2):
        gerar_mapa_agrupamento_8(0, 1, tabela, True)
    if(linha_2_e_3):
        gerar_mapa_agrupamento_8(1, 2, tabela, True)
    if(linha_3_e_4):
        gerar_mapa_agrupamento_8(2, 3, tabela, True)
    #colunas
    if(coluna_1_e_4):
        gerar_mapa_agrupamento_8(0, 3, tabela_transposta, False)
    if(coluna_1_e_2):
        gerar_mapa_agrupamento_8(0, 1, tabela_transposta, False)
    if(coluna_2_e_3):
        gerar_mapa_agrupamento_8(1, 2, tabela_transposta, False)
    if(coluna_3_e_4):
        gerar_mapa_agrupamento_8(2, 3, tabela_transposta, False)

    #verificando pontas
    if(pontas_1 and pontas_2):
        pontas_final = True

def gerar_imagem(matriz):
    indexImagemFunc()
    cores = [['yellow' if valor == 2 else 'white' for valor in linha] for linha in matriz]

    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            if matriz[i][j] == 2:
                matriz[i][j] = 1

    fig, ax = plt.subplots()

    tabela = ax.table(cellText=matriz, cellColours=cores, loc='center', cellLoc='center', edges='closed')

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(14)
    tabela.scale(0.6, 1.2)

    ax.axis('off')

    plt.savefig(os.path.join('teste', f'imagem_{indexImagem}.png'))
    plt.close()

if __name__ == "__main__":
    if not os.path.exists('teste'):
        os.makedirs('teste')

    shutil.rmtree('teste', ignore_errors=True)
    os.makedirs('teste')
    
    tabela = obter_valores_tabela()
    mapa_karnaugh = gerar_mapa_karnaugh(tabela)
    iterando_linhas_e_colunas(tabela)
    imprimir_mapa_karnaugh(mapa_karnaugh)
