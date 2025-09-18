import joblib
import pandas as pd
import sys

def fazer_predicao(ticker, dados_input):
    """
    Carrega o modelo salvo para um ticker específico e faz a predição.
    """
    try:
        # Define o caminho do modelo com base no ticker
        caminho_modelo = f'modelos/{ticker}_model.pkl'
        
        # Carrega o modelo de um arquivo
        model = joblib.load(caminho_modelo)
        
        # Faz a predição (o modelo deve retornar 1 para Compra e 0 para Venda)
        predicao = model.predict(dados_input)
        
        # Para demonstração, vamos simular a probabilidade (certeza)
        probabilidade = model.predict_proba(dados_input)
        certeza = max(probabilidade[0]) * 100
        
        return predicao[0], certeza
    
    except FileNotFoundError:
        print(f"Erro: Arquivo do modelo '{caminho_modelo}' não encontrado.")
        return None, None
    except Exception as e:
        print(f"Erro ao fazer a predição: {e}")
        return None, None

if __name__ == "__main__":
    # A entrada real viria do seu script coletor.
    # Por enquanto, vamos simular um DataFrame com as features necessárias.
    dados_exemplo = pd.DataFrame([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]], 
                                 columns=['close', 'volume', 'SMA_3d', 'SMA_7d', 'SMA_14d', 'EMA_3d', 'EMA_7d', 'EMA_14d', 'RSI_14d', 'BBL_20_2.0', 'BBM_20_2.0', 'BBU_20_2.0', 'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9'])
    
    # Faz a predição para um ticker de exemplo
    ticker_exemplo = 'VALE3'
    predicao, certeza = fazer_predicao(ticker_exemplo, dados_exemplo)
    
    if predicao is not None:
        operacao = "COMPRA" if predicao == 1 else "VENDA"
        print(f"Predição para {ticker_exemplo}: {operacao} com {certeza:.2f}% de certeza.")