
import pandas as pd
import numpy as np


def gerar_posicao_e_trade_obs(dados, sinal_compra, sinal_venda, posicao, trade, posicao_obs):
    # Redefinir o índice do DataFrame
    dados = dados.reset_index()
    
    # Inicializa as colunas de posição, trade e obs
    dados[posicao] = False
    dados[trade] = 0
    dados[posicao_obs] = ""

    # Variável para rastrear se estamos em uma posição comprada
    em_posicao = False
    trade_num = 0

    for linha in range(len(dados)):
        # Sinal de compra
        if dados.loc[linha, sinal_compra] == 1 and not em_posicao:
            dados.loc[linha, posicao] = True
            trade_num += 1
            dados.loc[linha, trade] = trade_num
            dados.loc[linha, posicao_obs] = "compra"
            em_posicao = True
        
        # Sinal de venda
        elif dados.loc[linha, sinal_venda] == 1 and em_posicao:
            dados.loc[linha, posicao] = False
            dados.loc[linha, trade] = trade_num
            dados.loc[linha, posicao_obs] = "venda"
            em_posicao = False
        
        # Manter a posição anterior
        elif linha > 0:
            dados.loc[linha, posicao] = dados.loc[linha - 1, posicao]
            dados.loc[linha, trade] = dados.loc[linha - 1, trade]
            if em_posicao:
                dados.loc[linha, posicao_obs] = "mantendo posicao"
            else:
                dados.loc[linha, posicao_obs] = "parado"

    return dados


def calcular_retorno_modelo(dados, close, posicao_obs, retorno_do_modelo):

    # Variáveis para rastrear o preço de compra e venda
    preco_compra = 0.0

    for linha in range(len(dados)):
        # Sinal de compra
        if dados.loc[linha, posicao_obs] == "compra":
            preco_compra = dados.loc[linha, close]
        
        # Sinal de venda
        elif dados.loc[linha, posicao_obs] == "venda" and preco_compra != 0.0:
            preco_venda = dados.loc[linha, close]
            retorno = (preco_venda - preco_compra) / preco_compra
            dados.loc[linha, retorno_do_modelo] = retorno
            preco_compra = 0.0  # Resetar o preço de compra após a venda

    return dados
