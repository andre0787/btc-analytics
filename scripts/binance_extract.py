import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk
from binance.client import Client
from datetime import datetime, timedelta

from utils import trading_utils

plt.style.use("cyberpunk")

# Inicializar cliente Binance (você precisará adicionar suas chaves API)
client = Client()

# Definir parâmetros
symbol = "BTCUSDT"
interval = Client.KLINE_INTERVAL_4HOUR

# Obter dados históricos
klines = client.get_historical_klines(
    symbol,
    interval,
    str((datetime.now() - timedelta(days=365)).strftime("%d %b %Y %H:%M:%S")),
    str(datetime.now().strftime("%d %b %Y %H:%M:%S"))
)

# Converter para DataFrame
dados = pd.DataFrame(klines, columns=[
    'timestamp', 'Open', 'High', 'Low', 'Close', 'Volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'
])

# Converter tipos de dados
dados['timestamp'] = pd.to_datetime(dados['timestamp'], unit='ms')
dados.set_index('timestamp', inplace=True)
for col in ['Open', 'High', 'Low', 'Close', 'Volume']:
    dados[col] = dados[col].astype(float)

# Remover colunas desnecessárias
dados = dados[['Open', 'High', 'Low', 'Close', 'Volume']]

dados = dados.dropna()

# Preparar e calcular dados importantes para o modelo
dados["media_maxima"] = dados.High.rolling(window=20).mean(20)
dados["media_minima"] = dados.Low.rolling(window=20).mean(20)

# Gerar sinais de compra
dados["sinal_compra"] = 0
dados.sinal_compra = (dados.Close > dados.media_maxima).astype(int)

# Gerar sinais de venda
dados["sinal_venda"] = 0
dados.sinal_venda = (dados.Close < dados.media_minima).astype(int)

# Criar colunas necessárias para operacoes
dados["posicao"] = False
dados["trade"] = 0
dados["posicao_obs"] = ""
dados["retorno_modelo"] = 0.0

# Gerar Operacoes
dados = trading_utils.gerar_posicao_e_trade_obs(dados, 
                                                'sinal_compra', 
                                                'sinal_venda', 
                                                'posicao', 
                                                'trade', 
                                                'posicao_obs'
                                                )

# Calcular retorno de todos os trades e retorno da base de comparacao
dados = trading_utils.calcular_retorno_modelo(dados, 
                                            'Close', 
                                            'posicao_obs', 
                                            'retorno_modelo'
                                            )

dados["retorno"] = dados.Close.pct_change()

# Gerar variaveis para plotagem dos dados
dados_retorno_modelo = (1 + dados.retorno_modelo).cumprod()-1
dados_retorno = (1 + dados.retorno).cumprod()-1

# Plotar resultados
dados_retorno_modelo.plot(label = "Modelo")
dados_retorno.plot(label = "Base de Comparação")
plt.legend()
plt.grid()
plt.show()

# Gerar comparativo em termos financeiros
quantia_inicial = 100

valor_final_acumulado_base = quantia_inicial * (1 + dados_retorno.iloc[-1])
valor_final_acumulado_modelo = quantia_inicial * (1 + dados_retorno_modelo.iloc[-1])
quantidade_de_vendas = dados.posicao_obs.value_counts().venda
quantidade_vendas_positivas = len(dados[(dados.posicao_obs == 'venda') & (dados.retorno_modelo > 0)])
quantidade_vendas_negativas = len(dados[(dados.posicao_obs == 'venda') & (dados.retorno_modelo < 0)])

print(f"Valor final acumulado ao aplicar {quantia_inicial} reais na base de comparação: {valor_final_acumulado_base:.2f} reais")
print(f"Valor final acumulado ao aplicar {quantia_inicial} reais no modelo: {valor_final_acumulado_modelo:.2f} reais")
print(f"A estrategia rendeu {quantidade_de_vendas} vendas no total")
print(f"A estrategia rendeu {quantidade_vendas_positivas} vendas com retorno positivo")
print(f"A estrategia rendeu {quantidade_vendas_negativas} vendas com retorno negativo")

diferenca_percentual = ((valor_final_acumulado_modelo - valor_final_acumulado_base) / valor_final_acumulado_base) * 100

if valor_final_acumulado_modelo > valor_final_acumulado_base:
    print(f"O modelo teve um desempenho melhor que a base de comparação por {diferenca_percentual:.2f}%.")
else:
    print(f"A base de comparação teve um desempenho melhor que o modelo por {diferenca_percentual:.2f}%.") 