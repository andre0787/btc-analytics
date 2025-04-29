import pandas as pd
import matplotlib.pyplot as plt
import mplcyberpunk
from binance.client import Client
from datetime import datetime, timedelta
from utils import trading_utils

plt.style.use("cyberpunk")

# Dicionário com todos os intervalos disponíveis
INTERVALOS = {
    '1m': Client.KLINE_INTERVAL_1MINUTE,
    '3m': Client.KLINE_INTERVAL_3MINUTE,
    '5m': Client.KLINE_INTERVAL_5MINUTE,
    '15m': Client.KLINE_INTERVAL_15MINUTE,
    '30m': Client.KLINE_INTERVAL_30MINUTE,
    '1h': Client.KLINE_INTERVAL_1HOUR,
    '2h': Client.KLINE_INTERVAL_2HOUR,
    '4h': Client.KLINE_INTERVAL_4HOUR,
    '6h': Client.KLINE_INTERVAL_6HOUR,
    '8h': Client.KLINE_INTERVAL_8HOUR,
    '12h': Client.KLINE_INTERVAL_12HOUR,
    '1d': Client.KLINE_INTERVAL_1DAY,
    '3d': Client.KLINE_INTERVAL_3DAY,
    '1w': Client.KLINE_INTERVAL_1WEEK,
    '1M': Client.KLINE_INTERVAL_1MONTH
}

def selecionar_intervalo(intervalo):
    """
    Seleciona o intervalo desejado a partir de uma string
    
    Args:
        intervalo: String com o intervalo desejado (ex: '1h', '4h', '1d')
    
    Returns:
        Intervalo correspondente da API da Binance
    """
    if intervalo not in INTERVALOS:
        raise ValueError(f"Intervalo inválido. Intervalos disponíveis: {list(INTERVALOS.keys())}")
    return INTERVALOS[intervalo]

def test_strategy(interval, days=365, window=20):
    """
    Testa a estratégia com diferentes intervalos e parâmetros
    
    Args:
        interval: Intervalo de tempo da Binance
        days: Número de dias para análise
        window: Janela da média móvel
    """
    client = Client()
    symbol = "BTCUSDT"
    
    # Obter dados históricos
    klines = client.get_historical_klines(
        symbol,
        interval,
        str((datetime.now() - timedelta(days=days)).strftime("%d %b %Y %H:%M:%S")),
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
    dados["media_maxima"] = dados.High.rolling(window=window).mean()
    dados["media_minima"] = dados.Low.rolling(window=window).mean()
    
    # Gerar sinais
    dados["sinal_compra"] = (dados.Close > dados.media_maxima).astype(int)
    dados["sinal_venda"] = (dados.Close < dados.media_minima).astype(int)
    
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
    
    # Calcular retornos
    dados = trading_utils.calcular_retorno_modelo(dados, 
                                                'Close', 
                                                'posicao_obs', 
                                                'retorno_modelo'
                                                )
    
    dados["retorno"] = dados.Close.pct_change()
    
    # Calcular métricas
    dados_retorno_modelo = (1 + dados.retorno_modelo).cumprod()-1
    dados_retorno = (1 + dados.retorno).cumprod()-1
    
    quantia_inicial = 100
    valor_final_acumulado_base = quantia_inicial * (1 + dados_retorno.iloc[-1])
    valor_final_acumulado_modelo = quantia_inicial * (1 + dados_retorno_modelo.iloc[-1])
    
    quantidade_de_vendas = dados.posicao_obs.value_counts().get('venda', 0)
    quantidade_vendas_positivas = len(dados[(dados.posicao_obs == 'venda') & (dados.retorno_modelo > 0)])
    quantidade_vendas_negativas = len(dados[(dados.posicao_obs == 'venda') & (dados.retorno_modelo < 0)])
    
    diferenca_percentual = ((valor_final_acumulado_modelo - valor_final_acumulado_base) / valor_final_acumulado_base) * 100
    
    return {
        'interval': interval,
        'window': window,
        'days': days,
        'valor_final_base': valor_final_acumulado_base,
        'valor_final_modelo': valor_final_acumulado_modelo,
        'diferenca_percentual': diferenca_percentual,
        'quantidade_vendas': quantidade_de_vendas,
        'vendas_positivas': quantidade_vendas_positivas,
        'vendas_negativas': quantidade_vendas_negativas
    }

# Exemplo de uso
intervalo_desejado = '4h'  # Você pode mudar para qualquer intervalo disponível
interval = selecionar_intervalo(intervalo_desejado)

# Testar diferentes intervalos
intervals = [
    selecionar_intervalo('1h'),
    selecionar_intervalo('4h'),
    selecionar_intervalo('1d')
]

results = []
for interval in intervals:
    result = test_strategy(interval)
    results.append(result)
    print(f"\nResultados para {interval}:")
    print(f"Valor final base: {result['valor_final_base']:.2f}")
    print(f"Valor final modelo: {result['valor_final_modelo']:.2f}")
    print(f"Diferença percentual: {result['diferenca_percentual']:.2f}%")
    print(f"Quantidade de vendas: {result['quantidade_vendas']}")
    print(f"Vendas positivas: {result['vendas_positivas']}")
    print(f"Vendas negativas: {result['vendas_negativas']}")

# Criar DataFrame com resultados
df_results = pd.DataFrame(results)
print("\nResumo comparativo:")
print(df_results[['interval', 'valor_final_modelo', 'diferenca_percentual', 'quantidade_vendas']]) 